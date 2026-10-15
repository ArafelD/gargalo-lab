FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd -m lab
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY gargalo_lab ./gargalo_lab
COPY tests ./tests
USER lab
CMD ["python", "-m", "gargalo_lab", "all", "--out", "/app/output"]
