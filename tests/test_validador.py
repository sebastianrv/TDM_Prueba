from core.generador import generar_clientes
from core.validador import validar_clientes
import json

clientes=generar_clientes(n=10, seed=42)
reporte= validar_clientes(clientes)

print(json.dumps(reporte,indent=2,ensure_ascii=False))