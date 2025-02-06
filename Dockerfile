# Use Python 3.12 as the base image
FROM python:3.12

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/

RUN python -m pip install --upgrade pip
# Install dependencies
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copy the full project into the container
COPY . /app/

# Set environment variables
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

#RUN python apps/manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Apply migrations (ensure this happens before CMD)
WORKDIR /app/SustainabilityApp


# Start the Django application with Gunicorn using the virtual environment's Python

#CMD ["python", "-m", "SustainabililityApp/manage.py", "collectstatic", "--noinput", "&&", "gunicorn", "--bind", "0.0.0.0:8000", "apps.wsgi:application"]
CMD python manage.py collectstatic --noinput; gunicorn --bind 0.0.0.0:8000 SustainabilityApp.wsgi:application
