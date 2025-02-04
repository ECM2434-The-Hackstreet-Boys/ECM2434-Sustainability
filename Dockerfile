# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the full project into the container
COPY . /app/

# Set environment variables
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

# Expose port 8000
EXPOSE 8000

# Change working directory to where manage.py is
WORKDIR /app/SustainabilityApp

# Apply migrations
RUN python manage.py migrate

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
