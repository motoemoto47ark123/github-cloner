# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Install python, pip, git, and zip
RUN apt-get update && \
    apt-get install -y python3 python3-pip git zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run app.py when the container launches
CMD ["flask", "run"]
