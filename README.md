# ATOM — Inteligencia Artificial Propia

ATOM es un proyecto de creación de una inteligencia artificial propia desde cero, con el objetivo de construir un modelo independiente entrenado con una identidad, conocimientos y forma de razonamiento propios.

## Visión

A diferencia de una IA que simplemente utiliza modelos existentes para responder, ATOM tiene su propio núcleo. Otros modelos actúan como **profesores**, ayudando a construir su aprendizaje mediante generación de preguntas, respuestas, evaluaciones y mejoras.

```
Modelos profesores (Qwen + Modelo 2 + Modelo 3)
              ↓
 Generación y evaluación de conocimiento
              ↓
        Entrenamiento de ATOM
              ↓
    ATOM 1B → ATOM 2B → ATOM 4B
```

## Objetivo

Crear **ATOM 1B**: un modelo propio de aproximadamente 1.000 millones de parámetros, capaz de conversar, razonar, aprender patrones y tener una personalidad definida. Diseñado para evolucionar a futuras versiones (ATOM 2B, ATOM 4B).

## Estructura del Proyecto

```
Atom/
├── data/           → Datos de entrenamiento y parámetros
├── docs/           → Documentación general del proyecto
├── evaluation/     → Pruebas y métricas de rendimiento
├── models/         → Versiones y estados de los modelos
├── src/            → Código fuente del sistema ATOM
├── teachers/       → Modelos profesores y sus configuraciones
├── tokenizer/      → Procesamiento de lenguaje
└── trainer/        → Proceso de entrenamiento
```

| Carpeta | Propósito |
|---------|-----------|
| [data/](data/) | Almacena todos los datos, parámetros e información utilizada para entrenar a ATOM |
| [docs/](docs/) | Documentación general, ideas, diseños y planificación del proyecto |
| [evaluation/](evaluation/) | Pruebas para medir capacidades, detectar errores y guiar mejoras |
| [models/](models/) | Versiones finales de los modelos entrenados y backups |
| [src/](src/) | Chatbot por terminal (CLI) — la forma de usar ATOM |
| [teachers/](teachers/) | Modelos profesores locales que generan datos y evalúan a ATOM |
| [tokenizer/](tokenizer/) | Gestión de cómo ATOM interpreta y procesa el lenguaje |
| [trainer/](trainer/) | Todo lo relacionado con el proceso de entrenamiento |

## Stack Técnico

| Componente | Tecnología |
|------------|------------|
| Framework de entrenamiento | PyTorch + HuggingFace Transformers |
| Tokenizer | BPE (Byte-Pair Encoding) |
| Idiomas | Español + Inglés (~32k-50k tokens) |
| Modelos profesores | Locales via Ollama |
| Interfaz de usuario | CLI (terminal) |

## Esquema de Versiones

| Versión | Modelo | Descripción |
|---------|--------|-------------|
| 1.0.0 - 1.9.9 | ATOM 1B | Modelo base (~1B parámetros) |
| 2.0.0 - 2.9.9 | ATOM 2B | Escalamiento (~2B parámetros) |
| 4.0.0 - 4.9.9 | ATOM 4B | Escalamiento (~4B parámetros) |

## Infraestructura

- **Desarrollo local**: PC principal para desarrollo y primeras pruebas
- **VPS**: 8GB RAM, 90GB almacenamiento — para entrenamiento de modelos mayores

## Filosofía

- 🧠 Modelo propio — no depende de otros para funcionar
- 📚 Conocimiento construido mediante entrenamiento real
- 🔥 Personalidad única y definida
- ⚙️ Capacidad de evolucionar a versiones superiores
- 🚀 Diseñado para crecer
