# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Step 4: Copy the current directory contents into the container at /app
COPY . /app

# Step 5: Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose the port that Flask will run on
EXPOSE 5000

# Step 7: Set the environment variable for Flask
ENV FLASK_APP=main.py

# Step 8: Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
