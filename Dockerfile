FROM python:3.9.4-slim-buster

# Upgrade pip
RUN pip install --upgrade pip

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install project dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Set work directory
WORKDIR /code

# listen on this port
EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
