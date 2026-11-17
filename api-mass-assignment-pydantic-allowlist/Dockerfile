FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY vulnerable_app.py fixed_app.py test_gate.py ./
EXPOSE 8000
CMD ["uvicorn", "fixed_app:app", "--host", "0.0.0.0", "--port", "8000"]
