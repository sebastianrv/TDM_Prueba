#Validación respecto a las reglas establecidas para los datos sintéticos

import re
from datetime import datetime, timedelta
from core.cedula import _validar_cedula

EDAD_MIN=18
MES_INACTIVO=6
FORMATO_NACIMIENTO="%d-%m-%Y"
FORMATO_FECHA="%d/%m/%Y %H:%M:%S"
ESTADOS_VALIDOS = {"Activo", "Inactivo"}

def _normalizar_valores(cliente: dict) -> dict:
    # Normaliza todos los valores generados
    normalizado = dict(cliente)
    for campo, valor in normalizado.items():
        if valor is not None and not isinstance(valor, str):
            normalizado[campo] = str(valor)
    return normalizado

def _fecha_valida(valor: str, formato: str) -> bool:
    # Verifica si un string tiene el formato de fecha
    try:
        datetime.strptime(valor, formato)
        return True
    except Exception:
        return False

def _schema_valido(campo: str, valor: str) -> bool:
    # Verifica si el valor cumple el formato esperado
    if campo == "customer_id":
        return (valor.startswith("Cus")
                and " " not in valor
                and valor[3:].isdigit()
                and len(valor[3:]) == 3)
    if campo == "cedula":
        return _validar_cedula(valor)
    if campo == "email":
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", valor))
    if campo == "telefono":
        return (valor.isdigit()
                and len(valor) == 10
                and valor.startswith("09"))
    if campo in ("nombre", "apellido"):
        return valor.replace("'", "").isalpha()
    if campo == "fecha_nacimiento":
        return _fecha_valida(valor, FORMATO_NACIMIENTO)
    if campo == "fecha_creacion":
        return _fecha_valida(valor, FORMATO_FECHA)
    return True

def _domain_valido(campo: str, valor: str) -> bool:
    # Verifica si el valor está dentro del dominio permitido
    if campo == "estado_cliente":
        return valor in ESTADOS_VALIDOS
    if campo == "telefono":
        return valor.startswith("09")
    if campo == "cedula":
        return valor.isdigit() and 1 <= int(valor[:2]) <= 24
    return True

def _error(campo: str, valor, detalle: str, tipo: str) -> dict:
    # Construye el diccionario de error estándar
    return {
        "campo": campo,
        "valor_erroneo": valor,
        "detalle": detalle,
        "tipo": tipo
    }

def _validar_schema(cliente: dict) -> dict | None:
    # Valida que todos los campos tengan el formato correcto
    for campo, valor in cliente.items():
        if isinstance(valor, str) and not _schema_valido(campo, valor):
            return _error(campo, valor,
                         f"Campo '{campo}' con formato inválido",
                         "schema")
    return None

def _validar_domain(cliente: dict) -> dict | None:
    # Valida que los valores estén dentro del dominio permitido
    for campo, valor in cliente.items():
        if isinstance(valor, str) and _schema_valido(campo, valor) and not _domain_valido(campo, valor):
            return _error(campo, valor,
                         f"Campo '{campo}' fuera del dominio permitido",
                         "domain")
    return None

def _validar_business(cliente: dict) -> dict | None:
    # Valida reglas de negocio funcionales
    return (validar_regla1(cliente) or
            validar_regla2(cliente) or
            validar_regla3(cliente) or
            validar_regla5(cliente))

def validar_regla1(cliente: dict) -> dict | None:
    # Valida que el cliente sea mayor de edad
    campo = "fecha_nacimiento"
    valor = cliente.get(campo)
    try:
        fecha = datetime.strptime(valor, FORMATO_NACIMIENTO)
        edad = (datetime.now() - fecha).days // 365
        if edad < EDAD_MIN:
            return _error(campo, valor,
                          f"Edad {edad} es menor a {EDAD_MIN}",
                          "business")
    except Exception:
        return _error(campo, valor,
                      "Campo fecha_nacimiento con formato inválido",
                      "schema")
    return None

