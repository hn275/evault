FROM node:24-alpine3.21

WORKDIR /evault_webui

COPY package*.json .
COPY . .

RUN npm i

EXPOSE 5173

CMD ["npm", "run", "dev"]
