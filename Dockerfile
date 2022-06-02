# Use slim buster images
FROM python:3.9.13-slim-bullseye

# Make a working directory
RUN mkdir /app
WORKDIR /app

# First, copy the requirements.txt only as it helps with caching
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# Copy the source code
COPY ./api /app/api
COPY ./impacts_model /app/impacts_model

# Run Flask command
CMD ["gunicorn", "-b", "0.0.0.0:5000", "api.server:create_app()"]