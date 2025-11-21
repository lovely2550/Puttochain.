import logging.config
import json
from datetime import datetime

# กำหนดรูปแบบ Structured Log (JSON)
class JsonFormatter(logging.Formatter):
    """
    Formatter ที่แปลง Log Record ให้อยู่ในรูปแบบ JSON
    เพื่อความสะดวกในการค้นหาและวิเคราะห์ด้วยเครื่องมือ Monitoring (เช่น ELK, Grafana Loki)
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "message": record.getMessage(),
        }
        
        # เพิ่ม extra data (เช่น transaction_id, user_id) ที่ส่งมากับ log call
        if hasattr(record, 'extra_data'):
            log_record.update(record.extra_data)
            
        # เพิ่ม traceback สำหรับ Error และ Critical
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
            
        return json.dumps(log_record, ensure_ascii=False)

def setup_logging():
    """
    ตั้งค่า Logging Configuration หลัก
    """
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': JsonFormatter,
            },
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'default': {
                'formatter': 'json',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'puttochain': {
                'handlers': ['default'],
                'level': 'INFO', # สำหรับ Production ควรเป็น INFO
                'propagate': False
            },
            'uvicorn': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }
    
    logging.config.dictConfig(LOGGING_CONFIG)
    
# Logger หลักที่โมดูลอื่นจะเรียกใช้
import logging
logger = logging.getLogger('puttochain')
