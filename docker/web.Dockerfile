FROM node:20-alpine3.19 as build-stage

LABEL maintainer="Romuald Oluwatobi <romualdnoualinon@gmail.com>"

WORKDIR /app

COPY ./package*.json ./

RUN npm i

COPY . .

RUN npm run build

# Nginx server
FROM nginx:1.27.1-alpine

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80