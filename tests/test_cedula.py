from core.cedula import generar_cedula, _validar_cedula

print("=== Generando cédulas válidas ===")
for i in range(5):
    cedula = generar_cedula()
    print(f"Cédula: {cedula} | Válida: {_validar_cedula(cedula)}")

print("\n=== Probando cédulas inválidas ===")
invalidas = [
    "1234567890",
    "9000034065",
    "1790034065",
    "1710036",
    "1710034ABC",
]
for cedula in invalidas:
    print(f"Cédula: {cedula} | Válida: {_validar_cedula(cedula)}")

print("\n=== Probando reproducibilidad con seed ===")
for _ in range(3):
    print(f"Cédula con seed=42: {generar_cedula(seed=42)}")