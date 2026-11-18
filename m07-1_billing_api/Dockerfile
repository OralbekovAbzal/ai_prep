from python:3.15-slim
env PYTHONUNBUFFERED=1
workdir /app
copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt
copy . .
cmd ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]