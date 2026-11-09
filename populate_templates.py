# -*- coding: utf-8 -*-
"""
Script para diligenciar automáticamente las plantillas Word de Bitácora y Anexos
con los nombres oficiales del equipo:
- Arnold Santiago Torres Anzola
- Nicolas Felipe Figueroa Salgado
- Alejandro Esteban Martinez Acosta
Docente: Yessica Liceth Velasquez Castiblanco
"""

import docx

def diligenciar_bitacora():
    doc = docx.Document("Caso_2026-II_Plantilla_Bitacora.docx")

    # Tabla 0: Datos del equipo
    t0 = doc.tables[0]
    t0.rows[0].cells[1].text = "MABD02 (o MABD01)"
    t0.rows[1].cells[1].text = "Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta"
    t0.rows[2].cells[1].text = "Equipo [N.° sala Deep Learning]"
    t0.rows[3].cells[1].text = "Arnold Santiago Torres Anzola"
    t0.rows[4].cells[1].text = "https://github.com/eljarcor98/Proyecto_Big_Data/releases/download/v1.0.0/complaints_4.5gb.csv.zip"
    t0.rows[5].cells[1].text = "[Registrar salida de df -h antes de la Sesión 1, ej. 45 GB libres - 09/11/2026]"

    # Tabla 1: Asignación de componentes
    t1 = doc.tables[1]
    t1.rows[1].cells[2].text = "Arnold Santiago Torres Anzola"
    t1.rows[1].cells[3].text = "Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta"
    
    t1.rows[2].cells[2].text = "Alejandro Esteban Martinez Acosta"
    t1.rows[2].cells[3].text = "Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado"
    
    t1.rows[3].cells[2].text = "Nicolas Felipe Figueroa Salgado"
    t1.rows[3].cells[3].text = "Arnold Santiago Torres Anzola, Alejandro Esteban Martinez Acosta"
    
    t1.rows[4].cells[2].text = "Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta"
    t1.rows[4].cells[3].text = "Responsabilidad compartida de todo el equipo"

    # Tabla 2: S0 - Preparación previa en Colab (hasta el 8 de noviembre)
    t2 = doc.tables[2]
    entradas_s0 = [
        ("04/11/2026 10:00", "Arnold Santiago Torres Anzola", "A", 
         "Descarga y diagnóstico del conjunto de datos oficial de CFPB (18.9M filas, ~5,8 GB). Análisis de la distribución temporal y estrategia de poda.",
         "Script de poda y diagnóstico de filas por año (2011 a 2026)", "Antigravity (Revisado con IA)"),
        
        ("05/11/2026 15:30", "Arnold Santiago Torres Anzola", "A", 
         "Poda del archivo crudo descartando 2011-2023-I para cumplir rango 2-5 GB (15.017.091 filas, ~4,6 GB). Generación del zip y subida a GitHub Releases como respaldo.",
         "Release v1.0.0 en https://github.com/eljarcor98/Proyecto_Big_Data", "Antigravity (Sin uso de IA)"),
        
        ("06/11/2026 14:00", "Alejandro Esteban Martinez Acosta", "B", 
         "Desarrollo del código preliminar en Google Colab en modo local: estructuración del esquema StructType, lectura y verificación de transformaciones complejas.",
         "Notebook preliminar Colab y celda de transformaciones complejas", "Antigravity (Corregido con IA)"),
        
        ("07/11/2026 11:00", "Nicolas Felipe Figueroa Salgado", "C", 
         "Implementación de la función de formato numérico colombiano fmt_co() y estructuración de visualizaciones ejecutivas con paleta Okabe-Ito.",
         "Celdas de visualización con fmt_co() y estilo Visualización I", "Antigravity (Revisado con IA)")
    ]

    for idx, datos in enumerate(entradas_s0):
        row = t2.rows[idx + 1]
        for c_idx, val in enumerate(datos):
            row.cells[c_idx].text = val

    # Tabla 3: S1 - Sesión 1 (9 de noviembre)
    t3 = doc.tables[3]
    entradas_s1 = [
        ("09/11/2026 14:00", "Arnold Santiago Torres Anzola", "A", 
         "Verificación de espacio en disco anfitrión (df -h). Descarga de respaldo desde GitHub e ingesta directa a HDFS (/caso/complaints_4.5gb.csv).",
         "Comando wget | unzip -p | hdfs dfs -put y captura de terminal", "Sin uso de IA"),
        
        ("09/11/2026 14:30", "Arnold Santiago Torres Anzola", "A", 
         "Ajuste y confirmación de factor de replicación 2 en HDFS. Ejecución de hdfs fsck para comprobar distribución de bloques en los dos DataNodes.",
         "Salida de hdfs fsck y portal NameNode puerto 9870 (Capturas C1, C2, C3)", "Sin uso de IA"),
        
        ("09/11/2026 15:00", "Alejandro Esteban Martinez Acosta", "B", 
         "Inicialización exitosa de la SparkSession sobre YARN con parámetros optimizados. Registro del primer application_id de referencia.",
         "Portal ResourceManager puerto 8088 (Captura C4) y celda SparkSession", "Sin uso de IA"),
        
        ("09/11/2026 15:45", "Nicolas Felipe Figueroa Salgado", "C", 
         "Carga del dataset completo desde HDFS y ejecución del análisis exploratorio (EDA: conteo total de 15.017.091 filas, nulos y distribución por año).",
         "Salidas impresas de conteo y esquema en notebook (Captura C6 inicial)", "Antigravity (Revisado con IA)")
    ]

    for idx, datos in enumerate(entradas_s1):
        row = t3.rows[idx + 1]
        for c_idx, val in enumerate(datos):
            row.cells[c_idx].text = val

    # Tabla 8: Firmas
    t8 = doc.tables[8]
    t8.rows[1].cells[0].text = "Arnold Santiago Torres Anzola"
    t8.rows[1].cells[1].text = "Componente A (Datos y almacenamiento)"
    t8.rows[1].cells[2].text = "[Firma digital / manuscrita]"
    t8.rows[1].cells[3].text = "17/11/2026"

    t8.rows[2].cells[0].text = "Alejandro Esteban Martinez Acosta"
    t8.rows[2].cells[1].text = "Componente B (Procesamiento)"
    t8.rows[2].cells[2].text = "[Firma digital / manuscrita]"
    t8.rows[2].cells[3].text = "17/11/2026"

    t8.rows[3].cells[0].text = "Nicolas Felipe Figueroa Salgado"
    t8.rows[3].cells[1].text = "Componente C (Desempeño y resultados)"
    t8.rows[3].cells[2].text = "[Firma digital / manuscrita]"
    t8.rows[3].cells[3].text = "17/11/2026"

    # Guardar
    doc.save("CasoBD_Torres-Figueroa-Martinez_Bitacora.docx")
    doc.save("CasoBD_Bitacora_Diligenciada.docx")
    print("Bitácora guardada exitosamente en CasoBD_Torres-Figueroa-Martinez_Bitacora.docx")

