# /backend/Dockerfile
FROM python:3.11

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

# Add a startup script that waits for DB, seeds, then runs app
CMD ["sh", "-c", "until nc -z db 5432; do echo '⏳ Waiting for Postgres...'; sleep 1; done && echo '✅ DB is ready' && python seed.py && python seed_badges.py && python run.py"]
