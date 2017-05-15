FROM nginx:latest

EXPOSE 80

RUN apt-get update
COPY src/index.html /usr/share/nginx/html



