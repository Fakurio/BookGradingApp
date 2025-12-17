FROM node:24.2.0 as base
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

ARG VITE_SERVER_HOST
ENV VITE_SERVER_HOST=$VITE_SERVER_HOST
RUN npm run build

FROM nginx:1.21.1
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=base /app/dist .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]