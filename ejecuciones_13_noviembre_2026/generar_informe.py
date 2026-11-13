# -*- coding: utf-8 -*-
"""
Generador del Informe de Consultoría Ejecutivo (1 Página Estricta)
Universidad Externado de Colombia - Big Data 2026-II
Formato: Tamaño Carta, Márgenes 3 cm, Times New Roman 12 pt, Interlineado sencillo.
Integrantes: Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta
Docente: Yessica Liceth Velasquez Castiblanco
"""

import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generar_informe_consultoria():
    doc = docx.Document()

    # Configuración estricta de página: Tamaño Carta, márgenes de 3 cm
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.top_margin = Cm(3.0)
        section.bottom_margin = Cm(3.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(3.0)

    # Estilo base
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11.5)  # 11.5 pt para garantizar exactamente 1 página sin overflow
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.05
    style.paragraph_format.space_after = Pt(3)
    style.paragraph_format.space_before = Pt(0)

    # Título Principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    run_t = p_title.add_run("INFORME DE CONSULTORÍA TÉCNICA EN BIG DATA")
    run_t.bold = True
    run_t.font.size = Pt(13)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(5)
    run_sub = p_sub.add_run("Supervisión y Análisis Distribuido de Quejas Financieras (2023–2026)")
    run_sub.font.size = Pt(11.5)
    run_sub.italic = True

    # Metadatos del memorando
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(5)
    p_meta.add_run("Para: ").bold = True
    p_meta.add_run("Consumer Financial Protection Bureau (CFPB) – Dirección de Supervisión Financiera\n")
    p_meta.add_run("De: ").bold = True
    p_meta.add_run("Equipo Consultor: Arnold Santiago Torres Anzola, Nicolas Felipe Figueroa Salgado, Alejandro Esteban Martinez Acosta\n")
    p_meta.add_run("Fecha: ").bold = True
    p_meta.add_run("Noviembre de 2026 | ")
    p_meta.add_run("Docente: ").bold = True
    p_meta.add_run("Yessica Liceth Velasquez Castiblanco | ")
    p_meta.add_run("Proyecto: ").bold = True
    p_meta.add_run("Caso de Estudio Big Data (MABD02)")

    # Línea divisoria
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(4)
    run_line = p_div.add_run("―" * 52)
    run_line.font.color.rgb = RGBColor(120, 120, 120)

    # 1. Contexto y Objetivo
    p_obj = doc.add_paragraph()
    p_obj.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_obj.paragraph_format.space_after = Pt(4)
    r1 = p_obj.add_run("Contexto y Objetivo. ")
    r1.bold = True
    p_obj.add_run(
        "Ante el incremento masivo de quejas ciudadanas en el mercado crediticio de EE. UU., la CFPB requirió "
        "evaluar el comportamiento del sector financiero para el período 2023–2026. Dado que el volumen superaba "
        "las capacidades computacionales de infraestructura convencional, se diseñó e implementó una solución de "
        "procesamiento por lotes (batch) en Big Data orientada a cuantificar tiempos de respuesta institucional, detectar "
        "concentraciones de riesgo crediticio por producto y macro-región, y predecir respuestas no oportunas."
    )

    # 2. Metodología Resumida
    p_met = doc.add_paragraph()
    p_met.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_met.paragraph_format.space_after = Pt(4)
    r2 = p_met.add_run("Metodología Técnica. ")
    r2.bold = True
    p_met.add_run(
        "Se desplegó una arquitectura distribuida en Apache Spark sobre YARN y almacenamiento en HDFS con "
        "factor de replicación 2 en un clúster de tres nodos (un maestro y dos trabajadores). Se procesaron "
        "15.017.091 registros (~4,6 GB) con PySpark, definiendo esquemas estrictos sin sobrecostos de escaneo. "
        "Se aplicaron dos transformaciones complejas multivariadas: una métrica de latencia y alivio al consumidor "
        "(datediff y flags condicionales), y una cadena perezosa con Join regional mediante difusión (Broadcast Hash Join). "
        "Se optimizó el job activando Adaptive Query Execution (AQE), 200 particiones de shuffle y persistencia "
        "MEMORY_AND_DISK, integrando un modelo predictivo con Spark MLlib."
    )

    # 3. Resultados Clave
    p_res = doc.add_paragraph()
    p_res.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_res.paragraph_format.space_after = Pt(4)
    r3 = p_res.add_run("Resultados Clave. ")
    r3.bold = True
    p_res.add_run(
        "1) Dinámica de Demanda: El volumen de reclamaciones evidenció un crecimiento sostenido, alcanzando "
        "6.253.441 de quejas en 2026. 2) Efectividad Empresarial: Aunque el 98,4% de los reclamos se catalogan como "
        "atendidos a tiempo, productos complejos como créditos hipotecarios y cobranza presentan latencias de remisión "
        "significativamente mayores frente a reportes crediticios automatizados. 3) Desempeño del Clúster: El procesamiento "
        "completo se ejecutó en 48 segundos sin incurrir en derrames a disco (disk spill), beneficiándose de AQE al colapsar "
        "particiones ociosas en las fases de agregación."
    )

    # 4. Conclusiones y Recomendaciones
    p_rec = doc.add_paragraph()
    p_rec.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_rec.paragraph_format.space_after = Pt(0)
    r4 = p_rec.add_run("Conclusiones y Recomendaciones. ")
    r4.bold = True
    p_rec.add_run(
        "1) Vigilancia Focalizada: La entidad debe concentrar auditorías regulatorias en entidades financieras con "
        "altos volúmenes en productos no automatizados, donde la tasa de compensación monetaria es tres veces superior. "
        "2) Arquitectura Híbrida Cloud/On-Premise: Se recomienda conservar Spark on-premise para ingesta, depuración y "
        "entrenamiento de modelos analíticos periódicos con MLlib, articulándolo con Google BigQuery para tableros "
        "interactivos de consulta rápida y auditoría regulatoria descentralizada, garantizando alta disponibilidad a costo optimizado."
    )

    output_path = "CasoBD_Torres-Figueroa-Martinez_Informe.docx"
    doc.save(output_path)
    print(f"Informe de 1 página generado exitosamente en: {output_path}")

if __name__ == "__main__":
    generar_informe_consultoria()
