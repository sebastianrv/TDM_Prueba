from core.generador import generar_clientes

print("=== Generando 5 clientes ===")
clientes = generar_clientes(n=5, seed=42)
for c in clientes:
    print(c)

print("\n=== Verificando reproducibilidad con mismo seed ===")
clientes2 = generar_clientes(n=5, seed=42)
print(f"Clientes iguales: {clientes == clientes2}")

print("\n=== Verificando customer_id único ===")
ids = [c["customer_id"] for c in clientes]
print(f"IDs generados: {ids}")
print(f"IDs únicos: {len(ids) == len(set(ids))}")