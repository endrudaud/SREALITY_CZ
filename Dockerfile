# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade selenium

# Download and install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.34.0-linux64.tar.gz
RUN rm geckodriver-v0.34.0-linux64.tar.gz
RUN mv geckodriver /usr/local/bin/

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

# Install Firefox and its dependencies
RUN apt-get update && apt-get install -y firefox-esr
RUN firefox-esr --version

# Copy the app.py file to the container
COPY app.py .
COPY helpers.py .

# Set the entrypoint command to run app.py
CMD ["python", "app.py"]