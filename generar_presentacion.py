# -*- coding: utf-8 -*-
"""
Generador de Diapositivas en PDF para la Sustentación Oral (ReportLab)
Caso de Estudio Big Data 2026-II - Universidad Externado de Colombia
Estructura: Exactamente 10 diapositivas (Portada + 3 diapos Componente A + 3 diapos Componente B + 3 diapos Componente C)
Integrantes: Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta
Docente: Yessica Liceth Velasquez Castiblanco
"""

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generar_presentacion_pdf():
    pdf_filename = "CasoBD_Torres-Figueroa-Martinez_Presentacion.pdf"
    
    ancho, alto = 10 * inch, 5.625 * inch
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=(ancho, alto),
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.4 * inch
    )

    styles = getSampleStyleSheet()

    c_primario = colors.HexColor("#0072B2")   # Azul
    c_secundario = colors.HexColor("#D55E00") # Naranja/Bermellón
    c_fondo_card = colors.HexColor("#F8F9FA")
    c_borde = colors.HexColor("#E2E8F0")
    c_texto = colors.HexColor("#1A202C")
    c_gris_sub = colors.HexColor("#4A5568")

    s_titulo_portada = ParagraphStyle(
        'TituloPortada',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=c_primario,
        alignment=1
    )

    s_sub_portada = ParagraphStyle(
        'SubPortada',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_gris_sub,
        alignment=1
    )

    s_meta_portada = ParagraphStyle(
        'MetaPortada',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_texto,
        alignment=1
    )

    s_header_componente = ParagraphStyle(
        'HeaderComponente',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=c_secundario,
        textTransform='uppercase'
    )

    s_titulo_slide = ParagraphStyle(
        'TituloSlide',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_primario
    )

    s_card_titulo = ParagraphStyle(
        'CardTitulo',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=c_primario
    )

    s_card_body = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_texto
    )

    s_footer = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor("#A0AEC0"),
        alignment=2
    )

    story = []

    def crear_slide(comp_tag, titulo, cards_data, footer_info):
        elementos = []
        elementos.append(Paragraph(comp_tag, s_header_componente))
        elementos.append(Spacer(1, 2))
        elementos.append(Paragraph(titulo, s_titulo_slide))
        elementos.append(Spacer(1, 8))

        n_cols = len(cards_data)
        col_width = (ancho - 1.2 * inch - (n_cols - 1) * 8) / n_cols
        
        celdas = []
        for c_tit, c_txt in cards_data:
            contenido_card = [
                Paragraph(f"<b>{c_tit}</b>", s_card_titulo),
                Spacer(1, 4),
                Paragraph(c_txt, s_card_body)
            ]
            celdas.append(contenido_card)

        tabla = Table([celdas], colWidths=[col_width] * n_cols)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_fondo_card),
            ('BOX', (0,0), (-1,-1), 0.5, c_borde),
            ('INNERGRID', (0,0), (-1,-1), 8, colors.white),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        elementos.append(tabla)
        elementos.append(Spacer(1, 8))
        elementos.append(Paragraph(footer_info, s_footer))
        elementos.append(PageBreak())
        return elementos

    # DIAPOSITIVA 1: PORTADA
    story.append(Spacer(1, 16))
    story.append(Paragraph("UNIVERSIDAD EXTERNADO DE COLOMBIA · BIG DATA 2026-II", s_header_componente))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Consultoría en Big Data: Procesamiento Distribuido de Reclamaciones Financieras", s_titulo_portada))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Análisis de 15 Millones de Quejas con Apache Spark sobre Hadoop YARN y HDFS (2023–2026)", s_sub_portada))
    story.append(Spacer(1, 12))

    meta_texto = """
    <b>Entidad Contratante:</b> Consumer Financial Protection Bureau (CFPB) – EE. UU.<br/>
    <b>Integrantes del Equipo:</b> Arnold Santiago Torres Anzola · Nicolas Felipe Figueroa Salgado · Alejandro Esteban Martinez Acosta<br/>
    <b>Docente:</b> Yessica Liceth Velasquez Castiblanco · <b>Grupo:</b> MABD02 (o MABD01)<br/>
    <b>Entorno:</b> Clúster Físico Sala Deep Learning (1 Master + 2 Workers) · <b>Sustentación:</b> Miércoles 18 de Noviembre de 2026
    """
    story.append(Paragraph(meta_texto, s_meta_portada))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Entrega Técnica y Sustentación Oral · Máximo 3 Diapositivas por Componente", s_footer))
    story.append(PageBreak())

    # COMPONENTE A (3 DIAPOSITIVAS)
    story.extend(crear_slide(
        "Componente A: Datos y Almacenamiento (1/3)",
        "Selección Oficial, Poda y Validación del Dataset",
        [
            ("Fuente Oficial y Relevancia", 
             "• <b>Entidad:</b> Consumer Financial Protection Bureau (CFPB) / Data.gov.<br/>"
             "• <b>Dominio:</b> Protección al consumidor financiero ante abusos en créditos e hipotecas.<br/>"
             "• <b>Actualización:</b> Diario; se tomaron registros hasta el <b>5 de noviembre de 2026</b>.<br/>"
             "• <b>Unicidad:</b> Dataset único aprobado con trazabilidad oficial."),
            ("Poda Metodológica Justificada",
             "• <b>Volumen Original:</b> 18,9M filas (~5,8 GB), excedía el límite de 5 GB.<br/>"
             "• <b>Criterio de Poda:</b> Descarte del histórico antiguo (2011 a 2023-I: 3,9M filas eliminadas).<br/>"
             "• <b>Datos Preservados:</b> 100% de la tendencia reciente contemporánea (2023-II a nov-2026).<br/>"
             "• <b>Tamaño Final:</b> <b>~4,6 GB descomprimido / 15.017.091 filas</b> (Rango 2-5 GB)."),
            ("Respaldo en Nube y Acceso",
             "• <b>Restricción:</b> Bloqueo de puertos USB por ciberseguridad en la sala.<br/>"
             "• <b>Respaldo:</b> GitHub Releases v1.0.0 con enlace directo mediante curl.<br/>"
             "• <b>Esquema Oficial:</b> 15 atributos (Date received, Product, Issue, Company, State, Response, etc.).")
        ],
        "Caso de Estudio Big Data · Componente A · Diapositiva 1 de 3"
    ))

    story.extend(crear_slide(
        "Componente A: Datos y Almacenamiento (2/3)",
        "Estrategia de Ingesta Directa a HDFS sin Copia Local",
        [
            ("Desafío de Almacenamiento Local",
             "• <b>Riesgo:</b> Las máquinas virtuales del laboratorio tienen espacio de disco reducido.<br/>"
             "• <b>Regla:</b> Se requiere 3x del dataset (copia local + 2 réplicas HDFS = 14 GB).<br/>"
             "• Si se descargaba en el disco local antes de pasarlo a HDFS, el nodo maestro colapsaba por falta de almacenamiento."),
            ("Tubería Streaming en Memoria",
             "• <b>Solución de Ingesta:</b> Canalización directa desde URL hacia HDFS en memoria estándar:<br/>"
             "<code>curl -L -s &lt;URL&gt; | funzip | hdfs dfs -put - /caso/complaints_4.5gb.csv</code><br/>"
             "• <b>Ventaja:</b> 0 bytes de desperdicio en el almacenamiento del sistema operativo anfitrión."),
            ("Configuración de Replicación = 2",
             "• <b>Tolerancia a Fallos:</b> Se aplicó factor de replicación explícito:<br/>"
             "<code>hdfs dfs -setrep -R 2 /caso/complaints_4.5gb.csv</code><br/>"
             "• <b>Respaldo de Evidencia:</b> Captura C2 del portal NameNode (puerto 9870) mostrando Replication = 2.")
        ],
        "Caso de Estudio Big Data · Componente A · Diapositiva 2 de 3"
    ))

    story.extend(crear_slide(
        "Componente A: Datos y Almacenamiento (3/3)",
        "Auditoría Distribuida de Bloques y DataNodes (Capturas C1, C2, C3)",
        [
            ("Estado del Clúster (Captura C1)",
             "• <b>Portal NameNode (9870):</b> Pestaña <i>Datanodes</i> confirma 2 nodos trabajadores activos.<br/>"
             "• <b>Balanceo:</b> Ambos DataNodes en servicio, con almacenamiento homogéneo y capacidad suficiente para alojar los 15M de registros."),
            ("Auditoría con hdfs fsck (Captura C3)",
             "• <b>Comando:</b> <code>hdfs fsck /caso/... -files -blocks -locations</code><br/>"
             "• <b>Status:</b> HEALTHY (sin bloques corruptos ni perdidos).<br/>"
             "• <b>Average Block Replication:</b> Exactamente <b>2,0</b>.<br/>"
             "• <b>Ubicación de bloques:</b> Verificación de réplicas cruzadas entre DataNode 1 y DataNode 2."),
            ("Métricas Clave Observadas",
             "• <b>Total Size:</b> ~4.939.210.752 bytes (~4,6 GB).<br/>"
             "• <b>Tamaño por Bloque HDFS:</b> 128 MB estándar.<br/>"
             "• <b>Total de Bloques Distribuidos:</b> ~37 bloques por réplica (74 bloques totales en el clúster).")
        ],
        "Caso de Estudio Big Data · Componente A · Diapositiva 3 de 3"
    ))

    # COMPONENTE B (3 DIAPOSITIVAS)
    story.extend(crear_slide(
        "Componente B: Procesamiento (1/3)",
        "Configuración Optimizada de SparkSession sobre YARN (Capturas C4 y C5)",
        [
            ("Parámetros de Ejecución Justificados",
             "• <b>master('yarn'):</b> Orquestación distribuida formal en lugar de modo local.<br/>"
             "• <b>executor.memory = 4g:</b> 4 GB de RAM por worker para evitar OOM y derrames a disco.<br/>"
             "• <b>executor.cores = 2:</b> Óptimo paralelismo sin sobrecargar la recolección de basura (GC).<br/>"
             "• <b>executor.instances = 2:</b> 2 ejecutores en los 2 nodos físicos (4 tareas concurrentes)."),
            ("Adaptive Query Execution (AQE)",
             "• <b>spark.sql.adaptive.enabled = true:</b> Optimización dinámica de planes en tiempo de ejecución.<br/>"
             "• <b>spark.sql.shuffle.partitions = 200:</b> Particionamiento balanceado para operaciones de shuffle masivo.<br/>"
             "• <b>driver.memory = 2g:</b> Memoria suficiente para coordinar y recibir resultados agregados."),
            ("Trazabilidad YARN (Captura C4)",
             "• <b>application_id de Referencia:</b> Capturado en la primera corrida exitosa del 9 de noviembre.<br/>"
             "• <b>Portal ResourceManager (8088):</b> Estado RUNNING/FINISHED con usuario hadoop y cola default.")
        ],
        "Caso de Estudio Big Data · Componente B · Diapositiva 1 de 3"
    ))

    story.extend(crear_slide(
        "Componente B: Procesamiento (2/3)",
        "Análisis Exploratorio de Datos (EDA) sobre 15 Millones de Registros",
        [
            ("Ingesta Acelerada con StructType",
             "• <b>Esquema Explícito:</b> Se definió <code>StructType</code> estricto para las 15 columnas.<br/>"
             "• <b>Ventaja Técnica:</b> Evitó el doble escaneo completo de 4,6 GB que exige <code>inferSchema</code>, reduciendo el tiempo de carga a solo segundos."),
            ("Distribución Temporal y Conteo",
             "• <b>Conteo Total Verificado:</b> <b>15.017.091 filas</b> (formateado con <code>fmt_co</code>).<br/>"
             "• <b>Evolución Anual:</b><br/>"
             "  - 2023-II: 586.449 (3,9%)<br/>"
             "  - 2024: 2.734.268 (18,2%)<br/>"
             "  - 2025: 5.442.933 (36,2%)<br/>"
             "  - 2026: 6.253.441 (41,6%) -> Crecimiento crítico del volumen de quejas."),
            ("Calidad de Datos y Canales",
             "• <b>Nulos Críticos:</b> Columnas principales (producto, empresa, fechas) con 0% de nulos.<br/>"
             "• Subproducto y subproblema con nulos parciales esperados.<br/>"
             "• <b>Canal Dominante:</b> Web concentra >85% de las radicaciones ciudadanas.")
        ],
        "Caso de Estudio Big Data · Componente B · Diapositiva 2 de 3"
    ))

    story.extend(crear_slide(
        "Componente B: Procesamiento (3/3)",
        "Transformaciones Complejas y Plan Físico AQE (Capturas C6 y C7)",
        [
            ("Transformación 1: Latencia y Eficiencia",
             "• <b>Latencia:</b> <code>datediff(fecha_envio, fecha_recibida)</code>.<br/>"
             "• <b>Agregación Multivariada:</b> Por producto financiero: volumen, días promedio de remisión, tasa de respuesta a tiempo y tasa de alivio monetario al consumidor."),
            ("Transformación 2: Join Regional",
             "• <b>Cadena Perezosa:</b> 5 transformaciones encadenadas (filtro, índice de severidad, agrupación).<br/>"
             "• <b>Broadcast Hash Join:</b> Cruce con tabla pequeña de macro-regiones de EE.UU. difundida a todos los workers sin shuffle de red."),
            ("Contraste de Planes AQE",
             "• <b>Plan Inicial (Captura C6):</b> Salida <code>.explain()</code> muestra <b>AdaptiveSparkPlan isFinalPlan=false</b>.<br/>"
             "• <b>Plan Final (Captura C7):</b> Spark UI SQL Details muestra <b>isFinalPlan=true</b> tras optimizar particiones en runtime.")
        ],
        "Caso de Estudio Big Data · Componente B · Diapositiva 3 de 3"
    ))

    # COMPONENTE C (3 DIAPOSITIVAS)
    story.extend(crear_slide(
        "Componente C: Desempeño y Resultados (1/3)",
        "Análisis de Spark UI y Monitoreo de Stages Críticos (Capturas C8 y C9)",
        [
            ("Stage Relevante 1 (Captura C8)",
             "• <b>Criterio de Relevancia:</b> Mayor volumen de Shuffle Read / Shuffle Write del job.<br/>"
             "• <b>Causa:</b> Redistribución masiva de 15M de filas para el <code>groupBy(producto)</code>.<br/>"
             "• <b>Métricas:</b> Balanceo equitativo entre tareas, duración mediana controlada y <b>cero derrames a disco (Spill disk: ninguno)</b>."),
            ("Stage Relevante 2 (Captura C9)",
             "• <b>Criterio de Relevancia:</b> Combinación y ordenamiento global con Join regional.<br/>"
             "• <b>Optimización AQE:</b> Reducción dinámica de particiones de shuffle ociosas (coalescing), evitando overhead en el cluster.<br/>"
             "• <b>Eficiencia:</b> Tareas ejecutadas en paralelo sobre los 4 cores disponibles."),
            ("Diagnóstico de Cuellos de Botella",
             "• La serialización y el tráfico de red en shuffle fueron el componente de mayor peso.<br/>"
             "• La configuración de 4 GB de RAM por worker fue clave para contener los buffers en memoria.")
        ],
        "Caso de Estudio Big Data · Componente C · Diapositiva 1 de 3"
    ))

    story.extend(crear_slide(
        "Componente C: Desempeño y Resultados (2/3)",
        "Persistencia, Patrón de Visualización y Hallazgos (Captura C10)",
        [
            ("Política de Persistencia (Captura C10)",
             "• <b>Nivel:</b> <code>MEMORY_AND_DISK</code> sobre el DataFrame base reutilizado.<br/>"
             "• <b>Justificación:</b> Evita recalcular transformaciones previas para las visualizaciones y el modelo MLlib.<br/>"
             "• <b>Liberación:</b> Uso estricto de <code>.unpersist()</code> al concluir."),
            ("Patrón Arquitectural de Visualización",
             "• <b>Patrón:</b> Spark (distribuido) -> <code>.toPandas()</code> (solo tras agregar) -> Matplotlib.<br/>"
             "• <b>Accesibilidad:</b> Paleta Okabe-Ito (lineamientos Visualización I), sin bordes innecesarios.<br/>"
             "• <b>Formato Colombiano:</b> Uso estricto de <code>fmt_co()</code> (punto para miles, coma para decimales)."),
            ("Hallazgos Clave para el Cliente",
             "• Reportes crediticios concentran el mayor volumen pero con resolución automatizada.<br/>"
             "• Hipotecas y cobranza presentan mayor severidad y tasa de compensación monetaria.<br/>"
             "• Macro-región Sur y Oeste concentran más del 60% de los reclamos del país.")
        ],
        "Caso de Estudio Big Data · Componente C · Diapositiva 2 de 3"
    ))

    story.extend(crear_slide(
        "Componente C: Desempeño y Resultados (3/3)",
        "Recomendación Cloud vs. On-Premise y Bonificación MLlib (Captura C11)",
        [
            ("Recomendación Cloud vs. On-Premise",
             "• <b>Propuesta para CFPB:</b> Arquitectura híbrida.<br/>"
             "• <b>Spark On-Premise:</b> Ideal para pipelines batch pesados, depuración histórica y privacidad de datos sensibles (15M filas procesadas en 48 s).<br/>"
             "• <b>BigQuery Serverless:</b> Ideal para tableros interactivos y auditoría rápida (65,8 MB escaneados en 0,8 s en práctica institucional), sin costos fijos de administración."),
            ("Bonificación Spark MLlib (+0,5 Puntos)",
             "• <b>Pipeline:</b> StringIndexer -> VectorAssembler -> LogisticRegression distribuida.<br/>"
             "• <b>Objetivo:</b> Clasificación binaria para predecir si una queja tendrá respuesta a tiempo.<br/>"
             "• <b>Evidencia (Captura C11):</b> <b>ROC-AUC >= 0,78 y Exactitud global</b> documentadas en celda.")
        ],
        "Caso de Estudio Big Data · Componente C · Diapositiva 3 de 3"
    ))

    doc.build(story)
    print(f"Presentación PDF generada exitosamente en: {pdf_filename}")

if __name__ == "__main__":
    generar_presentacion_pdf()
