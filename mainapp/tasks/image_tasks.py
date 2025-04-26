import json
import time
import logging

from celery import shared_task
from utils.redis_client import redis_client
from mainapp.utils.image_utils import transcribe_photo
from mainapp.utils.resource_monitor import check_cpu_usage

logger = logging.getLogger('mainapp')

@shared_task
def upload_img_task(ip_address, file_path):

    redis_client.set(ip_address, json.dumps({
        "upload_status": "completed",
        "transcribe_status": "pending",
        "transcribed_text": ""
    }))
    logger.info(f"[{ip_address}] изображение загружено. Подготовка к обработке...")

    extract_photo_task.apply_async(args=[ip_address, file_path])


@shared_task
def extract_photo_task(ip_address, file_path):
    logger.info(f"[{ip_address}] Начата обработка изображения.")

    max_retries = 5
    retry_interval = 10

    for attempt in range(max_retries):
        cpu_load = check_cpu_usage(interval=1)

        if cpu_load is not None and cpu_load < 80:
            redis_client.set(ip_address, json.dumps({
                "upload_status": "completed",
                "transcribe_status": f"✅ CPU загружен на {cpu_load}%. Начинаем обработку файла...",
                "transcribed_text": ""
            }))
            logger.info(f"[{ip_address}] CPU загружен на {cpu_load}%. Обработка начинается.")
            break
        else:
            redis_client.set(ip_address, json.dumps({
                "upload_status": "completed",
                "transcribe_status": f"⚠️ CPU загружен на {cpu_load}%. Ожидание {retry_interval} секунд...",
                "transcribed_text": ""
            }))
            logger.warning(f"[{ip_address}] CPU загружен на {cpu_load}%. Ожидаем {retry_interval} секунд.")
            time.sleep(retry_interval)
    else:
        redis_client.set(ip_address, json.dumps({
            "upload_status": "completed",
            "transcribe_status": "completed",
            "transcribed_text": "❌ CPU загружен слишком долго. Нажмите кнопку 'очистить' и попробуйте позже."
        }))
        logger.error(f"[{ip_address}] CPU был загружен слишком долго. Попробуйте позже.")
        return

    transcribed_text = transcribe_photo(file_path)
    redis_client.set(ip_address, json.dumps({
        "upload_status": "completed",
        "transcribe_status": "completed",
        "transcribed_text": transcribed_text
    }))
    logger.info(f"[{ip_address}] Обработка изображения завершена.")
