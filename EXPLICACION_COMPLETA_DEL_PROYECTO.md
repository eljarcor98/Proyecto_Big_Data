# GUÍA MAESTRA Y EXPLICACIÓN COMPLETA DEL PROYECTO
## Consultoría en Procesamiento Masivo con Apache Spark sobre Hadoop YARN
**Universidad Externado de Colombia · Maestría en Ciencia de Datos**  
**Asignatura:** Big Data (2026-II) · **Docente:** Yessica Liceth Velásquez Castiblanco  

---

### Integrantes y Componentes Declarados:
* **Arnold Santiago Torres Anzola** — **Componente A:** Datos y Almacenamiento
* **Alejandro Esteban Martínez Acosta** — **Componente B:** Procesamiento en Spark
* **Nicolas Felipe Figueroa Salgado** — **Componente C:** Desempeño, Spark UI y Bonificación
* **Responsabilidad Compartida** — **Componente D:** Redacción, Informe Ejecutivo y Presentación

---

## 1. CONTEXTO DE NEGOCIO Y ROL DE CONSULTORÍA

### ¿Quién es el cliente?
La **Consumer Financial Protection Bureau (CFPB)** *(Oficina para la Protección Financiera del Consumidor de los Estados Unidos)*. Es la agencia del gobierno federal estadounidense encargada de supervisar a los bancos (JPMorgan, Wells Fargo, Bank of America, Citibank, etc.) y agencias crediticias (Equifax, Experian, TransUnion) para proteger a los ciudadanos de fraudes, cobros indebidos y demoras abusivas.

### ¿Cuál es el problema del cliente?
La CFPB recibe cientos de miles de quejas mensuales. Su base histórica acumulada superaba los **15 millones de reclamaciones contemporáneas (4,6 GB de datos crudos)**. Sus sistemas tradicionales de bases de datos relacionales (RDBMS) colapsaban al intentar calcular estadísticas nacionales, tardaban horas en generar reportes y eran puramente **reactivos** (solo sancionaban al banco meses después de ocurrida la infracción).

### ¿Para qué nos contrataron?
Nos contrataron como firma consultora de Big Data para:
1. Diseñar una **arquitectura distribuida** capaz de auditar los 15 millones de quejas en segundos.
2. Identificar qué productos financieros y regiones del país concentran las peores infracciones y demoras.
3. Construir un **modelo de inteligencia artificial (Spark MLlib)** que prediga si un banco violará el plazo legal de respuesta (SLA) apenas entra una queja.
4. Emitir un **dictamen de inversión tecnológica**: recomendar si la CFPB debe comprar servidores propios (*On-Premise*) o migrar a la nube (*Cloud Serverless con Google BigQuery*).

---

## 2. INFRAESTRUCTURA Y ALMACENAMIENTO (COMPONENTE A)

### Clúster Físico de Referencia
* **Ubicación:** Laboratorio de Deep Learning de la Universidad.
* **Máquina física:** `Equipo [0068656]` (Espacio libre antes de iniciar: 54 GB).
* **Propietario del clúster:** Alejandro Esteban Martínez Acosta.
* **Arquitectura:** 1 Nodo Maestro (NameNode / ResourceManager) + 2 Nodos Trabajadores (DataNodes / NodeManagers).

### Poda del Conjunto de Datos (Dataset Pruning)
* **Regla estricta de la Guía:** El archivo descomprimido en HDFS debe pesar **obligatoriamente entre 2 GB y 5 GB**.
* **El archivo original:** El registro histórico de la CFPB desde 2011 pesaba ~5,8 GB (18,9 millones de filas), lo que violaba el tope máximo.
* **Criterio de poda aplicado:** Poda por relevancia temporal. Se conservaron las quejas del periodo contemporáneo pospandemia (segundo semestre de 2023 hasta noviembre de 2026).
* **Resultado:** Un archivo de **~4,6 GB (15.017.091 registros y 15 columnas crudas)** denominado `complaints_4.5gb.csv`.

### Ingesta a HDFS sin Saturar el Disco Local
* Se ejecutó una tubería directa en Linux:
  ```bash
  curl -L -s <url_respaldo> -o temp.zip && unzip -p temp.zip | hdfs dfs -put - /caso/complaints_4.5gb.csv && rm temp.zip
  ```
* Los datos pasaron por memoria y entraron directo a HDFS, sin ocupar espacio duplicado en el disco anfitrión.

