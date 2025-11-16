import os
import uuid
from werkzeug.utils import secure_filename
from flask import request


def handle_file_upload(file_key, allowed_extensions=None):
    """
    Сохраняет файл прямо в папку news/

    Args:
        file_key (str): имя поля в форме (например 'avatar', 'attached_files')
        allowed_extensions (list): разрешенные расширения файлов

    Returns:
        tuple: (True, путь_к_файлу) или (False, ошибка)
    """
    if allowed_extensions is None:
        allowed_extensions = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt']

    # Создаем папку news если не существует
    upload_path = 'file_dir/news'
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

        # Получаем файл из запроса
    file = request.files.get(file_key)

    # Проверяем что файл выбран
    if not file or file.filename == '':
        return False, "Файл не выбран"

    # Проверяем расширение файла
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions

    if not allowed_file(file.filename):
        return False, f"Недопустимое расширение файла. Разрешены: {', '.join(allowed_extensions)}"

    # Генерируем уникальное имя и сохраняем
    try:
        file_extension = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(unique_filename)
        file.save(file_path)

        return True, file_path

    except Exception as e:
        return False, f"Ошибка при сохранении файла: {str(e)}"


def allowed_file(filename, allowed_extensions):
    """Проверяет разрешенные расширения файлов"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions