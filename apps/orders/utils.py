import datetime
import random


def generar_numero_unico():
    ahora = datetime.datetime.now()
    timestamp = ahora.strftime('%Y%m%d%H%M%S')  # Ej: 20250616164901
    aleatorio = random.randint(1000, 9999)
    return f"ORD{timestamp}{aleatorio}"