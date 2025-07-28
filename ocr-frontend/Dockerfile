# Dockerfile

# Stage 1: Build React app
FROM node:20 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html

# Remove default nginx config and replace if needed
RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d  # if you have a custom config

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
