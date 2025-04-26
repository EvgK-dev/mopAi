import os
import time
import json
import logging

from celery import shared_task
from utils.redis_client import redis_client
from mainapp.utils.audio_utils import transcribe_audio
from mainapp.utils.resource_monitor import find_least_loaded_gpu

logger = logging.getLogger('mainapp')


@shared_task
def upload_file_task(ip_address, file_path, language, accuracy):

    redis_client.set(ip_address, json.dumps({
        "upload_status": "completed",
        "transcribe_status": "pending",
        "transcribed_text": ""
    }))
    logger.info(f"[{ip_address}] аудио-файл загружен. Подготовка к обработке...")

    transcribe_audio_task.apply_async(args=[ip_address, file_path, language, accuracy])


@shared_task
def transcribe_audio_task(ip_address, file_path, language, accuracy):

    redis_client.rpush("transcription_queue", ip_address)
    logger.info(f"[{ip_address}] Добавлен в очередь транскрибации.")

    timeout = 1500  # 25 минут
    start_time = time.time()

    gpu_id = None
    try:
        while True:
            queue_list = redis_client.lrange("transcription_queue", 0, -1)
            position = queue_list.index(ip_address) + 1 if ip_address in queue_list else None

            gpu_id = find_least_loaded_gpu()
            if gpu_id is not None and position == 1:
                logger.info(f"[{ip_address}] Получен доступ к видеокарте {gpu_id}. Запускается транскрибация.")
                redis_client.lrem("transcription_queue", 0, ip_address)
                break

            if time.time() - start_time > timeout:
                logger.warning(f"[{ip_address}] Время ожидания истекло. Удаление из очереди и завершение задачи.")
                redis_client.delete(ip_address)
                redis_client.lrem("transcription_queue", 0, ip_address)
                if os.path.exists(file_path):
                    os.remove(file_path)
                return

            if position:
                redis_client.set(ip_address, json.dumps({
                    "upload_status": "completed",
                    "transcribe_status": f"Ваша очередь {position}",
                    "transcribed_text": ""
                }))

            time.sleep(10)

    except Exception as e:
        logger.exception(f"[{ip_address}] Ошибка в процессе ожидания транскрибации: {str(e)}")
        redis_client.lrem("transcription_queue", 0, ip_address)

    # Запускаем транскрибацию
    transcribed_text = transcribe_audio(ip_address, file_path, language, accuracy, gpu_id)

    redis_client.set(ip_address, json.dumps({
        "upload_status": "completed",
        "transcribe_status": "completed",
        "transcribed_text": transcribed_text
    }))
    logger.info(f"[{ip_address}] Транскрибация завершена.")
