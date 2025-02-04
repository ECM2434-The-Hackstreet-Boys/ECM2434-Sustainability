# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt /app/

# Create a virtual environment inside the container
RUN python -m venv /app/venv

# Upgrade pip inside the virtual environment
RUN /app/venv/bin/pip install --upgrade pip

# Install dependencies into the virtual environment
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the full project into the container
COPY . /app/

# Set environment variables
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

# Expose port 8000
EXPOSE 8000

# Change working directory to where manage.py is
WORKDIR /app/SustainabilityApp

# Apply migrations
RUN /app/venv/bin/python manage.py migrate

# Start the Django application with Gunicorn using the virtual environment's Python
CMD ["/app/venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "SustainabilityApp.wsgi:application"]
