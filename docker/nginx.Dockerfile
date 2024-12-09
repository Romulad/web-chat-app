FROM nginx:1.27.1-alpine

RUN apk update && apk add certbot

COPY ssl-params.inc /etc/nginx/conf.d/ssl-params.inc

COPY acme.inc /etc/nginx/conf.d/acme.inc

RUN sudo certbot certonly --nginx --non-interactive --agree-tos --email myservicemailshome@gmail.com --domains ec2-35-180-138-45.eu-west-3.compute.amazonaws.com

# COPY acme-client /etc/periodic/weekly/acme-client

# RUN chmod +x /etc/periodic/weekly/acme-client

# RUN /etc/periodic/weekly/acme-client

COPY ./nginx.site.conf /etc/nginx/conf.d/nginx.site.conf
