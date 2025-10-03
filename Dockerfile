# Imagem leve + apt para instalar curl
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Lisbon \
    PYTHONPATH=/Resgate-IPT-SmartCampusCore
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /Resgate-IPT-SmartCampusCore
COPY requirements.txt /Resgate-IPT-SmartCampusCore/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /Resgate-IPT-SmartCampusCore
EXPOSE 8081
CMD ["python", "app.py"]

