# GUÍA DE PREPARACIÓN PARA LA SUSTENTACIÓN ORAL
### Caso de Estudio Big Data (2026-II) · Universidad Externado de Colombia
**Docente Titular:** Yessica Liceth Velasquez Castiblanco  
**Integrantes:**
* **Arnold Santiago Torres Anzola** (Componente A: Datos y Almacenamiento)
* **Alejandro Esteban Martinez Acosta** (Componente B: Procesamiento PySpark y AQE)
* **Nicolas Felipe Figueroa Salgado** (Componente C: Desempeño, Spark UI y Visualizaciones)

---

## 1. REGLAS Y PROTOCOLO DE LA SUSTENTACIÓN (ANEXO C)

* **Fecha y franja:** Miércoles 18 de noviembre de 2026 (entre 7:00 y 11:00 a. m.).
* **Tiempo total por equipo:** 18,5 minutos (3 integrantes).
  * **Ingreso y sorteo:** 1 minuto.
  * **Exposición oral:** 9 minutos (3 minutos por integrante, estrictos y cronometrados).
  * **Preguntas individuales:** 7,5 minutos (2,5 minutos por integrante).
  * **Cierre:** 1 minuto.
* **El sorteo sorpresa:** Al entrar, la docente **sortea qué componente (A, B o C) expone cada integrante**, sin previo aviso. Por tanto, **todos deben dominar los 3 componentes**.
* **Preguntas individuales:** Cada integrante responderá dos preguntas:
  1. Una sobre el **componente declarado como propio** en la bitácora.
  2. Una sobre un **componente ajeno** elegido por la docente.
* **Material proyectado:** La docente proyectará exclusivamente el archivo `CasoBD_Torres-Figueroa-Martinez_Presentacion.pdf`. No se permite proyectar diapositivas modificadas ni usar dispositivos propios.

---

## 2. BANCO DE PREGUNTAS Y ARGUMENTACIÓN TÉCNICA

### 🔹 COMPONENTE A: DATOS Y ALMACENAMIENTO (Arnold Santiago Torres Anzola)

#### Pregunta 1: ¿Por qué se configuró factor de replicación 2 y no el valor por defecto de Hadoop (3)?
* **Respuesta:** Nuestro clúster en la sala Deep Learning cuenta con 1 nodo maestro y **únicamente 2 nodos trabajadores (DataNodes)**. Por diseño fundamental de HDFS (política de colocación de réplicas en rack), Hadoop nunca coloca dos réplicas del mismo bloque en un mismo nodo físico para garantizar tolerancia a fallos. Si dejáramos replicación 3, el sistema reportaría permanentemente bloques en estado *Under-Replicated* con advertencias en el NameNode. Configurar factor 2 aprovecha de manera óptima y simétrica los 2 DataNodes físicos disponibles.

#### Pregunta 2: ¿Cómo se realizó la descarga e ingesta a HDFS sin colapsar el almacenamiento local del anfitrión?
* **Respuesta:** En la terminal del nodo maestro ejecutamos una tubería (*streaming pipeline*) que conecta `curl` y `unzip -p` directamente con `hdfs dfs -put - /caso/complaints_4.5gb.csv`. El signo guion (`-`) le indica a HDFS que lea los bytes desde la entrada estándar (`stdin`) a medida que se descomprimen en memoria RAM, escribiendo los bloques de 128 MB directamente hacia los DataNodes. Esto requirió **cero espacio en disco local** en el sistema anfitrión.

#### Pregunta 3: ¿Qué información clave aporta el comando `hdfs fsck` y cómo certifica la salud del clúster?
* **Respuesta:** El comando `hdfs fsck /caso/complaints_4.5gb.csv -files -blocks -locations` realiza una auditoría completa del árbol de metadatos:
  1. Certifica el estado general como `HEALTHY` con 0 bloques corruptos o perdidos.
  2. Confirma el tamaño total (~4,6 GB) y el `Average block replication = 2.0`.
  3. Muestra explícitamente en qué DataNode reside cada una de las réplicas de los ~37 bloques del archivo (74 bloques totales en el clúster).

#### Pregunta 4: ¿Cuál fue el criterio de poda del dataset original?
* **Respuesta:** El dataset completo del CFPB pesaba ~5,8 GB (18,9 millones de registros), superando el rango permitido de 2 a 5 GB. En lugar de aplicar un muestreo aleatorio (que degradaría el análisis de series de tiempo), aplicamos un criterio de relevancia temporal: eliminamos el histórico antiguo (2011 a primer semestre 2023) y conservamos el 100% de los datos recientes (segundo semestre 2023 a 5 de noviembre de 2026), logrando **15.017.091 registros y ~4,6 GB**, cumpliendo con la regla de contener datos sustantivos de 2026.

---

### 🔹 COMPONENTE B: PROCESAMIENTO EN PYSPARK Y AQE (Alejandro Esteban Martinez Acosta)

#### Pregunta 1: ¿Por qué se configuraron 4 GB de memoria y 2 núcleos por executor en la SparkSession?
* **Respuesta:** Los 4 GB de `spark.executor.memory` son necesarios para albergar los búferes de memoria durante las operaciones de shuffle y agregación sobre 15 millones de filas, evitando fallos de memoria (*OutOfMemory - OOM*) o derrame de datos a disco (*disk spill*). La asignación de 2 núcleos (`spark.executor.cores`) por cada uno de los 2 ejecutores permite ejecutar 4 tareas concurrentes en paralelo sin saturar las pausas de recolección de basura (*Garbage Collection*) de la máquina virtual Java.

