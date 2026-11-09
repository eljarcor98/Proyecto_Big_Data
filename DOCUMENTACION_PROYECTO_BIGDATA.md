# DOCUMENTACIÓN TÉCNICA Y OPERATIVA — CASO DE ESTUDIO BIG DATA (2026-II)
**Universidad Externado de Colombia · Maestría en Ciencia de Datos**  
**Asignatura:** Big Data (Período 2026-II)  
**Modalidad:** Procesamiento por lotes (Batch) con Apache Spark sobre Hadoop YARN y HDFS  

---

## 1. FICHA TÉCNICA DEL PROYECTO Y EQUIPO

* **Docente Titular:** Yessica Liceth Velasquez Castiblanco
* **Entidad Contratante:** Consumer Financial Protection Bureau (CFPB) – División de Supervisión y Regulación Financiera (Gobierno Federal de EE. UU.).
* **Problema de Consultoría:** Supervisión y análisis masivo del crecimiento exponencial de reclamaciones sobre productos crediticios e hipotecarios (2023–2026): evaluación de tiempos de respuesta empresarial, tasas de compensación económica y detección de riesgos sistémicos mediante arquitectura distribuida.
* **Integrantes del Equipo:**
  * **Arnold Santiago Torres Anzola** (Componente A: Datos y Almacenamiento)
  * **Alejandro Esteban Martinez Acosta** (Componente B: Procesamiento en Spark)
  * **Nicolas Felipe Figueroa Salgado** (Componente C: Desempeño, Spark UI y Visualizaciones)
  * *Componente D (Redacción e Informe): Responsabilidad compartida de todo el equipo.*
* **Grupo:** MABD02 (o MABD01)
* **Clúster de Referencia:** Sala Deep Learning (1 Nodo Maestro + 2 Nodos Trabajadores / DataNodes).
* **Propietario del Clúster de Referencia:** Arnold Santiago Torres Anzola.

---

## 2. FICHA TÉCNICA DEL CONJUNTO DE DATOS (DATASET)

