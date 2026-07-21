# 📁 teachers/ — Modelos Profesores

Contiene los modelos profesores que ayudan a entrenar y enseñar a ATOM. Son modelos locales que generan datos, evalúan respuestas y corrigen errores.

## Propósito

Los modelos profesores son el sistema de aprendizaje de ATOM. No son el cerebro — son los maestros que forman ese cerebro. Se encargan de:

1. **Generar datos**: Crear preguntas, respuestas y ejemplos para entrenar
2. **Evaluar**: Verificar si las respuestas de ATOM son correctas
3. **Corregir**: Proporcionar respuestas correctas con explicaciones
4. **Mejorar**: Identificar áreas débiles y generar ejercicios específicos

## Arquitectura de Profesores

```
┌─────────────────────────────────────────────────┐
│              SISTEMA DE PROFESORES                │
├─────────────────────────────────────────────────┤
│                                                   │
│  Profesor 1 (Qwen)                               │
│  → Generación de conocimiento general             │
│  → Evaluación de respuestas                       │
│                                                   │
│  Profesor 2 (Modelo 2)                           │
│  → Generación de problemas de razonamiento        │
│  → Evaluación de lógica                           │
│                                                   │
│  Profesor 3 (Modelo 3)                           │
│  → Generación de conversaciones                   │
│  → Evaluación de naturalidad                      │
│                                                   │
│         ↓ ↓ ↓                                     │
│  Coordinador de Profesores                        │
│  → Consolida datos                                │
│  → Resuelve conflictos                            │
│  → Genera dataset final                           │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Modelos Profesores

| Profesor | Modelo | Especialidad | Rol principal |
|----------|--------|--------------|---------------|
| Profesor 1 | Qwen | Conocimiento general | Generar datos, evaluar respuestas |
| Profesor 2 | (por definir) | Razonamiento | Generar problemas lógicos, evaluar deducción |
| Profesor 3 | (por definir) | Conversación | Generar diálogos, evaluar naturalidad |

## Instalación Local

Los modelos se ejecutan localmente via **Ollama** para:
- Sin dependencia de APIs externas
- Sin costos de uso
- Privacidad total de los datos
- Control completo del proceso

### Requisitos

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| RAM | 8GB | 16GB+ |
| Almacenamiento | 20GB | 50GB+ |
| GPU | Opcional | NVIDIA con 8GB+ VRAM |

### Instalación de Ollama

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelos profesores
ollama pull qwen2.5:7b
ollama pull [modelo-2]
ollama pull [modelo-3]
```

## Estructura

```
teachers/
├── configs/                ← Configuraciones de profesores
│   ├── qwen.yaml           ← Configuración de Qwen
│   ├── teacher-2.yaml      ← Configuración de Modelo 2
│   ├── teacher-3.yaml      ← Configuración de Modelo 3
│   └── coordinator.yaml    ← Configuración del coordinador
│
├── prompts/                ← Prompts para cada tarea
│   ├── generation/         ← Prompts para generar datos
│   │   ├── qa-generation.md
│   │   ├── conversation.md
│   │   └── reasoning.md
│   ├── evaluation/         ← Prompts para evaluar
│   │   ├── verify-answer.md
│   │   ├── correct-answer.md
│   │   └── coherence-check.md
│   └── improvement/        ← Prompts para mejorar
│       ├── weak-areas.md
│       └── exercises.md
│
├── scripts/                ← Scripts de gestión
│   ├── generate_dataset.py ← Generar dataset con profesores
│   ├── evaluate_model.py   ← Evaluar ATOM con profesores
│   ├── coordinator.py      ← Coordinar múltiples profesores
│   └── ollama_manager.py   ← Gestionar modelos Ollama
│
├── outputs/                ← Salidas generadas
│   ├── datasets/           ← Datasets generados
│   ├── evaluations/        ← Resultados de evaluación
│   └── corrections/        ← Correcciones generadas
│
└── README.md               ← Este archivo
```

## Flujo de Generación de Datos

```
┌─────────────────────────────────────────────────┐
│           GENERACIÓN DE DATASET                   │
├─────────────────────────────────────────────────┤
│                                                   │
│  1. Definir tema/categoría                        │
│                    ↓                              │
│  2. Profesor genera ejemplos                      │
│     → Preguntas y respuestas                      │
│     → Conversaciones                              │
│     → Problemas de razonamiento                   │
│                    ↓                              │
│  3. Otro profesor evalúa calidad                  │
│     → ¿La respuesta es correcta?                  │
│     → ¿La explicación es clara?                   │
│     → ¿El nivel es apropiado?                     │
│                    ↓                              │
│  4. Coordinador consolida                         │
│     → Aprueba ejemplos buenos                     │
│     → Rechaza o corrige ejemplos malos            │
│                    ↓                              │
│  5. Guardar en data/raw/                          │
│                    ↓                              │
│  6. Procesar y guardar en data/processed/         │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Flujo de Evaluación

```
┌─────────────────────────────────────────────────┐
│           EVALUACIÓN DE ATOM                      │
├─────────────────────────────────────────────────┤
│                                                   │
│  1. Cargar modelo ATOM desde models/              │
│                    ↓                              │
│  2. Hacer pregunta a ATOM                         │
│                    ↓                              │
│  3. Profesor 1 verifica respuesta                 │
│     → ¿Correcto? (sí/no)                         │
│                    ↓                              │
│  4. Si incorrecto: Profesor corrige               │
│     → Respuesta correcta                          │
│     → Explicación del por qué                     │
│                    ↓                              │
│  5. Profesor 2 evalúa coherencia                  │
│     → ¿La respuesta tiene sentido?                │
│     → ¿Está bien explicada?                       │
│                    ↓                              │
│  6. Guardar evaluación en evaluation/             │
│                    ↓                              │
│  7. Usar correcciones para re-entrenar            │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Conexión con Otras Áreas

- **data/** recibe los datos generados por los profesores
- **evaluation/** usa los profesores para evaluar a ATOM
- **trainer/** usa los datos generados para entrenar
- **src/** puede usar profesores para respuestas de respaldo
