FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

COPY interactivemaps_frontend/package*.json ./

RUN npm install

COPY interactivemaps_frontend .

RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist/spa" ]