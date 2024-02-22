FROM python:3

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x ./docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]