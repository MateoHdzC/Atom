# 📁 trainer/ — Entrenamiento de ATOM

Contiene todo lo relacionado con el proceso de entrenamiento y aprendizaje de ATOM. Es el motor que transforma datos en inteligencia.

## Propósito

Esta carpeta gestiona cómo ATOM aprende desde cero. Los modelos profesores enseñan, y el trainer ejecuta el proceso de aprendizaje iterativo hasta que ATOM internaliza el conocimiento.

## Stack

| Componente | Tecnología | Por qué |
|------------|------------|---------|
| Framework | PyTorch | Estándar de la industria, control total del entrenamiento |
| Transformers | HuggingFace Transformers | Optimizado para modelos de lenguaje, gran ecosistema |
| Distribución | Accelerate (HuggingFace) | Manejo transparente de multi-GPU y mixed precision |

## Estructura

```
trainer/
├── configs/              ← Configuraciones de entrenamiento
│   ├── atom-1b.yaml      ← Configuración para ATOM 1B
│   ├── atom-2b.yaml      ← Configuración para ATOM 2B
│   └── defaults.yaml     ← Valores por defecto
│
├── scripts/              ← Scripts de entrenamiento
│   ├── pretrain.py       ← Pretraining desde cero
│   ├── finetune.py       ← Fine-tuning de modelos existentes
│   └── resume.py         ← Reanudar entrenamiento interrumpido
│
├── optimizers/           ← Configuraciones de optimización
│   ├── adamw.py          ← Optimizador AdamW
│   └── scheduler.py      ← Learning rate schedulers
│
├── checkpoints/          ← Checkpoints temporales durante entrenamiento
│   └── .gitkeep
│
└── logs/                 ← Logs de entrenamiento
    └── .gitkeep
```

## Tipos de Entrenamiento

### 1. Pretraining (entrenamiento desde cero)
ATOM parte sin conocimiento. Los modelos profesores generan millones de ejemplos y ATOM aprende patrones del lenguaje y el conocimiento.

**Cuándo se usa**: Primera versión de cada modelo (1B, 2B, 4B).

**Proceso**:
```
Datos procesados (data/processed/)
        ↓
Modelo inicial aleatorio
        ↓
Entrenamiento iterativo (epochs)
        ↓
Evaluación (evaluation/)
        ↓
Mejora de parámetros
        ↓
Modelo entrenado → models/
```

### 2. Fine-tuning (especialización)
Se toma un modelo ya entrenado y se le enseña algo específico (mejorar en matemáticas, programación, conversación, etc.).

**Cuándo se usa**: Para mejorar áreas débiles detectadas en evaluación.

### 3. Instruction tuning (seguimiento de instrucciones)
Se enseña a ATOM a seguir instrucciones específicas: "responde en este formato", "sé conciso", "explica paso a paso".

**Cuándo se usa**: Después del pretraining base, antes de lanzar como chatbot.

## Flujo de Entrenamiento

```
┌─────────────────────────────────────────────────┐
│                  CICLO DE ENTRENAMIENTO           │
├─────────────────────────────────────────────────┤
│                                                   │
│  1. Cargar datos desde data/processed/            │
│                    ↓                              │
│  2. Inicializar modelo (aleatorio o checkpoint)   │
│                    ↓                              │
│  3. Ejecutar epochs de entrenamiento              │
│                    ↓                              │
│  4. Evaluar con evaluation/                       │
│                    ↓                              │
│  5. ¿Mejoró? → Guardar checkpoint                │
│     ¿No mejoró? → Ajustar parámetros             │
│                    ↓                              │
│  6. Repetir hasta convergencia                    │
│                    ↓                              │
│  7. Guardar modelo final en models/               │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Hiperparámetros Clave

| Parámetro | Descripción | ATOM 1B (estimado) |
|-----------|-------------|---------------------|
| `learning_rate` | Velocidad de aprendizaje | 3e-4 |
| `batch_size` | Ejemplos por iteración | 8-32 (según RAM) |
| `epochs` | Vueltas completas al dataset | 3-10 |
| `max_seq_length` | Longitud máxima de secuencia | 2048 tokens |
| `warmup_steps` | Pasos de calentamiento | 100-500 |
| `weight_decay` | Regularización | 0.01 |

## Infraestructura

### Desarrollo local (PC)
- Primeras pruebas y debugging
- Entrenamiento de ATOM 1B
- Experimentación con parámetros

### VPS (8GB RAM, 90GB almacenamiento)
- Entrenamiento de modelos mayores (2B, 4B)
- Entrenamientos largos sin interrupción
- Producción

## Conexión con Otras Áreas

- **data/** proporciona los datos de entrenamiento
- **models/** recibe los modelos entrenados finales
- **evaluation/** verifica la calidad durante el entrenamiento
- **tokenizer/** se usa para procesar el texto antes de entrenar