### Tolerancia a Fallos y Replicación
* **Factor de replicación:** Se forzó a 2 con `hdfs dfs -setrep -R 2 /caso/complaints_4.5gb.csv`.
* **Auditoría con `hdfs fsck` (Captura C3):**
  * Estado: **HEALTHY**.
  * Average Block Replication: **2.0**.
  * Total de bloques lógicos: **35 bloques de 128 MB** (70 bloques físicos entre las dos réplicas).
  * Distribución: Perfectamente balanceada entre el DataNode 1 y el DataNode 2 (Captura C1 y C2).

### Incidente Operacional Resuelto (Tabla 27 - Error 1)
* **Incidente:** El 9 de noviembre de 2026, el firewall institucional de la universidad bloqueó la descarga directa con `curl` desde GitHub Releases.
* **Solución aplicada:** Se utilizó una copia espejo de respaldo alojada en OneDrive institucional, permitiendo completar la carga en HDFS sin retrasar el cronograma.

---

## 3. PROCESAMIENTO DISTRIBUIDO EN APACHE SPARK (COMPONENTE B)

### Parámetros de la SparkSession sobre YARN (Capturas C4 y C5)
* **Application IDs:** `application_1794259897184_0001` (Sesión 1) y `application_1794430508749_0002` (Sesión 2).
* **Memoria por ejecutor:** `spark.executor.memory = 4g`.
* **Cores por ejecutor:** `spark.executor.cores = 2` (Total clúster: 4 núcleos).
* **Particiones de Shuffle:** `spark.sql.shuffle.partitions = 200`.
* **Optimizador Adaptativo:** `spark.sql.adaptive.enabled = true` (AQE).
* **Justificación técnica:** 4 GB de RAM para 2 núcleos garantizan hasta 2 GB por tarea física, evitando cuellos de botella y desbordamientos a disco.

### Ingesta Tipificada con `StructType` (Celda 7)
* No se usó `inferSchema=True` porque obligaría a Spark a leer los 4,6 GB dos veces.
* Al suministrar el esquema explícito de 15 columnas tipificadas, la ingesta y tipificación tomó **solo 1,24 segundos**.

### Exploración Masiva (EDA Distribuido - Celdas 9 y 10)
* **Censo total:** **15.017.091 registros** evaluados en paralelo sobre **35 particiones**.
* **Distribución temporal auditada:**
  * 2023: 1.583.567 quejas
  * 2024: 5.674.882 quejas
  * 2025: 6.124.912 quejas *(pico histórico de reclamaciones)*
  * 2026 (a nov): 1.633.730 quejas
* **Calidad del dato:** 0% de nulos en variables clave de supervisión (`producto`, `empresa`, `fecha_recibida`).

### Las Dos Transformaciones Complejas de Consultoría (Celdas 12, 14 y 18)
1. **Transformación 1 (Supervisión Operativa por Producto):**
   * Agrupa las 15M de quejas por tipo de producto y calcula: días promedio de trámite, porcentaje de respuestas a tiempo y tasa de compensación económica (*alivio monetario*).
   * **Tiempo en clúster:** **13,75 segundos** (condensó 15M de filas en **14 categorías**).
2. **Transformación 2 (Equidad Territorial - Operación Crítica):**
   * Cruza las 15M de quejas con un catálogo de 51 estados y 4 macro-regiones mediante un Join para calcular el **Índice de Latencia de Respuesta**.
   * **Tiempo en clúster:** **12,44 segundos** (generó **69 filas agregadas**).
* **Tiempo total del análisis principal:** **26,18 segundos**.

### Auditoría del Optimizador Catalyst y AQE (Capturas C6 y C7)
* **Plan inicial (Celda 16 - C6):** `.explain(mode='formatted')` muestra `AdaptiveSparkPlan isFinalPlan=false` en la raíz, indicando que el plan físico es tentativo y se adaptará durante la ejecución.
* **Plan final (Spark UI SQL Details - C7):** Muestra `isFinalPlan=true` porque AQE inspeccionó las estadísticas reales de runtime, coalesció particiones vacías y confirmó el uso de `BroadcastHashJoin`.

---

## 4. OPTIMIZACIÓN DE MEMORIA, SHUFFLES Y CERO SPILL (COMPONENTE C)

