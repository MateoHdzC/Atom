# 📁 evaluation/ — Evaluación de ATOM

Pruebas para medir las capacidades, detectar errores y guiar mejoras de ATOM. Es el sistema de control de calidad del modelo.

## Propósito

Evaluation verifica que ATOM está aprendiendo correctamente y identifica áreas de mejora. Los modelos profesores evalúan las respuestas de ATOM en dos niveles:

1. **Verificación**: ¿La respuesta es correcta? (sí/no)
2. **Corrección**: Si es incorrecta, ¿cuál es la respuesta correcta y por qué?

## Sistema de Evaluación Dual

### Nivel 1 — Verificación de Respuesta

Evalúa si ATOM responde correctamente a una pregunta.

```
Pregunta: "¿Cuál es la capital de España?"
ATOM responde: "Madrid"
Profesor evalúa: ✅ CORRECTO

Pregunta: "¿Cuál es la capital de España?"
ATOM responde: "Barcelona"
Profesor evalúa: ❌ INCORRECTO
```

### Nivel 2 — Corrección con Explicación

Si la respuesta es incorrecta, el profesor proporciona la respuesta correcta con explicación para que ATOM aprenda.

```
Pregunta: "¿Cuál es la capital de España?"
ATOM responde: "Barcelona"
Profesor corrige: ❌ INCORRECTO
  → Respuesta correcta: "Madrid"
  → Explicación: "Madrid es la capital de España desde 1561,
    cuando Felipe II trasladó la corte desde Toledo.
    Barcelona es la capital de Cataluña, una comunidad
    autónoma del noreste de España."

ATOM aprende esta corrección para mejorar.
```

## Tipos de Evaluación

### 1. Evaluación de Conocimiento
Verifica si ATOM sabe hechos correctos.

| Categoría | Ejemplo |
|-----------|---------|
| Geografía | "¿Capital de Francia?" → "París" |
| Historia | "¿Quién descubrió América?" → "Cristóbal Colón" |
| Ciencia | "¿Cuál es la fórmula del agua?" → "H2O" |
| Matemáticas | "¿Cuánto es 7×8?" → "56" |

### 2. Evaluación de Razonamiento
Verifica si ATOM puede pensar lógicamente.

| Tipo | Ejemplo |
|------|---------|
| Lógica | "Si A > B y B > C, ¿A > C?" → "Sí" |
| Deducción | "Todos los gatos son animales. Mi mascota es un gato. ¿Es un animal?" → "Sí" |
| Problemas | "Tengo 3 manzanas y comí 1. ¿Cuántas me quedan?" → "2" |

### 3. Evaluación de Conversación
Verifica si ATOM puede conversar naturalmente.

| Aspecto | Qué se evalúa |
|---------|---------------|
| Coherencia | ¿La respuesta tiene sentido con la pregunta? |
| Naturalidad | ¿Suena como una persona real? |
| Utilidad | ¿La respuesta es útil para el usuario? |
| Seguridad | ¿Evita contenido dañino? |

### 4. Evaluación de Coherencia
Verifica que las respuestas no solo sean correctas, sino que tengan sentido completo.

```
Pregunta: "¿Qué es Python?"
ATOM responde: "Un lenguaje"           ← Correcto pero incompleto
Profesor evalúa: ⚠️ PARCIAL
  → Respuesta mejor: "Python es un lenguaje de programación
    de alto nivel, interpretado y con sintaxis simple.
    Se usa en desarrollo web, ciencia de datos e IA."

ATOM aprende a dar respuestas completas y coherentes.
```

## Métricas

| Métrica | Descripción | Objetivo |
|---------|-------------|----------|
| **Accuracy** | % de respuestas correctas | >70% (1B), >80% (2B), >90% (4B) |
| **Perplexity** | Qué tan "sorprendido" está el modelo | Menor es mejor |
| **Coherence Score** | Calidad de las explicaciones | >0.7 (escala 0-1) |
| **Response Quality** | Utilidad general de las respuestas | >0.7 (escala 0-1) |

## Estructura

```
evaluation/
├── benchmarks/             ← Conjuntos de pruebas
│   ├── knowledge.json      ← Preguntas de conocimiento
│   ├── reasoning.json      ← Problemas de razonamiento
│   ├── conversation.json   ← Pruebas de conversación
│   └── coherence.json      ← Pruebas de coherencia
│
├── evaluators/             ← Scripts de evaluación
│   ├── verifier.py         ← Nivel 1: Verificación
│   ├── corrector.py        ← Nivel 2: Corrección con explicación
│   ├── coherence.py        ← Evaluación de coherencia
│   └── metrics.py          ← Cálculo de métricas
│
├── teacher_eval/           ← Evaluación por modelos profesores
│   ├── eval_config.yaml    ← Configuración de evaluación
│   ├── eval_round.py       ← Ejecutar una ronda de evaluación
│   └── results/            ← Resultados de evaluaciones
│       ├── atom-1b-v1.0.0/
│       └── atom-1b-v1.1.0/
│
├── reports/                ← Reportes de evaluación
│   ├── template.md         ← Plantilla de reporte
│   └── latest.md           ← Último reporte generado
│
└── scripts/                ← Utilidades
    ├── run_all.py          ← Ejecutar todas las evaluaciones
    ├── compare_versions.py ← Comparar dos versiones del modelo
    └── generate_report.py  ← Generar reporte de evaluación
```

## Flujo de Evaluación

```
┌─────────────────────────────────────────────────┐
│              CICLO DE EVALUACIÓN                  │
├─────────────────────────────────────────────────┤
│                                                   │
│  1. Cargar modelo desde models/                   │
│                    ↓                              │
│  2. Ejecutar benchmarks                           │
│     → Conocimiento                                │
│     → Razonamiento                                │
│     → Conversación                                │
│     → Coherencia                                  │
│                    ↓                              │
│  3. Modelos profesores evalúan respuestas         │
│     → Nivel 1: ¿Correcto? (sí/no)                │
│     → Nivel 2: Corrección + explicación           │
│                    ↓                              │
│  4. Calcular métricas                             │
│     → Accuracy, Perplexity, Coherence Score       │
│                    ↓                              │
│  5. Generar reporte                               │
│     → Fortalezas, debilidades, recomendaciones    │
│                    ↓                              │
│  6. ¿Mejoró respecto a versión anterior?          │
│     → Sí: Aprobar versión                         │
│     → No: Identificar áreas de mejora             │
│                    ↓                              │
│  7. Guardar resultados en teacher_eval/results/   │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Conexión con Otras Áreas

- **teachers/** proporciona los modelos profesores que evalúan
- **models/** es evaluado por este sistema
- **trainer/** usa los resultados para mejorar el entrenamiento
- **data/** puede generar datos de corrección para re-entrenar
