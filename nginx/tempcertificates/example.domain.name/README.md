### This is a placeholder ###

### Before NGINX will boot you must create a directory containing a self-signed certificate to boot NGINX and LetsEncrypt to acquire a valid signed certificate for https deployment ###

## Steps to create until automation is complete # #TODO remove once automatically creating default certificates for each domain in the config
# 1. Create domain directories (root.domain www.root.domain dev.root.domain)
# 2. Create a self signed certificate for each directory created using OpenSSL
# 3. Create a password file for the certificate in the data/certbot/conf/live directory named test.pass with a password per certificat per line
