FROM alpine

# Install required packages
RUN apk update
RUN apk upgrade
RUN apk add --update python python-dev py-pip postgresql-client postgresql-dev build-base gettext

# Initialize
RUN mkdir -p /data/web
COPY . /data/web/
WORKDIR /data/web/


#Setup
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Prepare
RUN mkdir -p socialNetwork/static/admin
