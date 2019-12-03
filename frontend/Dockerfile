FROM node:8-jessie
RUN mkdir /code
WORKDIR /code
COPY package.json /code/
RUN npm install
COPY . /code/
