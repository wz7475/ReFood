FROM node:18-alpine3.17 as build

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

FROM ubuntu
WORKDIR /app
RUN apt-get update
RUN apt-get install nginx -y
COPY --from=build /app/dist /var/www/html/
COPY ./nginix.conf ./nginix.conf
EXPOSE 80
CMD ["nginx", "-c", "./nginix.conf", "-g","daemon off;"]