### ¿Cómo es posible que 4,6 GB no desbordaran los 4 GB de RAM?
1. **Divide y Vencerás:** El archivo nunca entra completo a la RAM. Está dividido en HDFS en 35 bloques de 128 MB.
2. **Límite físico de núcleos:** Con 4 cores en total, el clúster solo puede ejecutar 4 tareas simultáneas.
3. **Cálculo en tiempo real:**
   $$4\text{ tareas concurrentes} \times 128\text{ MB} = \mathbf{512\text{ MB máximos en la RAM en cualquier instante}}$$
   512 MB caben con holgura absoluta en los 8 GB de RAM totales de los workers. Las tareas procesan por oleadas (*waves*), descartando los datos crudos al terminar cada bloque.

### ¿Por qué el Shuffle fue de solo 62 MiB y no de 4,6 GB? (Captura C8 - Stage 30)
* **Pre-agregación en el origen (`HashAggregate` en dos fases):**
  * Cada DataNode lee su bloque local y va sumando en una tabla hash en su memoria RAM local (`partial_count`). Las 400.000 filas de cada bloque se colapsan localmente en solo 14 filas de subtotales.
  * Por el cable de red **solo viajan los subtotales ya resumidos (62,0 MiB)**.
* **Poda de columnas:** Se descartan las 13 columnas no utilizadas antes del shuffle.
* **BroadcastHashJoin (Captura C9 - Stage 19):** Al cruzar con los estados, Spark envió una copia de la tabla pequeña (~2 KB) a cada worker. El Shuffle Read fue de apenas **45,5 KiB** y tardó solo **52 milisegundos**.

### ¿Qué es el Spill y por qué fue CERO («ninguno»)?
* El **Spill** es un desbordamiento de emergencia: ocurre cuando la memoria RAM de ejecución se satura y Spark se ve forzado a volcar búferes al disco local (`/tmp`), multiplicando el tiempo por 10x.
* En nuestras métricas (Capturas C8 y C9):
  $$\text{Spill (Memory): 0 B} \quad / \quad \text{Spill (Disk): 0 B} \quad \rightarrow \quad \text{«ninguno»}$$
* **Por qué no hubo Spill:**
  * Se asignaron 4 GB por ejecutor.
  * Con 200 particiones de shuffle, cada tarea solo manejó búferes de:
    $$\frac{62\text{ MiB}}{200\text{ particiones}} \approx \mathbf{317\text{ KB por tarea}}$$
  * 317 KB caben instantáneamente en RAM sin tocar el disco.

### Política de Caché con `MEMORY_AND_DISK` (Captura C10 - Celda 20)
* **Persistencia selectiva:** No se cacheó el CSV crudo. Se proyectaron únicamente las 7 columnas necesarias para los gráficos y el modelo (`df_base_reutilizable`).
* **Compresión Tungsten en RAM:** Los 15.017.091 registros se comprimieron en RAM mediante diccionarios binarios.
* **Métrica en Storage (C10):**
  * `Storage Level: MEMORY_AND_DISK`
  * `Fraction Cached: 100%`
  * `Size in Memory: 115.3 MiB`
  * `Size on Disk: 0 B`
* **Por qué conservamos los datos en memoria:** Para evitar que Spark tuviera que releer los 4,6 GB desde HDFS 3 veces consecutivas al generar los gráficos y entrenar el modelo.
* **Liberación de memoria (Celda 24):** Se ejecutó `.unpersist()` para limpiar los 115 MiB de RAM al finalizar su uso.

---

## 5. BONIFICACIÓN: MACHINE LEARNING CON SPARK MLLIB (+0,5 PTS)

### El Enfoque Predictivo (Celda 26 - Captura C11)
* **Objetivo de negocio:** Pasar de la supervisión reactiva a la preventiva. Predecir si un banco violará el plazo legal de respuesta al consumidor (`respuesta_a_tiempo: Yes vs No`).
* **Arquitectura del Pipeline distribuido:**
  1. `StringIndexer`: Codifica variables categóricas (`producto`, `canal_envio`).
  2. `VectorAssembler`: Ensambla los índices en un vector de características denso.
  3. `LogisticRegression`: Estimador distribuido optimizado con L-BFGS.
* **Resultados reales obtenidos en el clúster:**
  * **Tiempo de entrenamiento:** **41,42 segundos**.
  * **Métrica Area Under ROC (ROC-AUC):** **`0,8301`** *(Capacidad sobresaliente de discriminación, supera ampliamente el 0,78 base)*.
  * **Exactitud Global (Accuracy):** **`99,61%`**.
