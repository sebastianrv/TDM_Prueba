# TDM Data Sintética

Prueba de Test Data Management para generación, inyección de errores y validación determinística de datos sintéticos.

---

## Estructura

```
tdm-data-sintetica/
├── configuracion/
│   └── global.yaml          # Parámetros globales
├── core/
│   ├── generador.py         # Generación de clientes sintéticos
│   ├── validador.py         # Validación de reglas de negocio
│   ├── inyector_errores.py  # Generar inyección de errores 
│   └── cedula.py            # Generar una cedula ecuatoriana válida
├── output/
│   ├── archivos/*           # Datasets generados (CSV/JSON)
│   ├── reportes/*           # Reportes de validación
├── tests/
│   ├── test_cedula.py       # Prueba unitaria de del código que genera la cedula
│   ├── test_generador.py    # Prueba unitaria del código que genera los datasets
│   ├── test_inyector.py     # Prueba unitaria para inyectar datos erróneos
│   ├── test_validador.py    # Prueba unitaria para verificar el código de las validaciones
├── main.py                  # Orquestador principal
└── requerimientos.txt       # Dependencias
```

---

## Reglas validadas

| Regla | Descripción |
|---|---|
| 1 | Edad >= 18 años |
| 2 | Si Inactivo, fecha_creacion >= 6 meses |
| 3 | Email con formato válido |
| 4 | customer_id único |
| 5 | No valores nulos |

---

## Tipos de error inyectados

| Tipo | Descripción |
|---|---|
| schema | Violación de tipo de dato o formato |
| domain | Valor fuera del conjunto permitido |
| dup | customer_id duplicado |
| business | Violación de regla de negocio |

---

## Algoritmo cédula ecuatoriana

Implementa el algoritmo Módulo 10 estándar:
- Dígitos 1-2: código de provincia (01-24)
- Dígito 3: menor a 6 (0-5)
- Dígito 10: verificador calculado con coeficientes alternados 2,1
- Fuente: práctica estándar verificable en registrocivil.gob.ec

---

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd tdm-data-sintetica
```

### 2. Instalar dependencias
```bash
pip install -r requerimientos.txt
```

### 3. Verificar instalación
```bash
python -c "import faker, pandas, yaml; print('Dependencias OK')"
```

---

## Uso

```bash
# Con valores por defecto del yaml
python main.py

# Con parámetros personalizados
python main.py --n 300 --seed 45
python main.py --n 500 --seed 45 --error_rate 0.05 --formato csv
```

## Parámetros

| Parámetro | Descripción | Default |
|---|---|---|
| `--n` | Número de registros | 500 |
| `--seed` | Semilla de reproducibilidad | 45 |
| `--error_rate` | Tasa de error (0-1) | 0.05 |
| `--formato` | Formato de salida (csv/json) | csv |

---

## Ejemplo de ejecución

```bash
python main.py --n 500 --seed 45 --error_rate 0.05 --formato csv
```

Genera siempre los mismos 500 clientes con los mismos errores inyectados.

Archivos generados:
- `archivos/clientes_YYYYMMDD_HHMM_seed00.csv`
- `reportes/reporte_YYYYMMDD_HHMM_seed00.json`