import secrets
import string
def generate_chat_id(length : int = 16):
    """
    leinght: Длина генерируемого ключа, по умолчанию 16
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_room_hash():
    return secrets.token_hex(32)

if __name__ == '__main__':
    print(generate_room_hash())