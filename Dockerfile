# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the app, using an argument to specify the script
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
