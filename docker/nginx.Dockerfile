FROM nginx:1.27.1-alpine

COPY ./nginx.site.conf /etc/nginx/conf.d/nginx.site.conf