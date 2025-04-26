import logging
import GPUtil
import psutil

logger = logging.getLogger('mainapp')

def find_least_loaded_gpu() -> int | None:
    gpus = GPUtil.getGPUs()
    if not gpus:
        logger.warning("Видеокарты не обнаружены.")
        raise Exception("Видеокарты не обнаружены")

    for gpu in gpus:
        logger.debug(f"GPU {gpu.id}: {gpu.name}, Загрузка памяти: {gpu.memoryUtil * 100:.2f}%")

    available_gpus = [gpu for gpu in gpus if gpu.memoryUtil < 0.5]

    if available_gpus:
        gpu = min(available_gpus, key=lambda x: x.memoryUtil)
        logger.info(f"Выбрана видеокарта: GPU {gpu.id} с загрузкой памяти {gpu.memoryUtil * 100:.2f}%")
        return gpu.id

    logger.warning("Все видеокарты слишком загружены.")
    return None


def check_cpu_usage(interval: int = 1) -> float | None:
    try:
        usage = psutil.cpu_percent(interval=interval)
        logger.debug(f"Загрузка CPU: {usage:.2f}%")
        return usage
    except Exception as e:
        logger.error(f"Ошибка при проверке загрузки CPU: {str(e)}")
        return None
