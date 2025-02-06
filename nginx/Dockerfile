# Dockerfile for Nginx

# Use official Nginx image as base
FROM nginx:latest

# Copy the custom nginx.conf into the container
COPY nginx.conf /etc/nginx/nginx.conf
COPY ./certs/fullchain.pem /etc/ssl/certs/fullchain.pem
COPY ./certs/privkey.pem /etc/ssl/private/privkey.pem


# Expose port 80 for HTTP traffic
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]