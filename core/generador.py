#Genera datos de clientes sintéticos

import random
import unicodedata
from datetime import datetime, timedelta
from faker import Faker
from core.cedula import generar_cedula

ESTADOS = ["Activo", "Inactivo"]
VIAS = ["Av.", "Calle", "Pasaje"]
EDAD_MIN = 18
EDAD_MAX = 90

fake = Faker("es")


def campo_customer(numero: int) -> str:
    # Genera ID cliente
    return f"Cus{numero:03d}"


def campo_nacimiento(rng: random.Random) -> str:
    # Genera fecha de nacimiento válida entre 18 y 90 años
    hoy = datetime.now()
    dias_min = EDAD_MIN * 365
    dias_max = EDAD_MAX * 365
    dias_atras = rng.randint(dias_min, dias_max)
    fecha = hoy - timedelta(days=dias_atras)
    return fecha.strftime("%d-%m-%Y")


def campo_telefono(rng: random.Random) -> str:
    # Genera teléfono móvil
    return f"09{rng.randint(10000000, 99999999)}"


def normalizar_texto(texto: str) -> str:
    # Quita tildes, espacios y pasa a minúscula
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    ).lower().replace(" ", "")


def campo_email(nombre: str, apellido: str, rng: random.Random) -> str:
    # Genera email con nombre y apellido
    n = normalizar_texto(nombre)
    a = normalizar_texto(apellido)

    formatos = [
        f"{n}.{a}",
        f"{a}.{n}",
        f"{n}_{a}",
        f"{n[0]}.{a}",
        f"{n}{a}",
    ]

    return f"{rng.choice(formatos)}@{fake.free_email_domain()}"


def campo_direccion(rng: random.Random) -> str:
    # Genera dirección ficticia aleatoria
    tipo1 = rng.choice(VIAS)
    tipo2 = rng.choice(VIAS)
    calle1 = fake.last_name()
    calle2 = fake.last_name()
    ciudad = fake.city()

    return f"{tipo1} {calle1} y {tipo2} {calle2}, {ciudad}"


def campo_creacion(rng: random.Random, estado: str) -> datetime:
    # Asigna fecha según estado cliente
    if estado == "Inactivo":
        regla = rng.randint(183, 730)
        return datetime.now() - timedelta(days=regla)

    return datetime.now()


def generar_cliente(numero: int, rng: random.Random) -> dict:
    # Construye cliente con datos sintéticos
    nombre = fake.first_name().split()[0]
    apellido = fake.last_name().split()[0]
    estados = rng.choice(ESTADOS)
    fecha_creacion = campo_creacion(rng, estados)

    return {
        "customer_id": campo_customer(numero),
        "nombre": nombre,
        "apellido": apellido,
        "cedula": generar_cedula(),
        "fecha_nacimiento": campo_nacimiento(rng),
        "email": campo_email(nombre, apellido, rng),
        "direccion": campo_direccion(rng),
        "telefono": campo_telefono(rng),
        "fecha_creacion": fecha_creacion.strftime("%d/%m/%Y %H:%M:%S"),
        "estado_cliente": estados,
    }


def generar_clientes(n: int, seed: int) -> list[dict]:
    # Genera lista de clientes
    rng = random.Random(seed)
    Faker.seed(seed)

    return [generar_cliente(i + 1, rng) for i in range(n)]