import hashlib
import os

def hasher_pass(password):
    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))  # Преобразуем строку в байтовый массив
    hashed_value = hasher.hexdigest()  # Получаем шестнадцатеричное представление хэша
    return hashed_value

