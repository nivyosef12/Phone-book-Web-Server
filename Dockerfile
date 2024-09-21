FROM python:3.11-slim

ENV PYTHONPATH=/app
WORKDIR /app

RUN apt-get update

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory app contents into the container to /app
COPY ./app ./app
COPY ./tests ./tests
COPY ./.env ./.env

RUN mkdir -p /app/logs

EXPOSE 80

RUN echo $PYTHONPATH

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "180", "--workers", "4"]

