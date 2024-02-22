FROM node:lts
WORKDIR /app

COPY package.json ./
RUN npm install && npm cache clean --force

COPY app.js ./
COPY src ./src/

EXPOSE 3000

CMD ["node", "app.js"]
