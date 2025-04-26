import os
import logging
from datetime import datetime
from django.conf import settings
from faster_whisper import WhisperModel

logger = logging.getLogger('mainapp')

def transcribe_audio(ip_address, file_path, language, accuracy, gpu_id):
    try:
        logger.info(f"Начало транскрибации: {file_path}, IP: {ip_address}, язык: {language}, точность: {accuracy}, GPU: {gpu_id}")

        beam_size = {1: 1, 2: 5, 3: 10}.get(accuracy, 5)
        device = "cuda" if gpu_id is not None else "cpu"
        compute_type = "float32" if device == "cuda" else "float32"
        model_path = os.path.join(settings.BASE_DIR, 'models', 'whisper', 'medium')
        device_index = gpu_id if gpu_id is not None else 0

        model = WhisperModel(model_path, device=device, compute_type=compute_type, device_index=device_index)

        if language == "auto":
            _, info = model.transcribe(file_path, beam_size=beam_size)
            language = info.language

        segments, info = model.transcribe(file_path, beam_size=beam_size, ip=ip_address, language=language)
        segments = list(segments)

        format_time = lambda sec: f"{sec // 60:02d}:{sec % 60:02d}"
        formatted_text = []
        plain_text = []

        for segment in segments:
            start = format_time(int(segment.start))
            end = format_time(int(segment.end))
            formatted_text.append(f"[{start} - {end}] {segment.text}")
            plain_text.append(segment.text)
        
        logger.info(f"Транскрибация завершена: {file_path}")
        return "\n".join(formatted_text) + "\n\n" + "\n".join(plain_text)

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return "Ошибка: Аудиофайл не найден."
    except Exception as e:
        logger.exception(f"Ошибка транскрибации: {file_path} — {str(e)}")
        return f"Ошибка транскрибации: {str(e)}"
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Файл удалён: {file_path}")
            except Exception as e:
                logger.exception(f"Ошибка при удалении файла: {file_path} — {str(e)}")
