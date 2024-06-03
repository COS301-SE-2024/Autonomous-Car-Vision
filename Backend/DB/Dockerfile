FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Use a command that keeps the container running
CMD ["tail", "-f", "/dev/null"]