def validar_regla2(cliente: dict) -> dict | None:
    # Valida inactivos con antigüedad mínima requerida
    estado = cliente.get("estado_cliente")
    if estado not in ESTADOS_VALIDOS:
        return _error("estado_cliente", estado,
                      f"estado_cliente '{estado}' fuera del dominio permitido",
                      "domain")
    if estado == "Activo":
        return None
    campo = "fecha_creacion"
    valor = cliente.get(campo)
    try:
        fecha = datetime.strptime(valor, FORMATO_FECHA)
        limite = datetime.now() - timedelta(days=MES_INACTIVO * 30)
        if fecha > limite:
            return _error(campo, valor,
                          f"Cliente Inactivo con fecha_creacion menor a {MES_INACTIVO} meses",
                          "business")
    except Exception:
        return _error(campo, valor,
                      "Campo fecha_creacion con formato inválido",
                      "schema")
    return None

def validar_regla3(cliente: dict) -> dict | None:
    # Valida formato correcto del email
    campo = "email"
    valor = cliente.get(campo)
    if valor is None:
        return _error(campo, valor, "Email es nulo", "business")
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", str(valor)):
        return _error(campo, valor,
                      f"Email '{valor}' no tiene formato válido",
                      "schema")
    return None

def validar_regla4(cliente: dict, ids_vistos: set) -> dict | None:
    # Valida que customer_id no esté duplicado
    campo = "customer_id"
    valor = cliente.get(campo)
    if valor in ids_vistos:
        return _error(campo, valor,
                      f"customer_id '{valor}' duplicado",
                      "dup")
    ids_vistos.add(valor)
    return None

def validar_regla5(cliente: dict) -> dict | None:
    # Valida campos nulos o vacíos
    nulos = [campo for campo, valor in cliente.items() if valor is None or valor == ""]
    if nulos:
        campo = nulos[0]
        return _error(campo, cliente.get(campo),
                      f"Campos nulos o vacíos: {nulos}",
                      "business")
    return None

def validar_clientes(clientes: list[dict]) -> dict:
    # Ejecuta reglas y genera reporte
    errores_por_regla = {
        "regla_1_edad": [],
        "regla_2_inactividad": [],
        "regla_3_email": [],
        "regla_4_duplicado": [],
        "regla_5_nulos": [],
    }
    errores_por_tipo = {
        "schema": [],
        "domain": [],
        "dup": [],
        "business": [],
    }
    ids_vistos = set()

    for cliente in clientes:
        cliente = _normalizar_valores(cliente)
        cid = cliente.get("customer_id")

        # Valida por tipo — dup lo maneja validar_regla4
        for tipo, resultado in [
            ("schema", _validar_schema(cliente)),
            ("domain", _validar_domain(cliente)),
            ("business", _validar_business(cliente)),
        ]:
            if resultado:
                errores_por_tipo[tipo].append({"id": cid, **resultado})

        # Valida por regla de negocio
        for regla, resultado in [
            ("regla_1_edad", validar_regla1(cliente)),
            ("regla_2_inactividad", validar_regla2(cliente)),
            ("regla_3_email", validar_regla3(cliente)),
            ("regla_4_duplicado", validar_regla4(cliente, ids_vistos)),
            ("regla_5_nulos", validar_regla5(cliente)),
        ]:
            if resultado:
                entrada = {"id": cid, **resultado}
                errores_por_regla[regla].append(entrada)
                if resultado["tipo"] == "dup":
                    errores_por_tipo["dup"].append(entrada)

    total_registros = len(clientes)
    reglas_evaluadas = sum(1 for v in errores_por_regla.values() if v)
    errores_totales = (sum(len(v) for v in errores_por_regla.values()) +
                   len(errores_por_tipo["schema"]) +
                   len(errores_por_tipo["domain"]))
    cumplimiento = round((1 - errores_totales / (total_registros * 5)) * 100, 2)

    return {
        "total_registros": total_registros,
        "reglas_evaluadas": reglas_evaluadas,
        "errores_totales": errores_totales,
        "errores_por_regla": {k: len(v) for k, v in errores_por_regla.items()},
        "porcentaje_cumplimiento": cumplimiento,
        "muestras_errores": {
            tipo: [
                {
                    "id": e["id"],
                    "campo": e["campo"],
                    "valor_erroneo": e["valor_erroneo"],
                    "detalle": e["detalle"],
                    "regla": next(
                        (r for r, errores in errores_por_regla.items()
                         if any(x["id"] == e["id"] and x["campo"] == e["campo"]
                                for x in errores)),
                        "N/A"
                    )
                }
                for e in errores[:3]
            ]
            for tipo, errores in errores_por_tipo.items() if errores
        },
    }