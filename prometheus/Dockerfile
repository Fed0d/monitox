FROM python:3.12-slim

WORKDIR /prometheus

COPY . .
COPY prometheus.yml /etc/prometheus/prometheus.yml

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run_prometheus.py"]
