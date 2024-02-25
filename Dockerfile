# Use an official Ubuntu base image
FROM ubuntu:latest

# Install Python, pip, Git, and other necessary tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip git zip && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first, for separate dependency resolving
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the rest of your application
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python3", "app.py"]
