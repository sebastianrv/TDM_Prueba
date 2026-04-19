import random
from typing import Optional

longitud=10
provincia_min=1
provincia_max=24
modulo=10

def calcular_verificador (cedula_parcial: str) -> int:
    total=0
    for i in range(9):
        coeficiente= 2 if i % 2 == 0 else 1
        digito= int(cedula_parcial[i]) * coeficiente
        if digito >= modulo:
            digito-=(modulo-1)
        total += digito
    return (modulo-(total%modulo))%modulo

def validar_cedula(cedula: str) -> bool:
    if not isinstance(cedula, str):
        return False
    if not cedula.isdigit():
        return False    
    if len(cedula) != longitud:
        return False
    if not (provincia_min<= int(cedula[:2])<= provincia_max):
        return False
    if int(cedula[2])>5:
        return False
    return calcular_verificador(cedula)==int(cedula[9])    

def generar_cedula(seed: Optional[int]= None) ->str:
    rng= random.Random(seed)

    while True:
        provincia= str(rng.randint(provincia_min, provincia_max)).zfill(2)
        tercer_digito= str(rng.randint(0,5))
        resto=[str(rng.randint(0,9)) for _ in range (6)]

        cedula_parcial= provincia + tercer_digito + "".join(resto)
        verificador= calcular_verificador(cedula_parcial)
        cedula= cedula_parcial + str(verificador)

        if validar_cedula(cedula):
            return cedula
    