FROM node:12 
WORKDIR /usr/src/app
COPY package.json ./
RUN yarn install --production=true
COPY . .
EXPOSE 3000
RUN yarn run build-prod
CMD ["yarn", "run", "start"]