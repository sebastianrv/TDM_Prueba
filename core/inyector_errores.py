import random
import copy
from datetime import datetime

tipos_error = ["schema", "domain", "dup", "business"]


def generar_errores(rng: random.Random) -> dict:

    fecha_actual = datetime.now().year

    return {
        "schema": [
            # customer_id
            {"customer_id": f"cuss{rng.randint(1,999):03d}"},
            {"customer_id": f"CUS {rng.randint(1,999):03d}"},
            # cedula
            {"cedula": "".join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + str(rng.randint(10000, 99999))},
            {"cedula": str(rng.randint(100000, 999999))},
            {"cedula": str(rng.randint(10000000000, 99999999999))},
            # nombre
            {"nombre": rng.randint(1000, 9999)},
            # fecha_nacimiento
            {"fecha_nacimiento": f"{rng.randint(1990,2000)}/{rng.randint(1,12):02d}/{rng.randint(1,28):02d}"},
            {"fecha_nacimiento": rng.choice(["ayer", "mañana"])},
            {"fecha_nacimiento": f"{rng.randint(1,28):02d}-{rng.randint(1,12):02d}-{str(rng.randint(50,99))}"},
            # email
            {"email": rng.randint(1000, 9999)},
            {"email": f"correo{rng.randint(1,999)}sin_arroba.com"},
            # telefono
            {"telefono": "".join(rng.choices("abcxyz-", k=9))},
            {"telefono": str(rng.randint(100000, 999999))},
            {"telefono": str(rng.randint(100000000000, 999999999999))},
            # fecha_creacion
            {"fecha_creacion": f"{rng.randint(2020,2026)}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}"},
            {"fecha_creacion": rng.choice(["ahora", "hoy"])},
            # estado_cliente
            {"estado_cliente": rng.randint(0, 9)},
        ],
        "domain": [
            # customer_id — no aplica domain
            # cedula
            {"cedula": f"00{rng.randint(1000000, 9999999)}{rng.randint(0,9)}"},
            {"cedula": f"99{rng.randint(1000000, 9999999)}{rng.randint(0,9)}"},
            {"cedula": f"25{rng.randint(1000000, 9999999)}{rng.randint(0,9)}"},
            {"cedula": "1710034060"},
            # email
            {"email": f"usuario{rng.randint(1,999)}@dominioxxx.zzz"},
            # telefono
            {"telefono": f"06{rng.randint(10000000, 99999999)}"},
            {"telefono": f"07{rng.randint(10000000, 99999999)}"},
            {"telefono": f"08{rng.randint(10000000, 99999999)}"},
            # estado_cliente
            {"estado_cliente": rng.choice(["Pendiente", "Suspendido", "Eliminado", "Bloqueado"])},
            {"estado_cliente": ""},
        ],
        "business": [
            # Regla 1: edad menor a 18
            {"fecha_nacimiento": datetime.now().strftime("%d-%m-%Y")},
            {"fecha_nacimiento": f"01-01-{fecha_actual - rng.randint(1, 17)}"},
            # Regla 2: inactivo con fecha reciente
            {"estado_cliente": "Inactivo", "fecha_creacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S")},
            # Regla 5: nulos
            {"customer_id": None},
            {"nombre": None},
            {"apellido": None},
            {"cedula": None},
            {"email": None},
            {"telefono": None},
        ],
    }


def inyectar_errores( clientes: list[dict], error_rate: float, seed: int) -> list[dict]:

    if not clientes:
        raise ValueError("La lista de clientes no puede estar vacía")
    if not (0 < error_rate <= 1):
        raise ValueError(f"error_rate debe estar entre 0 y 1, recibido: {error_rate}")

    rng = random.Random(seed)
    resultado = copy.deepcopy(clientes)
    errores = generar_errores(rng)

    n_errores = max(1, round(len(resultado) * error_rate))
    n_errores = min(n_errores, len(resultado))

    indices = rng.sample(range(len(resultado)), n_errores)
    ids_disponibles= [c["customer_id"] for c in resultado]

    for idx in indices:
        tipo = rng.choice(tipos_error)
        cliente = resultado[idx]

        if tipo == "dup":
            id_duplicado=rng.choice([
                id for id in ids_disponibles
                if id!= cliente["customer_id"]
            ])
            cliente["customer_id"] = id_duplicado
        else:
            mutacion = rng.choice(errores[tipo])
            cliente.update(mutacion)

        cliente["tipo_error"] = tipo

    return resultado