### 2.1 Identificación y Fuentes Oficiales
* **Nombre Oficial:** Consumer Complaint Database.
* **Entidad Publicadora:** Consumer Financial Protection Bureau (CFPB) / Data.gov.
* **URL Oficial Primaria:** [https://www.consumerfinance.gov/data-research/consumer-complaints/](https://www.consumerfinance.gov/data-research/consumer-complaints/)
* **URL Catálogo Data.gov:** [https://catalog.data.gov/dataset/consumer-complaint-database](https://catalog.data.gov/dataset/consumer-complaint-database)
* **URL de Respaldo en la Nube (GitHub Releases):**  
  [https://github.com/eljarcor98/Proyecto_Big_Data/releases/download/v1.0.0/complaints_4.5gb.csv.zip](https://github.com/eljarcor98/Proyecto_Big_Data/releases/download/v1.0.0/complaints_4.5gb.csv.zip)
* **Repositorio del Proyecto:** [https://github.com/eljarcor98/Proyecto_Big_Data](https://github.com/eljarcor98/Proyecto_Big_Data)

### 2.2 Dimensiones, Poda y Validación de Criterios de la Guía
* **Cumplimiento de Rango de Tamaño:** Entre 2 GB y 5 GB descomprimido.
  * Tamaño archivo filtrado: **~4,6 GB descomprimido** (cumple plenamente).
* **Total de Filas Conservadas:** **15.017.091 registros** (excluyendo encabezado).
* **Cobertura Temporal:** 1 de agosto de 2023 hasta el **5 de noviembre de 2026** (incluye datos sustantivos y actualizados de 2026).
* **Criterio de Poda Técnica Justificada:**  
  Para cumplir con los límites de infraestructura de la sala Deep Learning sin desvirtuar la tendencia contemporánea, se descartó el histórico antiguo (2011 a primer semestre 2023) y se preservó el 100% de los datos recientes:
  * **Datos conservados (15.017.091 filas):**
    * 2026 (hasta 5 de nov): 6.253.441 filas (100% del año en curso).
    * 2025: 5.442.933 filas (100% del año).
    * 2024: 2.734.268 filas (100% del año).
    * 2023 (segundo semestre): 586.449 filas (desde 1 de agosto a 31 de diciembre).
  * **Datos eliminados (3.918.700 filas podadas):**
    * 2011 a 2022: 3.213.101 filas (100% podadas).
    * 2023 (primer semestre): 705.599 filas (100% podadas).

### 2.3 Estructura del Archivo y Esquema (15 Columnas)
| N.° | Nombre de Columna en CSV | Nombre Estandarizado | Tipo PySpark | Descripción del Dato |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `Date received` | `fecha_recibida` | `DateType` | Fecha de radicación ante el CFPB. |
| 2 | `Product` | `producto` | `StringType` | Categoría del producto financiero (Credit reporting, Mortgage, etc.). |
| 3 | `Sub-product` | `subproducto` | `StringType` | Subcategoría específica del producto. |
| 4 | `Issue` | `problema` | `StringType` | Motivo principal de la queja. |
| 5 | `Sub-issue` | `subproblema` | `StringType` | Detalle puntual del reclamo. |
| 6 | `Company public response` | `respuesta_publica_empresa` | `StringType` | Declaración pública emitida por la entidad. |
| 7 | `Company` | `empresa` | `StringType` | Nombre de la entidad financiera o banco. |
| 8 | `State` | `estado` | `StringType` | Código postal/estado de EE. UU. (ej. CA, NY, TX). |
| 9 | `ZIP code` | `codigo_postal` | `StringType` | Código postal del consumidor. |
| 10 | `Tags` | `etiquetas` | `StringType` | Marcas de grupos de interés (Servicemember, Older American). |
| 11 | `Submitted via` | `canal_envio` | `StringType` | Canal de entrada (Web, Phone, Referral, Postal mail). |
| 12 | `Date sent to company` | `fecha_envio` | `DateType` | Fecha en que CFPB remite el reclamo al banco. |
| 13 | `Company response to consumer`| `respuesta_a_consumidor` | `StringType` | Tipo de resolución (Closed with monetary relief, Closed with explanation, etc.). |
| 14 | `Timely response?` | `respuesta_a_tiempo` | `StringType` | Si la respuesta fue oportuna dentro del término legal (`Yes` / `No`). |
| 15 | `Complaint ID` | `id_queja` | `LongType` | Identificador único del expediente. |

---

## 3. GUÍA DE COMANDOS DE TERMINAL (SESIÓN 1 — INGESTA Y HDFS)

Para no agotar el espacio físico en disco del anfitrión de la sala Deep Learning, se canaliza la descarga directamente a HDFS en memoria:

```bash
# ==============================================================================
# PASO 1: Verificación de espacio en el equipo anfitrión (Terminal Host)
# ==============================================================================
df -h
# Anotar el valor libre para la entrada de la Bitácora (ej. 45 GB libres)

# ==============================================================================
# PASO 2: Creación de directorio de trabajo en HDFS
# ==============================================================================
hdfs dfs -mkdir -p /caso

# ==============================================================================
# PASO 3: Descarga directa e ingesta a HDFS (descomprimiendo en memoria)
# ==============================================================================
curl -L -s https://github.com/eljarcor98/Proyecto_Big_Data/releases/download/v1.0.0/complaints_4.5gb.csv.zip -o temp.zip && unzip -p temp.zip | hdfs dfs -put - /caso/complaints_4.5gb.csv && rm temp.zip

# ==============================================================================
# PASO 4: Asegurar factor de replicación igual a 2 (Requerimiento 1)
# ==============================================================================
hdfs dfs -setrep -R 2 /caso/complaints_4.5gb.csv

# ==============================================================================
# PASO 5: Verificaciones de almacenamiento (Para Capturas C2 y C3)
# ==============================================================================
# Verificar tamaño total del archivo:
hdfs dfs -du -s -h /caso/complaints_4.5gb.csv

# Verificar factor de replicación:
hdfs dfs -stat %r /caso/complaints_4.5gb.csv

# Auditoría de bloques y distribución en los dos DataNodes:
hdfs fsck /caso/complaints_4.5gb.csv -files -blocks -locations
```

---

## 4. CONFIGURACIÓN DE LA SPARK SESSION SOBRE YARN

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CasoBD_CFPB_Complaints_Consultoria") \
    .master("yarn") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .config("spark.executor.instances", "2") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

### Justificación Técnica de Parámetros (Captura C5):
1. **`master("yarn")`:** Enlaza el cómputo distribuido al Resource Manager de Hadoop YARN en el clúster físico.
2. **`executor.memory("4g")`:** Otorga 4 GB de memoria a cada trabajador, previniendo fallas de *OutOfMemory (OOM)* y minimizando derrames a disco (*disk spills*) al agrupar 15 millones de filas.
3. **`executor.cores("2")`:** Configura 2 núcleos por worker, equilibrando la concurrencia multihilo sin sobrecargar las pausas de recolección de basura (*Garbage Collection*) de la máquina virtual Java.
4. **`executor.instances("2")`:** Ocupa 2 contenedores sobre los dos nodos trabajadores físicos, totalizando 4 hilos concurrentes efectivos de cómputo.
5. **`driver.memory("2g")`:** Reserva 2 GB para el Driver, suficiente para la coordinación de tareas y recolección de DataFrames agregados.
6. **`shuffle.partitions("200")`:** Fracciona las redistribuciones de datos en bloques manejables durante operaciones de agrupamiento y joins.
7. **`adaptive.enabled("true")`:** Habilita Adaptive Query Execution (AQE) para ajustar el plan físico en tiempo de ejecución (fusión de particiones pequeñas y conversión automática a broadcast joins).

---

## 5. MAPEO DE CAPTURAS OBLIGATORIAS (ANEXO A1)

| N.° | Requerimiento | Qué debe verse | Análisis / Interpretación ya Redactada |
| :---: | :---: | :--- | :--- |
| **C1** | Req. 1 | Web HDFS (9870) › Datanodes | Evidencia los dos nodos trabajadores (DataNodes) en servicio, con capacidad, espacio utilizado y balance operativo en el clúster. |
| **C2** | Req. 1 | Web HDFS (9870) › Browse directory | Muestra el archivo `/caso/complaints_4.5gb.csv` con su tamaño y el valor **2** en la columna *Replication*. |
| **C3** | Req. 1 | Terminal hadoop: `hdfs fsck` | Certifica el estado *HEALTHY*, el tamaño total (~4,6 GB), promedio de replicación en 2,0 y ubicación de bloques en ambos DataNodes. |
| **C4** | Req. 2 | Web YARN (8088) › Apps | Primera ejecución exitosa de la Sesión 1 (9 de noviembre) con su `application_id` de referencia, usuario hadoop y estado. |
| **C5** | Req. 2 | Spark UI › Environment | Muestra los parámetros configurados en la SparkSession (`executor.memory=4g`, `executor.cores=2`, `shuffle.partitions=200`, `AQE=true`). |
| **C6** | Req. 5 | Notebook: salida `.explain()` | Muestra la celda completa del `.explain()` con la línea explícita `AdaptiveSparkPlan isFinalPlan=false`. |
| **C7** | Req. 5 | Spark UI › SQL / DataFrame | Detalle de la misma consulta en Spark UI confirmando el plan final ejecutado con `AdaptiveSparkPlan isFinalPlan=true`. |
| **C8** | Req. 6 | Spark UI › Stage 1 Relevante | Detalle del stage de agregación pesada (DAG, tareas, duración, Shuffle Read/Write y ausencia de derrame a disco). |
| **C9** | Req. 6 | Spark UI › Stage 2 Relevante | Detalle del stage de combinación/Join regional con tabla de lookup (DAG, métricas de tareas y tiempos de ejecución). |
| **C10** | Req. 8 | Spark UI › Storage (Condicional) | Verificación del DataFrame persistido con nivel `MEMORY_AND_DISK`, fracción cacheada al 100% y tamaño en RAM/disco. |
| **C11** | Bonificación | Notebook / Spark UI | Salida con las métricas de evaluación del modelo MLlib (**ROC-AUC $\ge 0,78$ y Exactitud**) para la bonificación de **+0,5 puntos**. |

---

## 6. FORMULACIÓN ANALÍTICA Y TRANSFORMACIONES COMPLEJAS

### 6.1 Transformación Compleja 1: Latencia y Eficiencia Empresarial
* **Métrica de latencia:** $\text{días\_remisión} = \text{datediff}(\text{fecha\_envio}, \text{fecha\_recibida})$
* **Indicadores:**
  * Tasa de oportunidad de respuesta: $\% \text{ a tiempo} = \text{avg}(\mathbb{I}(\text{Timely response} = \text{'Yes'})) \times 100$
  * Tasa de alivio monetario: $\% \text{ compensación} = \text{avg}(\mathbb{I}(\text{Company response} = \text{'Closed with monetary relief'})) \times 100$
* **Agrupación multivariada:** Por producto financiero, evaluando la demora y disposición indemnizatoria de las entidades bancarias.

### 6.2 Transformación Compleja 2: Enriquecimiento Regional y Severidad
* **Cadena perezosa ($\ge 4$ transformaciones):**
  1. Filtrado de registros sin estado territorial.
  2. Construcción de escala ponderada de severidad (1 a 4 según impacto económico y morosidad).
  3. Cruce (**Join**) con tabla de macro-regiones de EE. UU. (Northeast, Midwest, South, West).
  4. Agrupación compuesta por macro-región y producto financiero.
  5. Agregación de volumen total, severidad promedio y cálculo de tasa de expedientes vencidos.

---

## 7. RECOMENDACIÓN CLOUD VS. ON-PREMISE (ANEXO A5)

> **Texto redactado (~150 palabras):**  
> Para el Consumer Financial Protection Bureau (CFPB), se recomienda una arquitectura híbrida con primacía cloud serverless (Google BigQuery) para analítica interactiva y reportería regulatoria, reservando el clúster on-premise (Hadoop/Spark) para transformaciones batch masivas y modelado recurrente con MLlib. En nuestro clúster on-premise propio, el procesamiento batch de 15.017.091 registros tomó aproximadamente 48 segundos utilizando 4 cores y 8 GB de RAM distribuidos, requiriendo mantenimiento activo de YARN, gestión de replicación HDFS y ajuste fino de particiones. En contraste, en la práctica de BigQuery, el motor serverless procesó volúmenes comparables escaneando únicamente las columnas requeridas (65,8 MB en 0,8 s) con facturación estrictamente por consulta, eliminando costos fijos de administración, caídas de nodos y cuellos de botella de hardware. BigQuery minimiza drásticamente la curva de aprendizaje del equipo de auditoría y ofrece escalabilidad inmediata ante picos regulatorios de fin de año, mientras que Spark on-premise garantiza soberanía total de datos sensibles.

---

## 8. DECLARACIÓN DE USO DE IA (ANEXO A6)

### 8.1 Tabla por Componente (Lineamientos Universidad Externado)
| Componente | Integrante Responsable | Categoría Institucional | Herramienta | Descripción Breve del Uso |
| :--- | :--- | :---: | :---: | :--- |
| **A. Datos y almacenamiento** | Arnold Santiago Torres Anzola | Revisado con IA | Antigravity | Estructuración de comandos de tubería wget/curl hacia HDFS y optimización de replicación. |
| **B. Procesamiento** | Alejandro Esteban Martinez Acosta | Corregido con IA | Antigravity | Depuración de expresiones de agregación en PySpark y formulación de planes con AQE. |
| **C. Desempeño y resultados** | Nicolas Felipe Figueroa Salgado | Revisado con IA | Antigravity | Estructuración de gráficos accesibles con paleta Okabe-Ito y función `fmt_co()`. |
| **D. Redacción** | Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta | Revisado con IA | Antigravity | Revisión de estilo y síntesis ejecutiva para el informe de consultoría. |

### 8.2 Contribución Intelectual Significativa del Equipo (< 150 palabras)
> El equipo definió autónomamente el objetivo de consultoría enfocado en la supervisión de quejas financieras y la detección de riesgos de morosidad bancaria para la CFPB. Realizamos el diseño del criterio de poda temporal sobre los datos oficiales descartando registros antiguos (2011 a 2023-I) para cumplir con el rango técnico de 4,6 GB. Asimismo, diseñamos las dos transformaciones complejas: el índice de latencia de respuesta empresarial y el enriquecimiento regional con tabla de lookup, interpretamos los planes físicos de ejecución AQE identificando cuellos de botella en operaciones de shuffle, y formulamos las recomendaciones estratégicas para la entidad contratante.

---

## 9. REFERENCIAS BIBLIOGRÁFICAS (FORMATO APA 7.ª EDICIÓN)

* Apache Software Foundation. (2026). *Apache Spark: Adaptive Query Execution (AQE)*. https://spark.apache.org/docs/latest/sql-performance-tuning.html
* Consumer Financial Protection Bureau. (2026). *Consumer Complaint Database* [Conjunto de datos abiertos]. Gobierno Federal de los Estados Unidos. https://www.consumerfinance.gov/data-research/consumer-complaints/
* Data.gov. (2026). *Consumer Complaint Database catalog*. General Services Administration (GSA). https://catalog.data.gov/dataset/consumer-complaint-database
* White, T. (2015). *Hadoop: The definitive guide* (4th ed.). O'Reilly Media.
