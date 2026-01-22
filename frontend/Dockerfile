# Stage 1: Build
FROM node:20-alpine as build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production=false

# Copy source code
COPY . .

# Build arguments for environment variables
ARG VITE_DEFAULT_SERVICE_URL
ENV VITE_DEFAULT_SERVICE_URL=$VITE_DEFAULT_SERVICE_URL

# Build the application
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Create nginx config template
RUN echo 'server { \
    listen $PORT; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf.template

# Copy startup script
COPY <<'EOF' /docker-entrypoint.sh
#!/bin/sh
set -e
envsubst '$$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
exec nginx -g 'daemon off;'
EOF

RUN chmod +x /docker-entrypoint.sh

EXPOSE $PORT

CMD ["/docker-entrypoint.sh"]