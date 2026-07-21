# ATOM — Inteligencia Artificial Propia

## ¿Qué es ATOM?

ATOM es una inteligencia artificial creada desde cero por un desarrollador indie (solo, sin empresa detrás). No es un wrapper de modelos existentes ni una API que conecta con otros servicios. Es un modelo propio que nace, aprende y evoluciona con su propio cerebro.

```
Desarrollador indie
       ↓
    Crea ATOM
       ↓
Modelos profesores le enseñan
       ↓
ATOM aprende y crece
       ↓
ATOM funciona solo
```

## Objetivo

Crear una IA que sea **útil** y que **evolucione sola**. No busca competir con GPT, Claude, Gemini ni ningún otro modelo comercial. ATOM es un proyecto personal que apunta a ser grande, pero a su ritmo.

### Casos de uso principales

| Área | Descripción |
|------|-------------|
| **Conversación** | Mantener diálogos naturales, responder preguntas, ser un compañero de chat |
| **Programación** | Ayudar a escribir código, explicar conceptos, resolver problemas básicos |

## ¿Qué lo hace diferente?

### 1. Entrenado desde cero
ATOM no parte de un modelo existente. No es fine-tuning de LLaMA ni de Qwen. Es un modelo que nace con parámetros aleatorios y aprende todo desde cero, guiado por modelos profesores.

### 2. No compite
No busca ser mejor que GPT-4 ni reemplazar a nadie. Es un proyecto indie, personal, que crece a su propio paso. Si mañana decide no avanzar más, ATOM ya habrá sido una experiencia valiosa.

### 3. Modelos profesores como maestros
Otros modelos (Qwen y dos adicionales) actúan como profesores. No son el cerebro de ATOM — son los maestros que le enseñan:
- Generan datos de entrenamiento
- Evalúan las respuestas de ATOM
- Corregien errores y explican por qué
- Identifican áreas débiles y generan ejercicios

### 4. Desarrollador indie
No hay equipo de 100 personas, ni millones de dólares de inversión, ni datacenters masivos. Hay una persona con una visión, una PC y una VPS. Eso lo hace diferente por definición.

### 5. Local y privado
ATOM funciona localmente. Tus conversaciones no se van a ningún servidor externo. Tu data es tuya.

## ATOM 1B — Versión Inicial

### ¿Qué es?

ATOM 1B es la primera versión del modelo. Tiene aproximadamente **1.000 millones de parámetros** (1B = 1 billion).

### ¿Qué puede hacer?

| Capacidad | Nivel esperado |
|-----------|----------------|
| Mantener conversación | ✅ Natural y coherente |
| Responder preguntas medias | ✅ Conocimiento general |
| Programación básica | ✅ Código simple, explicaciones |
| Razonamiento lógico | ⚠️ Limitado (suficiente para empezar) |
| Matemáticas complejas | ❌ No en esta versión |

### Meta de rendimiento

**90% de respuestas correctas** en preguntas de conocimiento general.

Esto significa que de cada 10 preguntas que le hagas, 9 debería responderlas bien. No busca perfección — busca ser útil.

### Especificaciones técnicas

| Característica | Valor |
|----------------|-------|
| Parámetros | ~1.000 millones |
| Idiomas | Español + Inglés |
| Contexto | 2048 tokens |
| Interfaz | CLI (terminal) |
| Framework | PyTorch + HuggingFace Transformers |

## Hoja de Ruta — Evolución

```
ATOM 1B (ahora)
    ↓
ATOM 2B (más grande, más conocimiento)
    ↓
ATOM 3B (mejor razonamiento)
    ↓
ATOM 4B (programación avanzada)
    ↓
ATOM 5B (acceso a internet, más capacidades)
    ↓
ATOM 6B+ (se definirá según el avance)
```

### Evolución por versión

| Versión | Parámetros | Capacidades nuevas |
|---------|------------|-------------------|
| **1B** | ~1.000M | Conversación, preguntas medias, código básico |
| **2B** | ~2.000M | Mejor razonamiento, más conocimiento |
| **3B** | ~3.000M | Programación intermedia, mejor coherencia |
| **4B** | ~4.000M | Programación avanzada, mejor razonamiento |
| **5B** | ~5.000M | Acceso a internet, lectura de código, mejoras autónomas |
| **6B+** | Por definir | Se decidirá según el avance del proyecto |

### Capacidades futuras (a partir de 5B)

| Capacidad | Descripción |
|-----------|-------------|
| **Ver imágenes** | Analizar y describir imágenes |
| **Navegar internet** | Buscar información en tiempo real |
| **Leer código** | Analizar código existente y sugerir mejoras |
| **Mejorar código** | Reescribir código para que sea más eficiente o limpio |
| **Ayudar en tareas** | Asistir en tareas complejas paso a paso |

## Filosofía

### Lo que ATOM es
- Un modelo propio, con su propio cerebro
- Un proyecto indie que crece a su ritmo
- Una IA útil para conversación y programación
- Un modelo que aprende de otros modelos, pero no depende de ellos

### Lo que ATOM no es
- Un competidor de GPT, Claude o Gemini
- Un wrapper de modelos existentes
- Un proyecto de empresa
- Una IA perfecta (al menos no al principio)

### Principios

1. **Aprender desde cero** — No atajos, no dependencias
2. **Evolucionar solo** — Los profesores enseñan, ATOM aprende
3. **Ser útil** — No buscar perfección, buscar servir
4. **Crecer a su ritmo** — Sin prisa, sin presión
5. **Ser local** — Tu data es tuya

## Infraestructura

| Recurso | Uso |
|---------|-----|
| **PC local** | Desarrollo, pruebas, entrenamiento de 1B-2B |
| **VPS (8GB RAM, 90GB)** | Entrenamiento de modelos mayores (3B+) |

## Stack Técnico

| Componente | Tecnología |
|------------|------------|
| Framework | PyTorch + HuggingFace Transformers |
| Tokenizer | BPE (32k-50k tokens) |
| Interfaz | CLI (terminal) |
| Modelos profesores | Qwen + 2 modelos locales via Ollama |

---

*ATOM no es perfecto. ATOM no es el mejor. ATOM es propio. Y eso es lo que lo hace especial.*
