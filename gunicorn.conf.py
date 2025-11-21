# gunicorn.conf.py
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8000'
# เพิ่ม timeout ถ้า API มีการทำงานนาน (เช่น การ Mint Token อาจใช้เวลา)
# timeout = 60
