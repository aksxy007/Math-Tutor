FROM node:18-alpine

WORKDIR /usr/src/app

COPY package* .

RUN npm install

COPY . .

EXPOSE 3001

CMD [ "node", "index.js" ]