* **Impacto regulatorio:** La CFPB puede emitir alertas automáticas a los bancos en el mismo instante en que el consumidor radica la queja.

---

## 6. DICTAMEN DE CONSULTORÍA: CLOUD VS. ON-PREMISE (TABLA 28)

| Dimensión | Clúster On-Premise (Hadoop / Spark) | Cloud Serverless (Google BigQuery) |
| :--- | :--- | :--- |
| **Tiempo de consulta** | 26,18 segundos (análisis 15M filas) | **0,8 segundos** (práctica de laboratorio) |
| **Volumen escaneado** | 4,6 GB en HDFS (lectura particionada) | **65,8 MB** (proyección columnar estricta) |
| **Administración** | Alta (gestión de YARN, replicación, particiones) | **Cero servidores** (serverless autogestionado) |
| **Modelo de costos** | Costo fijo de hardware y electricidad | Facturación variable por consulta escaneada |
| **Seguridad / Soberanía** | Soberanía total de datos confidenciales | Cumplimiento regulatorio en nube pública |

### Recomendación Estratégica Entregada a la CFPB:
Se recomienda una **Arquitectura Híbrida**:
1. **Google BigQuery (Nube):** Para la reportería diaria, tableros interactivos y consultas ad-hoc de los inspectores financieros (baja latencia, cobro por consulta, cero mantenimiento).
2. **Spark On-Premise:** Para cargas batch pesadas nocturnas, ingesta de datos bancarios ultra confidenciales y reentrenamiento periódico de los modelos de Machine Learning con MLlib.

---

## 7. RESUMEN DE LA HOJA DE REGISTRO (TABLA 25 / ANEXO A2)

Para la sustentación y el documento Word, estos son los **números de oro oficiales**:

* **Ruta en HDFS:** `/caso/complaints_4.5gb.csv`
* **Tamaño HDFS:** ~4.939.210.752 bytes (~4,6 GB)
* **Número de bloques:** 35 bloques (bloques 0 a 34)
* **Replicación:** 2.0 (auditada con `hdfs fsck`)
* **DataNodes:** DataNode 1 y DataNode 2
* **Application ID de referencia:** `application_1794259897184_0001` (S1) / `application_1794430508749_0002` (S2)
* **Executors vivos:** 2 ejecutores (4 GB RAM y 2 cores cada uno)
* **Shuffle partitions:** 200
* **Registros y columnas:** 15.017.091 registros y 15 columnas crudas (17 con fechas derivadas)
* **Particiones del DataFrame:** 35 particiones
* **Operación crítica:** Bloque 5 (`df_enriquecido.explain()`)
* **Estrategia de Join:** `BroadcastHashJoin` (plan inicial y final)
* **isFinalPlan:** `false` (inicial en notebook) / `true` (final en Spark UI)
* **Stage Relevante 1 (C8):** Stage 30 — Criterio (b) Shuffle Read = 62.0 MiB, Duración = 8s, Spill = ninguno.
* **Stage Relevante 2 (C9):** Stage 19 — Criterio (d) Operación crítica, Duración = 52 ms, Spill = ninguno.
* **Tiempo total del análisis principal:** 26,18 segundos (T1 en 13,75 s + T2 en 12,44 s)
* **Filas agregadas:** 14 filas (T1) y 69 filas (T2)
* **Storage Level:** `MEMORY_AND_DISK`
* **Caché:** Fraction Cached = 100%, Size in Memory = 115.3 MiB, Size on Disk = 0 B
* **MLlib Bonificación:** ROC-AUC = 0,8301, Accuracy = 99,61%, Tiempo = 41,42 s.


---

## 8. MAPA INTEGRAL DE EJECUCIONES EN LA CONSULTORÍA (CFPB)
### ¿Qué hace cada ejecución, qué propósito tiene y qué resultado da la impresión?

