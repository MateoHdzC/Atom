# 📁 src/ — Sistema ATOM

Contiene el desarrollo interno del sistema de ATOM. Incluye el chatbot por terminal (CLI) que permite a las personas conversar con ATOM.

## Propósito

Esta carpeta es el código que hace que ATOM sea usable. Mientras trainer/ entrena el modelo y models/ lo almacena, src/ es lo que permite a la gente interactuar con ATOM: chatear, hacer preguntas, obtener respuestas.

## Componentes

### 1. CLI — Chatbot por Terminal (PRINCIPAL)
La experiencia principal de ATOM: una conversación natural por línea de comandos. Sin HTML, sin web, sin frontend visual. Solo terminal.

```
$ atom chat
╔══════════════════════════════════════╗
║           ATOM v1.0.0                ║
║  Escribe 'salir' para terminar       ║
╚══════════════════════════════════════╝

> Hola, ¿cómo estás?
ATOM: Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?

> ¿Cuál es la capital de España?
ATOM: La capital de España es Madrid.

> salir
Hasta luego.
```

### 2. API (futuro — para integraciones)
Permitir que otras aplicaciones usen ATOM. No es prioridad ahora.

## Stack

| Componente | Tecnología | Por qué |
|------------|------------|---------|
| CLI Framework | Click / Typer | Simple y elegante para CLIs de Python |
| Inferencia | PyTorch + Transformers | Carga y ejecución del modelo |
| Formateo | Rich | Salida de terminal con colores y formato |

## Estructura

```
src/
├── atom/                   ← Paquete principal
│   ├── __init__.py
│   ├── core/               ← Núcleo del sistema
│   │   ├── model.py        ← Carga y gestión del modelo
│   │   ├── tokenizer.py    ← Gestión del tokenizer
│   │   └── inference.py    ← Motor de inferencia
│   │
│   ├── chatbot/            ← Lógica del chatbot
│   │   ├── __init__.py
│   │   ├── conversation.py ← Gestión de conversaciones
│   │   ├── personality.py  ← Personalidad de ATOM
│   │   └── memory.py       ← Memoria de conversación
│   │
│   └── cli/                ← Interfaz de línea de comandos
│       ├── __init__.py
│       ├── main.py         ← Punto de entrada CLI
│       └── commands/       ← Comandos
│           ├── chat.py     ← atom chat
│           └── model.py    ← atom model
│
├── config/                 ← Configuraciones
│   ├── settings.py         ← Configuración global
│   └── defaults.yaml       ← Valores por defecto
│
├── tests/                  ← Pruebas
│   ├── test_core.py
│   ├── test_chatbot.py
│   └── test_cli.py
│
├── requirements.txt        ← Dependencias
├── pyproject.toml          ← Configuración del proyecto
└── README.md               ← Este archivo
```

## Modo de Uso

### CLI (único modo actual)
```bash
# Chat interactivo
atom chat

# Chat con un mensaje
atom chat --message "¿Cuál es la capital de España?"

# Información del modelo
atom model info
```

> **Nota**: No hay interfaz web. ATOM es una IA que se usa por terminal, como chatear con una persona pero en la consola.

## Arquitectura del Chatbot

```
┌─────────────────────────────────────────────────┐
│                  CHATBOT ATOM                     │
├─────────────────────────────────────────────────┤
│                                                   │
│  Usuario escribe mensaje en terminal              │
│                    ↓                              │
│  CLI recibe mensaje                               │
│                    ↓                              │
│  Conversation Manager                             │
│  → Historial de conversación                      │
│  → Contexto de la sesión                          │
│                    ↓                              │
│  Personality Module                               │
│  → Tono de ATOM                                   │
│  → Estilo de respuesta                            │
│                    ↓                              │
│  Inference Engine                                 │
│  → Tokenizer: texto → tokens                      │
│  → Modelo: tokens → predicción                    │
│  → Tokenizer: predicción → texto                  │
│                    ↓                              │
│  Response Builder                                 │
│  → Formatear respuesta                            │
│  → Agregar personalidad                           │
│                    ↓                              │
│  Mostrar respuesta en terminal                    │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Conexión con Otras Áreas

- **models/** carga los modelos entrenados para usarlos
- **tokenizer/** se usa para procesar texto en el chatbot
- **evaluation/** puede integrarse para respuestas de respaldo
- **teachers/** puede usarse como fallback si ATOM no sabe algo
