FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose the port the app runs on (matching the Flask default)
EXPOSE 8000

# Define the command to run the application using Gunicorn
# 'server:app' refers to the 'app' object inside 'server.py'
ENTRYPOINT ["python3"]
CMD ["app.py"]
