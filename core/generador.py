import random
import unicodedata
from datetime import datetime, timedelta
from faker import Faker
from core.cedula import generar_cedula

estado= ["Activo", "Inactivo"]
vias=["Av.","Calle","Pasaje"]
edad_min= 18
edad_max= 90
fake=Faker("es")

def campo_customer(numero: int) -> str:
    return f"Cus{numero:03d}"

def campo_nacimiento(rng: random.Random) -> str:
    hoy= datetime.now()
    dias_min= edad_min*365
    dias_max= edad_max*365
    dias_atras= rng.randint(dias_min, dias_max)
    fecha= hoy - timedelta(days=dias_atras)
    return fecha.strftime("%d-%m-%Y")

def campo_telefono(rng: random.Random) -> str:
    return f"09{rng.randint(10000000,99999999)}" 

def normalizar_texto(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    ).lower().replace(" ", "")

def campo_email(nombre: str, apellido: str, rng: random.Random) -> str:
    n=normalizar_texto(nombre)
    a=normalizar_texto(apellido)
    formatos= [
        f"{n}.{a}",
        f"{a}.{n}",
        f"{n}_{a}",
        f"{n[0]}.{a}",
        f"{n}{a}",        
    ]
    return f"{rng.choice(formatos)}@{fake.free_email_domain()}"

def campo_direccion(rng: random.Random) -> str:
    tipo1= rng.choice(vias)
    tipo2= rng.choice(vias)
    calle1=fake.last_name()
    calle2=fake.last_name()
    ciudad=fake.city()
    return f"{tipo1} {calle1} y {tipo2} {calle2}, {ciudad}"

def campo_creacion(rng: random.Random, estado: str) -> datetime:
    if estado == "Inactivo":
        regla= rng.randint(183,730)
        return datetime.now() - timedelta(days=regla)
    return datetime.now()

def generar_cliente(numero: int, rng: random.Random) -> dict:
    nombre=fake.first_name()
    apellido=fake.last_name()
    estados=rng.choice(estado)
    fecha_creacion=campo_creacion(rng,estados)

    return{
        "customer_id": campo_customer(numero),
        "nombre": nombre,
        "apellido": apellido,
        "cedula": generar_cedula(),
        "fecha_nacimiento": campo_nacimiento(rng),
        "email": campo_email(nombre,apellido,rng),
        "direccion": campo_direccion(rng),
        "telefono": campo_telefono(rng),
        "fecha_creacion": fecha_creacion.strftime("%d/%m/%Y %H:%M:%S"),
        "estado_cliente": estados,
    }

def generar_clientes(n:int, seed:int) ->list[dict]:
    rng=random.Random(seed)
    Faker.seed(seed)
    return [generar_cliente(i+1, rng) for i in range(n)]