#### Pregunta 2: ¿Por qué se utilizó un esquema explícito (`StructType`) en lugar de `inferSchema`?
* **Respuesta:** Con un archivo CSV masivo de ~4,6 GB, si se activa `inferSchema=True`, Spark debe leer y escanear la totalidad del archivo dos veces: una para determinar los tipos de datos columna por columna y otra para construir el DataFrame. Al proveer un `StructType` estricto con las 15 columnas tipificadas, la lectura se realiza en un único paso optimizado en cuestión de segundos.

#### Pregunta 3: ¿Qué significa `AdaptiveSparkPlan isFinalPlan=false` y en qué se diferencia del plan final?
* **Respuesta:** Al ejecutar `.explain(mode="formatted")` sobre una consulta antes de disparar la acción (Captura C6), AQE reporta `isFinalPlan=false`. Esto significa que Spark ha generado un plan físico inicial basado en estadísticas estáticas del catálogo. Una vez disparada la acción, Spark ejecuta el job por etapas (*stages*), recopila estadísticas de runtime del shuffle y genera el plan final con `isFinalPlan=true` (Captura C7), donde AQE fusiona particiones de shuffle pequeñas (*coalesce*) o convierte un Sort Merge Join en Broadcast Hash Join si los datos filtrados son pequeños.

#### Pregunta 4: ¿Cuáles fueron las dos transformaciones complejas implementadas?
* **Respuesta:**
  1. *Transformación 1 (Eficiencia y latencia empresarial):* Cálculo de la latencia en días de remisión mediante `datediff(fecha_envio, fecha_recibida)`, banderas booleanas de alivio monetario y respuesta a tiempo, y agregación multivariada agrupada por producto financiero.
  2. *Transformación 2 (Cadena perezosa y Join regional):* Cadena de 5 operaciones consecutivas evaluadas de forma perezosa (filtrado, ponderación de severidad, Join regional mediante difusión con catálogo de macro-regiones, agrupación compuesta y ordenamiento global).

---

### 🔹 COMPONENTE C: DESEMPEÑO, SPARK UI Y VISUALIZACIONES (Nicolas Felipe Figueroa Salgado)

#### Pregunta 1: ¿Por qué se aplicó persistencia con `StorageLevel.MEMORY_AND_DISK` y no `MEMORY_ONLY`?
* **Respuesta:** El DataFrame de quejas enriquecidas se reutiliza en dos fases distintas: en la materialización de los gráficos ejecutivos y en el entrenamiento del modelo de MLlib. Se utilizó `MEMORY_AND_DISK` porque, si el volumen de datos persistidos sobrepasa la memoria RAM asignada a los ejecutores, Spark envía ordenadamente las particiones sobrantes a disco local en lugar de fallar o provocar la terminación de contenedores en YARN. Al concluir su uso, se ejecutó obligatoriamente `.unpersist()` para liberar memoria.

#### Pregunta 2: ¿Cómo se seleccionaron los dos stages relevantes y qué métricas se evaluaron?
* **Respuesta:**
  * *Stage Relevante 1 (Captura C8):* Corresponde a la agregación masiva `groupBy(producto)`. Se seleccionó bajo el criterio de **mayor volumen de Shuffle Read y Shuffle Write** del análisis. Se evaluaron duración mediana y máxima, balanceo de tareas y ausencia de derrame a disco (*Spill disk: ninguno*).
  * *Stage Relevante 2 (Captura C9):* Corresponde al Join regional y ordenamiento final, analizando el comportamiento de las particiones optimizadas por AQE.

#### Pregunta 3: ¿Por qué se aplica la regla de materializar con `.toPandas()` únicamente tras agregaciones?
* **Respuesta:** `.toPandas()` recolecta y materializa todos los registros distribuidos en el proceso Driver en un único nodo físico. Si se invoca sobre el DataFrame de 15 millones de filas crudo, el Driver colapsaría por falta de memoria (OOM). Al agregarlo previamente con Spark, el resultado enviado a pandas contiene pocas decenas de filas, permitiendo graficar de forma instantánea y segura con Matplotlib.

#### Pregunta 4: ¿Cuál es la conclusión de la recomendación Cloud vs. On-Premise (BigQuery vs. Spark)?
* **Respuesta:** Recomendamos una **arquitectura híbrida**: Google BigQuery como servicio serverless para analítica regulatoria interactiva y tableros en tiempo real (evidenciado en nuestra práctica con 65,8 MB leídos en 0,8 s sin costos de infraestructura ociosa), y el clúster Spark on-premise para ingesta pesada, transformaciones batch complejas y entrenamiento de modelos con MLlib, preservando la soberanía de datos sensibles.

---

### 🎁 PUNTOS EXTRAS: SPARK MLlib (+0,5 PUNTOS)

#### ¿En qué consistió la bonificación y qué valor aporta a la consultoría?
* **Respuesta:** Construimos un pipeline supervisado de clasificación binaria con Spark MLlib (`StringIndexer`, `VectorAssembler` y `LogisticRegression`) para predecir si una queja financiera recibirá **Respuesta Oportuna (`Timely response`)** o entrará en mora regulatoria según el producto y canal de ingreso.
* **Métrica clave:** El modelo alcanzó un **Area Under ROC (ROC-AUC) superior a 0,78**, demostrando capacidad discriminativa efectiva y registrándose en la **Captura C11** del notebook.
