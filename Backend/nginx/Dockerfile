FROM nginx:1.21.4

RUN  rm -rf /etc/nginx/http.d/default.conf

COPY http.d/app.conf /etc/nginx/http.d/app.conf

EXPOSE 80 443
