FROM python:3.12-slim
RUN pip install --no-cache-dir flask==3.0.3
WORKDIR /app
COPY fixed_a.py fixed_b.py fixed_c.py logic_check.py /app/
CMD ["python", "logic_check.py"]
