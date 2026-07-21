# 📁 data/ — Datos de Entrenamiento

Almacena todos los datos, parámetros e información utilizada para enseñar y entrenar a ATOM. Es la materia prima del aprendizaje del modelo.

## Propósito

Esta carpeta centraliza todo lo que ATOM necesita para aprender:
- **Datos de entrenamiento**: pares pregunta-respuesta, conversaciones, ejemplos de razonamiento
- **Parámetros**: configuraciones de hiperparámetros utilizados en cada entrenamiento
- **Datos externos**: información proveniente de modelos profesores y fuentes externas

## Estructura

```
data/
├── raw/                ← Datos crudos sin procesar
│   ├── conversations/  ← Conversaciones generadas por profesores
│   ├── qa/             ← Pares pregunta-respuesta
│   └── reasoning/      ← Ejemplos de razonamiento
│
├── processed/          ← Datos limpios y listos para entrenar
│   ├── train/          ← Conjunto de entrenamiento
│   ├── val/            ← Conjunto de validación
│   └── test/           ← Conjunto de prueba
│
├── parameters/         ← Hiperparámetros de entrenamiento
│   ├── atom-1b/        ← Configuraciones para ATOM 1B
│   ├── atom-2b/        ← Configuraciones para ATOM 2B
│   └── atom-4b/        ← Configuraciones para ATOM 4B
│
└── external/           ← Datos de fuentes externas
    ├── teacher-outputs/← Salidas generadas por modelos profesores
    └── curated/        ← Datos curados de fuentes públicas
```

## Flujo de Datos

```
1. Modelos profesores generan datos
              ↓
2. raw/ almacena los datos crudos
              ↓
3. evaluation/ verifica calidad
              ↓
4. processed/ guarda datos limpios
              ↓
5. trainer/ usa los datos para entrenar
```

## Tipos de Datos

### Conversaciones
Diálogos generados por los modelos profesores para enseñar a ATOM a conversar de forma natural.

### Pares Pregunta-Respuesta
Ejemplos de preguntas con sus respuestas correctas, evaluadas por los profesores. Incluye:
- Conocimiento general
- Programación
- Ciencia
- Matemáticas
- Razonamiento lógico

### Parámetros
Archivos de configuración (YAML/JSON) que definen:
- Learning rate
- Batch size
- Número de epochs
- Arquitectura del modelo
- Opciones de optimización

### Datos Externos
Información curada de fuentes públicas y salidas de los modelos profesores, ya evaluadas y filtradas.

## Formatos

| Tipo de dato | Formato |
|--------------|---------|
| Conversaciones | JSONL |
| Pares QA | JSONL |
| Parámetros | YAML / JSON |
| Datos procesados | Parquet (a determinar según rendimiento) |

## Conexión con Otras Áreas

- **teachers/** genera datos que llegan aquí
- **evaluation/** verifica la calidad de los datos
- **trainer/** consume los datos procesados para entrenar
