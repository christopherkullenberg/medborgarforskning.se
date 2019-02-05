
# To purge old container images:
# Use bash (wont work in fish):
# sudo docker rmi $(sudo docker images -f "dangling=true" -q)

sudo docker stop mycontainer
sudo docker rm mycontainer
sudo docker build -t myimage .
sudo docker run -d --name mycontainer -p 80:80 myimage

