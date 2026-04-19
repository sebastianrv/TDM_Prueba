import re
from datetime import datetime, timedelta

edad_min=18
mes_inactivo=6
formato_nacimiento="%d-%m-%Y"
formato_fecha="%d/%m/%Y %H:%M:%S"

def validar_regla1 (cliente: dict) ->str | None:
    try:
        fecha = datetime.strptime(cliente["fecha_nacimiento"], formato_nacimiento)
        edad = (datetime.now() - fecha).days // 365
        if edad < edad_min:
            return f"Edad {edad} es menor a {edad_min}"
    except Exception:
        return "Campo fecha_nacimiento con formato inválido"
    return None

def validar_regla2 (cliente: dict) -> str | None:
    if cliente["estado_cliente"] != "Inactivo":
        return None
    try:
        fecha = datetime.strptime(cliente["fecha_creacion"], formato_fecha)
        limite = datetime.now() - timedelta(days=mes_inactivo * 30)
        if fecha > limite:
            return f"Cliente Inactivo con fecha_creacion menor a {mes_inactivo} meses"
    except Exception:
        return "Campo fecha_creacion con formato inválido"
    return None

def validar_regla3 (cliente: dict) -> str | None:
    """Regla 3: Email con formato válido."""
    email = cliente.get("email", "")
    if email is None:
        return "Email es nulo"
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
        return f"Email '{email}' no tiene formato válido"
    return None

def validar_regla4 (cliente: dict, ids_vistos: set) -> str | None:
    cid = cliente.get("customer_id")
    if cid in ids_vistos:
        return f"customer_id '{cid}' duplicado"
    ids_vistos.add(cid)
    return None

def validar_regla5 (cliente: dict) -> str | None:
    """Regla 5: No valores nulos."""
    nulos = [campo for campo, valor in cliente.items() if valor is None or valor == ""]
    if nulos:
        return f"Campos nulos o vacíos: {nulos}"
    return None

def validar_clientes (clientes: list[dict]) -> dict:
    errores = {
        "regla_1_edad": [],
        "regla_2_inactividad": [],
        "regla_3_email": [],
        "regla_4_duplicado": [],
        "regla_5_nulos": [],
    }

    ids_vistos = set()

    for cliente in clientes:
        cid = cliente.get("customer_id")

        r1 = validar_regla1(cliente)
        r2 = validar_regla2(cliente)
        r3 = validar_regla3(cliente)
        r4 = validar_regla4(cliente, ids_vistos)
        r5 = validar_regla5(cliente)

        if r1: errores["regla_1_edad"].append({"id": cid, "detalle": r1})
        if r2: errores["regla_2_inactividad"].append({"id": cid, "detalle": r2})
        if r3: errores["regla_3_email"].append({"id": cid, "detalle": r3})
        if r4: errores["regla_4_duplicado"].append({"id": cid, "detalle": r4})
        if r5: errores["regla_5_nulos"].append({"id": cid, "detalle": r5})

    total_registros = len(clientes)
    errores_totales = sum(len(v) for v in errores.values())
    cumplimiento = round((1 - errores_totales / (total_registros * 5)) * 100, 2)

    return {
        "total_registros": total_registros,
        "reglas_evaluadas": 5,
        "errores_totales": errores_totales,
        "errores_por_regla": {k: len(v) for k, v in errores.items()},
        "porcentaje_cumplimiento": cumplimiento,
        "muestras_errores": {k: v[:3] for k, v in errores.items() if v},
    }