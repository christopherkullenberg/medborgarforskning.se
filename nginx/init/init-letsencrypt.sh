#!/bin/bash
# Derrived from init-letsencrypt.sh on https://github.com/wmnnd/nginx-certbot

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

#domains=(arcstest.brierjon.com medborgarforskning.se www.medborgarforskning.se dev.medborgarforskning.se) # TODO move to domains config variable
domains=(arcstest.brierjon.com) # TODO move to domains config variable
rsa_key_size=4096 # TODO move to RSA certificate config variable
data_path="./../../data/certbot"
email="jonathan.brier@gu.se" # Adding a valid address is strongly recommended # TODO move to admin email config variable
staging=1 # Set to 1 if you're testing your setup to avoid hitting request limits # TODO move to environment type config variable

if [ -d "$data_path" ]; then
  read -p "Existing data found for $domains. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi


#if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
#  echo "### Downloading recommended TLS parameters ..."
#  mkdir -p "$data_path/conf"
#  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
#  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
#  echo
#fi

### nginx will not start without a certificate with ssl enabled - generate a self signed dummy certificate that will be replaced by LetsEncrypt certificate automation
##### Begin LetsEncrypt init assit with nginx #####
echo "### Creating dummy certificate for $domains ..."
path="/etc/letsencrypt/live/$domains"
mkdir -p "$data_path/conf/live/$domains"
docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:1024 -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" letsencrypt
echo

#
echo "### Starting nginx ..."
docker-compose up --force-recreate -d nginximg
echo

echo "### Deleting dummy certificate for $domains ..."
docker-compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$domains && \
  rm -Rf /etc/letsencrypt/archive/$domains && \
  rm -Rf /etc/letsencrypt/renewal/$domains.conf" letsencrypt
echo
##### End LetsEncrypt init assit with nginx #####

##### Wait for nginximg to boot - it can take a while ####
echo "### Waiting for 35 seconds for nginx to start ###"
sleep 35

echo "### Requesting Let's Encrypt certificate for $domains ..."
#Join $domains to -d args
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Select appropriate email arg
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" letsencrypt
echo

echo "### Reloading nginx ..."
docker-compose exec nginximg nginx -s reload
