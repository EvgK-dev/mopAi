import os
import logging
import fitz  
from PIL import Image
import pytesseract

logger = logging.getLogger('mainapp')

def transcribe_pdf(file_path):
    text = ""
    try:
        logger.info(f"Начало обработки PDF: {file_path}")

        with fitz.open(file_path) as pdf_document:
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
                img = Image.frombytes("RGB", [image.width, image.height], image.samples)

                image_path = f"page_{page_number + 1}.png"
                img.save(image_path)
                logger.debug(f"Страница {page_number + 1} сохранена как изображение.")

                page_text = pytesseract.image_to_string(img, lang='rus+eng')
                text += page_text + "\n"

                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                        logger.debug(f"Временный файл {image_path} удалён.")
                    except Exception as e:
                        logger.warning(f"Не удалось удалить временный файл {image_path}: {str(e)}")

        logger.info(f"Обработка PDF завершена: {file_path}")
        return text

    except FileNotFoundError:
        logger.error(f"PDF-файл не найден: {file_path}")
        return "Ошибка: PDF-файл не найден."
    except Exception as e:
        logger.exception(f"Ошибка при обработке PDF-файла: {file_path} — {str(e)}")
        return f"Произошла ошибка: {str(e)}"

    finally:
        if os.path.exists(file_path):
            try:
                if os.access(file_path, os.W_OK):
                    os.remove(file_path)
                    logger.info(f"Файл PDF удалён: {file_path}")
                else:
                    logger.warning(f"Нет прав на удаление файла: {file_path}")
            except Exception as e:
                logger.error(f"Ошибка при удалении файла {file_path}: {str(e)}")
