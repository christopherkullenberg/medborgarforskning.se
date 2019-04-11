FROM tiangolo/uwsgi-nginx-flask:python3.7

# ENV STATIC_INDEX 1

COPY ./app /app
RUN pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#RUN pip3 install --upgrade pip
#RUN pip3 install beautifulsoup4
#RUN pip3 install requests
#RUN pip3 install lxml
