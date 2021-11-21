FROM node:16.13-alpine3.12 as build

RUN mkdir -p /AdminPage

WORKDIR /AdminPage

COPY package.json /AdminPage

RUN npm install

COPY . /AdminPage

RUN npm run ng build --configuration=production --output-path=dist

FROM nginx:1.21.4

RUN  rm -rf /etc/nginx/conf.d/default.conf

COPY conf.d/app.conf /etc/nginx/conf.d/app.conf

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*

COPY --from=build /AdminPage/dist/AdminPage /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
