# Use Python 3.12 as the base image
FROM python:3.12
# Set the working directory within the container
WORKDIR /app/backend
# Copy the requirements.txt file to the container
COPY requirements.txt /app/backend
# Install Python dependencies using pip
RUN pip install -r requirements.txt
# Copy the entire application code to the container
COPY . /app/backend
# Expose port 8000 to the outside world
EXPOSE 8000
# Apply migrations to set up the database (SQLite in this case)
RUN python manage.py migrate
# Run the Django application
CMD python /app/backend/manage.py runserver 0.0.0.0:8000