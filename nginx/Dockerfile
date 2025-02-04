# Dockerfile for Nginx

# Use official Nginx image as base
FROM nginx:latest

# Copy the custom nginx.conf into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for HTTP traffic
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]