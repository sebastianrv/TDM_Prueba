import yaml
import json
from core.generador import generar_clientes
from core.inyector_errores import inyectar_errores
from core.validador import validar_clientes

with open("configuracion/global.yaml") as f:
    config = yaml.safe_load(f)

# Generar clientes limpios
clientes = generar_clientes(n=config["registros"], seed=config["seed"])

# Inyectar errores
clientes_con_errores = inyectar_errores(
    clientes,
    error_rate=config["error_rate"],
    seed=config["seed"]
)

# Validar
reporte = validar_clientes(clientes_con_errores)

print(json.dumps(reporte, indent=2, ensure_ascii=False))

# Verificar cuántos errores se inyectaron
errores = [c for c in clientes_con_errores if "_inyectado" in c]
print(f"\nErrores inyectados: {len(errores)}")