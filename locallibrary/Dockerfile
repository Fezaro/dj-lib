# DOCKERFILE

# Pull Debian Buster slim (smaller, faster build) image with 
# Python3.8 installed from DockerHub

FROM python:3.8.1-slim-buster

# Run a system update and ensure python and virtual env  is installed 
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv 
 
# For python best-practice

ENV PYTHONUNBUFFERED=1

# Create the app folder
RUN mkdir dj-lib

# Set working directory
WORKDIR /dj-lib

# Set up virtual environment

RUN python3 -m venv library

# Activate virtual environment
ENV PATH="/library/bin/activate:${PATH}"

# Copy the application code 

COPY ./ .

# Install dependencies 

RUN pip install -r requirements.txt

# Port to listen on

EXPOSE 8000

# Running the production server

ENTRYPOINT [ "python", "locallibrary/manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]