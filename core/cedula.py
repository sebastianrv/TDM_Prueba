#Código para la generación y validación de cédulas ecuatorianas sintéticas
import random
from typing import Optional

LONGITUD = 10
PROVINCIA_MIN = 1
PROVINCIA_MAX = 24
PROVINCIA_EXTRANJEROS = 30
MODULO = 10

def _calcular_verificador (cedula_parcial: str) -> int:
    #Calcula el dígito verificador de la cédula usando el módulo 10
    total = 0
    for i in range(9):
        coeficiente = 2 if i % 2 == 0 else 1
        digito = int(cedula_parcial[i]) * coeficiente
        if digito >= MODULO:
            digito -= (MODULO - 1)
        total += digito
    return (MODULO - (total % MODULO)) % MODULO

def _validar_cedula(cedula: str) -> bool:
    #Valida formato de la cédula
    if not isinstance(cedula, str):
        return False
    if not cedula.isdigit():
        return False
    if len(cedula) != LONGITUD:
        return False

    provincia = int(cedula[:2])
    if not (PROVINCIA_MIN <= provincia <= PROVINCIA_MAX or
            provincia == PROVINCIA_EXTRANJEROS):
        return False
    if int(cedula[2]) > 5:
        return False

    return _calcular_verificador(cedula) == int(cedula[9])   

def generar_cedula(seed: Optional[int]= None) ->str:
    #Genera una cédula ecuatoriana sintética válida
    rng = random.Random(seed)

    while True:
        provincia = str(rng.randint(PROVINCIA_MIN, PROVINCIA_MAX)).zfill(2)
        tercer_digito = str(rng.randint(0, 5))
        resto = [str(rng.randint(0, 9)) for _ in range(6)]

        cedula_parcial = provincia + tercer_digito + "".join(resto)
        verificador = _calcular_verificador(cedula_parcial)
        cedula = cedula_parcial + str(verificador)

        if _validar_cedula(cedula):
            return cedula
    