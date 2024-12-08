FROM nginx:1.27.1-alpine

RUN apk update && apk add acme-client openssl

COPY ssl-params.inc /etc/nginx/conf.d/ssl-params.inc

COPY acme.inc /etc/nginx/conf.d/acme.inc

COPY acme-client /etc/periodic/weekly/acme-client

RUN chmod +x /etc/periodic/weekly/acme-client

RUN /etc/periodic/weekly/acme-client

COPY nginx.conf /etc/nginx/conf.d/nginx.site.conf