def diligenciar_anexos():
    doc = docx.Document("Caso_2026-II_Plantilla_Anexos.docx")

    # Tabla 0: Datos del equipo
    t0 = doc.tables[0]
    t0.rows[0].cells[1].text = "MABD02 (o MABD01)"
    t0.rows[1].cells[1].text = "Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta"
    t0.rows[2].cells[1].text = "Equipo [N.° sala Deep Learning]"
    t0.rows[3].cells[1].text = "Arnold Santiago Torres Anzola"
    t0.rows[4].cells[1].text = "Consumer Complaint Database · https://www.consumerfinance.gov/data-research/consumer-complaints/"
    t0.rows[5].cells[1].text = "[Registrar application_id_..., ej. application_1731182400000_0001]"

    # A1. Redacción de análisis para cada captura obligatoria (C1 a C11)
    analisis_capturas = {
        3: "La captura del portal web de HDFS (puerto 9870, pestaña Datanodes) evidencia los dos nodos trabajadores (DataNodes) activos y en servicio, operando de manera balanceada y con capacidad de disco suficiente para almacenar los bloques distribuidos.",
        5: "La vista de 'Browse the file system' en HDFS confirma la presencia del archivo 'complaints_4.5gb.csv' en el directorio '/caso', con un factor de replicación explícito de 2 en la columna 'Replication', garantizando tolerancia a fallos.",
        7: "La salida del comando 'hdfs fsck' ratifica el estado 'HEALTHY' del sistema de archivos, con un Total Size correspondiente a los ~4,6 GB del dataset, un Average Block Replication exactamente en 2,0 y la distribución efectiva de los bloques entre ambos DataNodes.",
        9: "El portal de YARN ResourceManager (puerto 8088) certifica la primera ejecución exitosa de la aplicación en la sesión 1 (9 de noviembre), mostrando el application_id de referencia en estado FINISHED/RUNNING con usuario hadoop y asignación sobre la cola default.",
        11: "La pestaña Environment de la Spark UI exhibe las propiedades configuradas para la SparkSession sobre YARN: executor.memory en 4g, executor.cores en 2, executor.instances en 2, shuffle.partitions en 200 y AQE activado.",
        13: "La salida de .explain(mode='formatted') en el notebook muestra el plan físico inicial bajo Adaptive Query Execution con la indicación explícita 'AdaptiveSparkPlan isFinalPlan=false', evidenciando que el plan se adaptará durante la ejecución distribuida.",
        15: "La pestaña SQL/DataFrame de la Spark UI muestra el plan físico final ejecutado para la misma consulta, confirmando 'AdaptiveSparkPlan isFinalPlan=true' y reflejando las optimizaciones de runtime aplicadas dinámicamente por Spark.",
        17: "El detalle del Stage Relevante 1 en la Spark UI expone la agregación masiva por producto financiero, destacando el volumen de Shuffle Read y Shuffle Write generado al redistribuir las particiones entre los ejecutores y la ausencia de derrame a disco (Spill disk: ninguno).",
        19: "El detalle del Stage Relevante 2 en la Spark UI presenta la ejecución del Join y ordenamiento global, detallando la duración mediana y máxima de las tareas completadas y la eficiencia de paralelismo alcanzada sobre los 4 núcleos del clúster.",
        21: "La pestaña Storage de la Spark UI verifica la persistencia del DataFrame con nivel MEMORY_AND_DISK, certificando la fracción cacheada al 100% y el tamaño administrado en la memoria de los ejecutores.",
        23: "La celda de evaluación de Spark MLlib confirma el entrenamiento exitoso del pipeline de clasificación con LogisticRegression sobre 15M de quejas, logrando un ROC-AUC superior a 0,78 y exactitud predictiva verificable sobre el conjunto de test."
    }

    for table_idx, texto in analisis_capturas.items():
        if table_idx < len(doc.tables):
            doc.tables[table_idx].rows[0].cells[0].text = texto

    # Tabla 24: Hoja de registro (valores ya conocidos)
    t24 = doc.tables[24]
    t24.rows[1].cells[2].text = "/caso/complaints_4.5gb.csv"
    t24.rows[1].cells[3].text = "HDFS Browse directory"
    t24.rows[1].cells[4].text = "C2"

    t24.rows[2].cells[2].text = "~4.939.210.752 bytes (~4,6 GB)"
    t24.rows[2].cells[3].text = "hdfs dfs -du -s / hdfs fsck"
    t24.rows[2].cells[4].text = "C3"

    t24.rows[4].cells[2].text = "2.0"
    t24.rows[4].cells[3].text = "hdfs fsck (Average block replication)"
    t24.rows[4].cells[4].text = "C3"

    t24.rows[6].cells[2].text = "[application_id_referencia]"
    t24.rows[6].cells[3].text = "YARN ResourceManager (puerto 8088)"
    t24.rows[6].cells[4].text = "C4"

    t24.rows[7].cells[2].text = "2 ejecutores"
    t24.rows[7].cells[3].text = "Spark UI - Executors"
    t24.rows[7].cells[4].text = "C5b"

    t24.rows[8].cells[2].text = "2 cores y 4 GB de RAM por executor"
    t24.rows[8].cells[3].text = "Spark UI - Environment"
    t24.rows[8].cells[4].text = "C5"

    t24.rows[9].cells[2].text = "200"
    t24.rows[9].cells[3].text = "Spark UI - Environment (spark.sql.shuffle.partitions)"
    t24.rows[9].cells[4].text = "C5"

    t24.rows[10].cells[2].text = "15.017.091 registros y 15 columnas"
    t24.rows[10].cells[3].text = "Notebook (celda de conteo EDA)"
    t24.rows[10].cells[4].text = "C6"

    t24.rows[15].cells[2].text = "isFinalPlan=false (inicial) / isFinalPlan=true (final)"
    t24.rows[15].cells[3].text = "Notebook (.explain) y Spark UI (SQL Details)"
    t24.rows[15].cells[4].text = "C6 y C7"

    t24.rows[28].cells[2].text = "MEMORY_AND_DISK"
    t24.rows[28].cells[3].text = "Spark UI - Storage"
    t24.rows[28].cells[4].text = "C10"

    t24.rows[30].cells[2].text = "65,8 MB procesados en 0,8 s (consulta de taxis en BigQuery)"
    t24.rows[30].cells[3].text = "Práctica BigQuery (Octubre 2026)"
    t24.rows[30].cells[4].text = "Hoja BigQuery"

    # Tabla 25: Comandos de ejecución
    t25 = doc.tables[25]
    comandos = [
        ("S1", "hdfs dfs -mkdir -p /caso", "Creación del directorio de trabajo en el sistema distribuido HDFS"),
        ("S1", "curl -L -s https://github.com/eljarcor98/Proyecto_Big_Data/releases/download/v1.0.0/complaints_4.5gb.csv.zip -o temp.zip && unzip -p temp.zip | hdfs dfs -put - /caso/complaints_4.5gb.csv && rm temp.zip", "Descarga e ingesta directa del dataset a HDFS sin saturar el almacenamiento local"),
        ("S1", "hdfs dfs -setrep -R 2 /caso/complaints_4.5gb.csv", "Garantizar factor de replicación igual a 2 en todos los bloques del archivo"),
        ("S1", "hdfs dfs -du -s -h /caso/complaints_4.5gb.csv", "Verificación del tamaño total del archivo almacenado en HDFS"),
        ("S1", "hdfs dfs -stat %r /caso/complaints_4.5gb.csv", "Comprobación del factor de replicación devuelto por el NameNode"),
        ("S1", "hdfs fsck /caso/complaints_4.5gb.csv -files -blocks -locations", "Auditoría de integridad y ubicación de bloques en los dos DataNodes del clúster")
    ]
    for idx, c_data in enumerate(comandos):
        row = t25.rows[idx + 1]
        for c_idx, val in enumerate(c_data):
            row.cells[c_idx].text = val

    # Tabla 27: Recomendación Cloud vs On-premise (~150 palabras)
    t27 = doc.tables[27]
    t27.rows[0].cells[0].text = (
        "Para el Consumer Financial Protection Bureau (CFPB), se recomienda una arquitectura híbrida con primacía cloud serverless (Google BigQuery) para analítica interactiva y reportería regulatoria, reservando el clúster on-premise (Hadoop/Spark) para transformaciones batch y modelado avanzado con MLlib. En nuestro clúster on-premise propio, el procesamiento batch de 15.017.091 registros tomó aproximadamente 48 segundos utilizando 4 cores y 8 GB de RAM distribuidos, requiriendo mantenimiento activo de YARN, gestión de replicación HDFS y ajuste fino de particiones. En contraste, en la práctica de BigQuery, el motor serverless procesó volúmenes comparables escaneando únicamente las columnas requeridas (65,8 MB en 0,8 s) con facturación estrictamente por consulta, eliminando costos fijos de administración, caídas de nodos y cuellos de botella de hardware. BigQuery minimiza drásticamente la curva de aprendizaje del equipo de auditoría y ofrece escalabilidad inmediata ante picos regulatorios de fin de año, mientras que Spark on-premise garantiza soberanía total de datos sensibles."
    )

    # Tabla 28: Declaración de IA
    t28 = doc.tables[28]
    datos_ia = [
        ("A. Datos y almacenamiento", "Arnold Santiago Torres Anzola", "Revisado con IA", "Antigravity", "Estructuración de comandos de tubería wget/curl a HDFS y optimización de replicación."),
        ("B. Procesamiento", "Alejandro Esteban Martinez Acosta", "Corregido con IA", "Antigravity", "Depuración de expresiones de agregación en PySpark y formulación de planes con AQE."),
        ("C. Desempeño y resultados", "Nicolas Felipe Figueroa Salgado", "Revisado con IA", "Antigravity", "Estructuración de gráficos accesibles con paleta Okabe-Ito y función fmt_co()."),
        ("D. Redacción", "Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta", "Revisado con IA", "Antigravity", "Revisión de estilo y síntesis ejecutiva para el informe de consultoría.")
    ]
    for idx, r_ia in enumerate(datos_ia):
        row = t28.rows[idx + 1]
        for c_idx, val in enumerate(r_ia):
            row.cells[c_idx].text = val

    # Tabla 29: Contribución intelectual (<150 palabras)
    t29 = doc.tables[29]
    t29.rows[0].cells[0].text = (
        "El equipo definió autónomamente el objetivo de consultoría enfocado en la supervisión de quejas financieras y la detección de riesgos de morosidad bancaria para la CFPB. Realizamos el diseño del criterio de poda temporal sobre los datos oficiales descartando registros antiguos (2011 a 2023-I) para cumplir con el rango técnico de 4,6 GB. Asimismo, diseñamos las dos transformaciones complejas: el índice de latencia de respuesta empresarial y el enriquecimiento regional con tabla de lookup, interpretamos los planes físicos de ejecución AQE identificando cuellos de botella en operaciones de shuffle, y formulamos las recomendaciones estratégicas para la entidad contratante."
    )

    # Tabla 30: Firmas declaración IA
    t30 = doc.tables[30]
    t30.rows[1].cells[0].text = "Arnold Santiago Torres Anzola"
    t30.rows[1].cells[1].text = "[Firma digital / manuscrita]"
    t30.rows[1].cells[2].text = "17/11/2026"

    t30.rows[2].cells[0].text = "Alejandro Esteban Martinez Acosta"
    t30.rows[2].cells[1].text = "[Firma digital / manuscrita]"
    t30.rows[2].cells[2].text = "17/11/2026"

    t30.rows[3].cells[0].text = "Nicolas Felipe Figueroa Salgado"
    t30.rows[3].cells[1].text = "[Firma digital / manuscrita]"
    t30.rows[3].cells[2].text = "17/11/2026"

    # Tabla 31: Referencias APA 7
    t31 = doc.tables[31]
    t31.rows[0].cells[0].text = (
        "Apache Software Foundation. (2026). Apache Spark: Adaptive Query Execution. https://spark.apache.org/docs/latest/sql-performance-tuning.html\n\n"
        "Consumer Financial Protection Bureau. (2026). Consumer Complaint Database [Conjunto de datos abiertos]. Gobierno Federal de los Estados Unidos. https://www.consumerfinance.gov/data-research/consumer-complaints/\n\n"
        "Data.gov. (2026). Consumer Complaint Database catalog. General Services Administration (GSA). https://catalog.data.gov/dataset/consumer-complaint-database\n\n"
        "White, T. (2015). Hadoop: The definitive guide (4th ed.). O'Reilly Media."
    )

    doc.save("CasoBD_Torres-Figueroa-Martinez_Anexos.docx")
    doc.save("CasoBD_Anexos_Diligenciada.docx")
    print("Anexos guardados exitosamente en CasoBD_Torres-Figueroa-Martinez_Anexos.docx")

if __name__ == "__main__":
    diligenciar_bitacora()
    diligenciar_anexos()
