import random
import string

def generar_codigo_unico(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
