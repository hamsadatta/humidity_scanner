# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the publisher and subscriber directories into the container at /app
COPY publisher /app/publisher
COPY subscriber /app/subscriber

# Install any needed packages
RUN pip install paho-mqtt requests

# Set the entrypoint to dynamically switch between publisher and subscriber
ENTRYPOINT ["python"]
CMD ["${SCRIPT_PATH}"]
