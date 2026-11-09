# CASO DE ESTUDIO — BIG DATA (2026-II)
### Procesamiento Masivo con Apache Spark sobre Hadoop YARN y HDFS
**Universidad Externado de Colombia · Maestría en Ciencia de Datos**

* **Docente Titular:** Yessica Liceth Velasquez Castiblanco
* **Entidad Contratante:** Consumer Financial Protection Bureau (CFPB) – EE. UU.
* **Integrantes del Equipo:**
  * **Arnold Santiago Torres Anzola** *(Componente A: Datos y Almacenamiento)*
  * **Alejandro Esteban Martinez Acosta** *(Componente B: Procesamiento en Spark)*
  * **Nicolas Felipe Figueroa Salgado** *(Componente C: Desempeño, Spark UI y Visualizaciones)*
  * *Componente D (Redacción e Informe): Responsabilidad compartida de todo el equipo.*
* **Grupo:** MABD02 (o MABD01)
* **Entorno de Ejecución:** Clúster físico en Sala Deep Learning (1 Nodo Maestro + 2 Nodos Trabajadores).

---

## 📥 Descarga del Dataset y Canalización a HDFS

El dataset oficial de la CFPB fue podado y optimizado a **~4,6 GB descomprimido** (**15.017.091 registros**), conservando el 100% de los datos recientes (segundo semestre de 2023 a noviembre de 2026).

Para descargar y canalizar directamente a HDFS en el clúster sin saturar el almacenamiento local:

```bash
# 1. Crear directorio en HDFS
hdfs dfs -mkdir -p /caso

# 2. Descarga e ingesta directa en memoria (descomprimiendo en streaming)
curl -L -s https://github.com/eljarcor98/Proyecto_Big_Data/releases/download/v1.0.0/complaints_4.5gb.csv.zip -o temp.zip && unzip -p temp.zip | hdfs dfs -put - /caso/complaints_4.5gb.csv && rm temp.zip

# 3. Forzar factor de replicación 2
hdfs dfs -setrep -R 2 /caso/complaints_4.5gb.csv

# 4. Verificación de bloques y salud de HDFS
hdfs dfs -du -s -h /caso/complaints_4.5gb.csv
hdfs dfs -stat %r /caso/complaints_4.5gb.csv
hdfs fsck /caso/complaints_4.5gb.csv -files -blocks -locations
```

---

## 📦 Estructura de Entregables Oficiales en este Repositorio

| Archivo | Tipo de Entregable | Descripción |
| :--- | :--- | :--- |
| **`CasoBD_Torres-Figueroa-Martinez_Notebook.ipynb`** | **Cuaderno PySpark** | Código de ejecución sobre YARN: configuración explícita, carga con `StructType`, EDA, 2 transformaciones complejas, planes físicos con AQE (`isFinalPlan=false` y `true`), persistencia, visualizaciones accesibles y bonificación con **Spark MLlib (+0,5 pts)**. Banners destacados para las capturas C1 a C11. |
| **`CasoBD_Torres-Figueroa-Martinez_Informe.docx`** | **Informe de Consultoría** | Formato de consultoría ejecutiva en **exactamente 1 página** (Times New Roman 11,5 pt, márgenes de 3 cm, tamaño carta). |
| **`CasoBD_Torres-Figueroa-Martinez_Bitacora.docx`** | **Bitácora de Equipo** | Registro formal de actividades por componente, Fases S0 y S1 diligenciadas, aplicaciones ejecutadas y tabla de firmas. |
| **`CasoBD_Torres-Figueroa-Martinez_Anexos.docx`** | **Plantilla de Anexos** | Interpretaciones redactadas para capturas C1 a C11, Hoja de Registro (A2) con valores fijos, comandos (A3), recomendación Cloud vs. On-Premise (A5), declaración de IA (A6) y referencias APA 7 (A7). |
| **`CasoBD_Torres-Figueroa-Martinez_Presentacion.pdf`** | **Presentación Oral** | Diapositivas apaisadas 16:9 organizadas estrictamente en **10 diapositivas** (1 portada + 3 por componente A, B y C). |
| **`DOCUMENTACION_PROYECTO_BIGDATA.md`** | **Manual Técnico** | Documentación consolidada de referencia técnica y operativa. |

---

## 🛠️ Scripts de Automatización

* `generate_notebook.py`: Genera el cuaderno oficial con las especificaciones y banners.
* `populate_templates.py`: Diligencia y formatea las plantillas oficiales de Word.
* `generar_informe.py`: Compila el informe ejecutivo de una sola página en Word.
* `generar_presentacion.py`: Compila las diapositivas de sustentación en PDF con ReportLab.
* `complaints.csv/datos.ipynb`: Cuaderno original de filtrado y poda por fechas.
