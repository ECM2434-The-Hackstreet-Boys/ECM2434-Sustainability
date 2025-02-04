# Use Python 3.12 as the base image
FROM python:3.12

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/

# Create a virtual environment inside the container
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt && \
    /app/venv/bin/pip install gunicorn  # Ensure gunicorn is installed

# Copy the full project into the container
COPY . /app/

# Set environment variables
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV PATH="/app/venv/bin:$PATH"

# Expose port 8000
EXPOSE 8000

# Apply migrations (ensure this happens before CMD)
WORKDIR /app/SustainabilityApp
RUN /app/venv/bin/python manage.py migrate

# Start the Django application with Gunicorn using the virtual environment's Python
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "SustainabilityApp.wsgi:application"]
