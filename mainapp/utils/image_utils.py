import os
import logging
from PIL import Image
import pytesseract

logger = logging.getLogger('mainapp')

def transcribe_photo(file_path):
    try:
        logger.info(f"Начало обработки изображения: {file_path}")

        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang='rus+eng')

        logger.info(f"Извлечение текста завершено: {file_path}")
        return text

    except FileNotFoundError:
        logger.error(f"Файл изображения не найден: {file_path}")
        return "Ошибка: Файл изображения не найден."
    except Exception as e:
        logger.exception(f"Ошибка при извлечении текста из изображения: {file_path} — {str(e)}")
        return f"Произошла ошибка: {str(e)}"
    finally:
        if os.path.exists(file_path):
            try:
                if os.access(file_path, os.W_OK):
                    os.remove(file_path)
                    logger.info(f"Файл изображения удалён: {file_path}")
                else:
                    logger.warning(f"Нет прав на удаление файла: {file_path}")
            except Exception as e:
                logger.exception(f"Ошибка при удалении файла: {file_path} — {str(e)}")