| Bloque | Ejecución en el Clúster | Componente y Responsable | Propósito en la Consultoría (CFPB) | Resultado e Impresión Observada |
| :---: | :--- | :---: | :--- | :--- |
| **Bloque 1** | **SparkSession sobre YARN** | **Comp. B**<br>*(A. E. Martínez)* | Dimensionar el clúster con concurrencia óptima para procesar el censo nacional de 15M de quejas sin cuellos de botella ni fallos de memoria. | `application_1794430508749_0002`: 2 ejecutores × 4 GB RAM × 2 cores (8 GB RAM y 4 cores totales), 200 particiones de shuffle y AQE activo. |
| **Bloque 2** | **Ingesta HDFS con StructType** | **Comp. A**<br>*(A. S. Torres)* | Garantizar almacenamiento seguro y tolerante a fallos del repositorio federal (4,6 GB). Usar `StructType` para evitar el costo de inferencia automática. | Ingesta en **1,24 s** dividida en **35 bloques de 128 MB** con **factor de replicación 2.0** (70 réplicas físicas entre DataNodes). Cero pérdida de datos. |
| **Bloque 3** | **Auditoría Censal (EDA)** | **Comp. B**<br>*(A. E. Martínez)* | Auditar el 100% de las quejas ciudadanas (sin muestreo que introduzca sesgos legales) y certificar la latencia de respuesta institucional. | **15.017.091 quejas censadas** en 18 columnas; integridad referencial del 100%; latencia promedio de respuesta de **4,45 días** (cumpliendo límite legal de 15 días). |
| **Bloque 4** | **Transformación 1: Riesgo por Producto** | **Comp. B**<br>*(A. E. Martínez)* | Identificar qué productos concentran disputas y cuáles otorgan compensación económica al consumidor ante abusos bancarios. | 14 categorías en **13,75 s**. *Credit reporting* y tarjetas concentran >70% de quejas pero con **<10% de compensación económica**, evidenciando alta fricción administrativa. |
| **Bloque 4** | **Transformación 2: Equidad Regional** | **Comp. B**<br>*(A. E. Martínez)* | Evaluar disparidades territoriales de atención bancaria cruzando 51 estados clasificados en 4 macro-regiones. | 69 combinaciones en **12,44 s**. La región **Sur concentra el 40,3%** de la litigiosidad nacional, priorizando la apertura de oficinas de inspección de la CFPB. |
| **Bloque 5** | **Optimización Catalyst y AQE** | **Comp. B**<br>*(A. E. Martínez)* | Auditar la eficiencia computacional del plan físico para no saturar la red ni desperdiciar presupuesto público en el clúster. | Whole-Stage CodeGen (`*`), pre-agregación en 2 fases (`HashAggregate` con `partial_count`) y difusión de estados con `BroadcastHashJoin`. |
| **Bloque 6** | **Auditoría Spark UI y Spill** | **Comp. C**<br>*(N. F. Figueroa)* | Certificar estabilidad en estrés operativo, tráfico de red (Shuffle Read) y verificar ausencia de derrame a disco. | Stage 30 (62,0 MiB Shuffle Read) y Stage 19 (45,5 KiB). **Spill (Memoria y Disco) = 0 B («ninguno»)**. Tiempo total de transformaciones: **26,18 s**. |
| **Bloque 7** | **Persistencia Selectiva** | **Comp. C**<br>*(N. F. Figueroa)* | Mantener en memoria RAM la capa depurada para tableros sin el costo de releer 4,6 GB desde HDFS. | Ocupación en RAM de **solo 115,3 MiB** para 15M de filas (reducción 97% con Tungsten); liberado con `.unpersist()`. |
| **Bloque 8** | **Visualizaciones Ejecutivas** | **Comp. C**<br>*(N. F. Figueroa)* | Traducir los hallazgos en gráficos para la Junta Directiva de la CFPB con rigor perceptivo. | 2 gráficos ejecutivos (Okabe-Ito, formato colombiano) que confirman la primacía de quejas en reportes crediticios y el predominio territorial del Sur. |
| **Bloque 9** | **Supervisión MLlib (+0,5 pts)** | **Comp. C**<br>*(N. F. Figueroa)* | Evolucionar de una supervisión reactiva a preventiva: predecir qué entidades bancarias violarán el plazo legal de respuesta al consumidor. | Pipeline supervisado con LogisticRegression entrenado en **41,42 s** con **ROC-AUC = 0,8301** y **Exactitud = 99,61%** en prueba independiente. |
| **Bloque 10** | **Matriz Consolidada y Cloud** | **Comp. D**<br>*(Compartida)* | Entregar a la CFPB la hoja de balance técnico y la recomendación económica On-Premise vs Cloud. | Matriz unificada de 16 indicadores auditados y análisis de costo total de propiedad (TCO) para arquitectura híbrida. |
