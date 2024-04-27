# Use official Python image
FROM python:3.8.10

# Set the working directory
WORKDIR /LogIt

# Copy contents including dependencies to working directory
COPY . .

# Install virtualenv
RUN pip install virtualenv

# Create virtual environment
RUN virtualenv venv

# Install dependencies inside the virtual environment
RUN /LogIt/venv/bin/pip install --no-cache-dir -r web_flask/requirements.txt

# Change working directory
WORKDIR /LogIt/web_flask

# Expose the port for our app
EXPOSE 5001

# Run Flask app
CMD ["/LogIt/venv/bin/gunicorn", "-w", "4", "--bind", "0.0.0.0:5001", "app:app"]