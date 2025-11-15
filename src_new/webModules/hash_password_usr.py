import hashlib
import os

def hasher_pass(password, salt=None):
    """
    Хеширование пароля с использованием соли для повышения безопасности.
    Если соль не передана, генерируется новая.
    """
    if salt is None:
        salt = os.urandom(32)
    
    # Используем PBKDF2 для более безопасного хеширования
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Возвращаем соль + хеш в hex формате
    return salt.hex() + hashed.hex()

def verify_password(password, hashed_password):
    """
    Проверка пароля против хешированного значения.
    """
    try:
        # Извлекаем соль (первые 64 символа - это 32 байта в hex)
        salt = bytes.fromhex(hashed_password[:64])
        stored_hash = hashed_password[64:]
        
        # Хешируем введенный пароль с той же солью
        new_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()
        
        return new_hash == stored_hash
    except Exception as e:
        print(f"Ошибка проверки пароля: {e}")
        return False