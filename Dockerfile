FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY hello.py test_hello.py monitor.py pytest.ini ./
CMD ["python", "hello.py"]
