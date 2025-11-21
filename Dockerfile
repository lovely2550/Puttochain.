# ใช้ Python เวอร์ชันที่เหมาะสม
FROM python:3.10-slim

# ตั้งค่า Working Directory ภายใน Container
WORKDIR /app

# คัดลอกไฟล์ dependencies และติดตั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดที่เหลือ
COPY . .

# กำหนด Environment Variable ที่จำเป็น (สำหรับ Production)
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# รัน uvicorn Server
# ใช้ gunicorn ร่วมกับ uvicorn worker สำหรับ Production Performance
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
