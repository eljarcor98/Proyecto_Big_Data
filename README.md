# CFPB Complaints Dataset (Reducido)

Este repositorio contiene el flujo de trabajo para procesar y analizar el dataset de quejas de la CFPB (*Consumer Financial Protection Bureau*).

El dataset original de 5.7 GB fue optimizado a **~4.5 GB** (15 millones de filas) descartando registros históricos previos al **1 de agosto de 2023** y comprimido a formato `.zip` (~236 MB).

---

## 📥 Descarga rápida del dataset comprimido

Para descargar el archivo de datos directamente desde la terminal o servidor, ejecuta:

```bash
curl -L -O https://github.com/eljarcor98/Proyecto_Big_Data/releases/download/v1.0.0/complaints_4.5gb.csv.zip
```

---

## 📓 Contenido del repositorio

* **`complaints.csv/datos.ipynb`**: Cuaderno Jupyter con las instrucciones completas para:
  1. Filtrar el dataset por fecha en modo *streaming* (sin saturar la memoria RAM).
  2. Comprimir el archivo resultante a `.zip`.
  3. Cargar y explorar los datos directamente con Pandas sin descomprimir en disco.

---

## 🚀 Uso en Pandas

```python
import pandas as pd

# Lectura directa desde el archivo comprimido (sin descomprimir)
datos = pd.read_csv("complaints_4.5gb.csv.zip", nrows=100)
print(datos.head())
```
