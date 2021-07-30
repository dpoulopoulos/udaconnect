FROM node:14.8.0-alpine3.12

WORKDIR .

COPY . ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

EXPOSE 3000

CMD ["npm", "start"]
