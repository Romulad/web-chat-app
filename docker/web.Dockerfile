FROM node:20-alpine3.19 as build-stage

LABEL maintainer="Romuald Oluwatobi <romualdnoualinon@gmail.com>"

WORKDIR /app

COPY ./package*.json ./

RUN npm i

COPY . .

RUN npm run build

# Nginx server
FROM nginx:1.27.1-alpine

RUN addgroup -S web
RUN adduser -G web -S web-user

COPY --from=build-stage --chown=web-user:web /app/dist /usr/share/nginx/html

USER web-user

EXPOSE 80