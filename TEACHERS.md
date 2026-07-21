# TEACHERS.md — Modelos Profesores de ATOM

## ¿Qué son los profesores?

Los modelos profesores son los **maestros** de ATOM. No son el cerebro — son quienes le enseñan. Generan datos, evalúan respuestas, corrigen errores y ayudan a que ATOM aprenda.

```
Profesor 1 (Chat)         Profesor 2 (Código)       Profesor 3 (Matemáticas)
     ↓                          ↓                          ↓
 Genera conversaciones     Genera ejercicios de código   Genera problemas de matemáticas
 Evalúa respuestas         Evalúa código                 Evalúa soluciones
 Corrige errores           Corrige bugs                  Corrige cálculos
     ↓                          ↓                          ↓
     └──────────────────────────┼──────────────────────────┘
                                ↓
                        ATOM 1B aprende
```

## Los 3 Profesores

### Profesor 1 — Chat (Conversación)

| Característica | Valor |
|----------------|-------|
| **Modelo** | Qwen2.5:7b |
| **Tamaño** | ~4GB |
| **Especialidad** | Conversación, comunicación, personalidad |
| **Instalación** | `ollama pull qwen2.5:7b` |

**¿Qué enseña?**

| Área | Descripción |
|------|-------------|
| Conversación natural | Hablar como una persona, no como un robot |
| Adaptación de tono | Ser gracioso, serio, empático, directo según la situación |
| Preguntas y respuestas | Responder preguntas de conocimiento general |
| Personalidad | Tener opiniones, estilo propio, forma de hablar definida |
| Contexto | Recordar lo que se habló antes en la conversación |
| Manejo de emociones | Responder apropiadamente según el estado del usuario |

**Tipos de preguntas que genera:**

```
- "Hola, ¿cómo estás?"
- "Cuéntame un chiste"
- "¿Qué opinas sobre [tema]?"
- "Explícame [concepto] como si tuviera 10 años"
- "Estoy triste, ¿puedes ayudarme?"
- "¿Cuál es tu color favorito?"
```

---

### Profesor 2 — Código (Programación)

| Característica | Valor |
|----------------|-------|
| **Modelo** | DeepSeek-Coder:6.7b |
| **Tamaño** | ~4GB |
| **Especialidad** | Programación, código, debugging |
| **Instalación** | `ollama pull deepseek-coder:6.7b` |

**¿Qué enseña?**

| Área | Descripción |
|------|-------------|
| Escribir código | Crear código desde cero en varios lenguajes |
| Explicar código | Explicar qué hace un código línea por línea |
| Debugging | Encontrar y arreglar errores en código |
| Mejores prácticas | Código limpio, eficiente, mantenible |
| Múltiples lenguajes | Python, JavaScript, TypeScript, Java, C, Go, Rust |
| Resolución de problemas | Algoritmos, estructuras de datos, lógica |

**Lenguajes soportados:**

| Lenguaje | Nivel |
|----------|-------|
| Python | Avanzado |
| JavaScript/TypeScript | Avanzado |
| Java | Intermedio |
| C/C++ | Intermedio |
| Go | Intermedio |
| Rust | Básico |
| SQL | Intermedio |
| HTML/CSS | Avanzado |

**Tipos de preguntas que genera:**

```
- "Escribe una función que ordene una lista"
- "¿Qué hace este código? [código]"
- "Encuentra el error en este código [código]"
- "¿Cómo hago [tarea] en Python?"
- "Optimiza este código [código]"
- "Crea una API REST en FastAPI"
```

---

### Profesor 3 — Matemáticas

| Característica | Valor |
|----------------|-------|
| **Modelo** | Qwen2.5-Math:7b |
| **Tamaño** | ~4GB |
| **Especialidad** | Matemáticas, razonamiento lógico, cálculo |
| **Instalación** | `ollama pull qwen2.5-math:7b` |

**¿Qué enseña?**

| Área | Descripción |
|------|-------------|
| Aritmética | Sumas, restas, multiplicaciones, divisiones |
| Álgebra | Ecuaciones, variables, polinomios |
| Geometría | Áreas, perímetros, teoremas |
| Trigonometría | Seno, coseno, tangente |
| Cálculo | Derivadas, integrales, límites |
| Estadística | Media, mediana, desviación estándar, probabilidad |
| Razonamiento lógico | Problemas de lógica, deducción |
| Explicación paso a paso | No solo la respuesta, sino el proceso |

**Niveles de dificultad:**

| Nivel | Ejemplo |
|-------|---------|
| Básico | 2 + 2 = ? |
| Intermedio | Resuelve: 2x + 5 = 15 |
| Avanzado | Calcula la derivada de f(x) = x³ + 2x |
| Explicación | "¿Por qué la derivada de x² es 2x?" |

**Tipos de preguntas que genera:**

```
- "¿Cuánto es 15 × 23?"
- "Resuelve: 3x² + 2x - 5 = 0"
- "¿Cuál es el área de un círculo con radio 5?"
- "Calcula la integral de x² dx"
- "¿Qué es la desviación estándar?"
- "Explica paso a paso cómo resolver esta ecuación"
```

---

## Distribución de Datos

Los 3 profesores generan datos en partes iguales para alcanzar **~1.000 millones de parámetros** (1B).

| Profesor | Datos generados | Preguntas aprox. |
|----------|-----------------|------------------|
| Chat (Qwen) | ~33% | ~33 millones |
| Código (DeepSeek) | ~33% | ~33 millones |
| Matemáticas (Qwen-Math) | ~33% | ~33 millones |
| **Total** | **100%** | **~100 millones** |

> **Nota**: 100 millones de ejemplos de entrenamiento es suficiente para un modelo de 1B parámetros. No se necesitan miles de millones.

## Infraestructura Requerida

| Componente | VPS (8GB RAM) | PC desarrollo |
|------------|---------------|---------------|
| RAM | 8GB ✅ | 16GB+ |
| Almacenamiento | 90GB ✅ | 50GB+ |
| GPU | No requerida | Opcional (NVIDIA 8GB+) |
| CPU | 4+ cores | 4+ cores |

### Estrategia de ejecución: 1x1 (un profesor a la vez)

Los profesores se ejecutan **uno a la vez**, no los 3 simultáneamente. Esto permite usar modelos de 7b en una VPS de 8GB RAM sin problemas.

```
Día 1: Profesor Chat (Qwen 7b)     → genera 33M ejemplos → se descarga
Día 2: Profesor Código (DeepSeek)  → genera 33M ejemplos → se descarga
Día 3: Profesor Matemáticas (Math) → genera 33M ejemplos → se descarga
```

**RAM necesaria por modelo**: ~5GB (modelo 4GB + overhead del sistema)
**RAM disponible en VPS**: 8GB → sobra para un modelo a la vez

**Tamaño de los modelos**: ~4GB cada uno (se descargan y eliminan uno a la vez)

## Instalación

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Instalar un profesor a la vez (no los 3 juntos)
# Día 1: Chat
ollama pull qwen2.5:7b
# ... generar datos ...
ollama rm qwen2.5:7b

# Día 2: Código
ollama pull deepseek-coder:6.7b
# ... generar datos ...
ollama rm deepseek-coder:6.7b

# Día 3: Matemáticas
ollama pull qwen2.5-math:7b
# ... generar datos ...
ollama rm qwen2.5-math:7b
```

## Flujo de Enseñanza

```
┌─────────────────────────────────────────────────────────┐
│                CICLO DE ENSEÑANZA                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Profesor genera pregunta/ejercicio                   │
│                    ↓                                     │
│  2. ATOM intenta responder                               │
│                    ↓                                     │
│  3. Profesor evalúa la respuesta                         │
│     → ¿Correcto? (sí/no)                                │
│     → ¿Coherente? (sí/no)                               │
│     → ¿Completa? (sí/no)                                │
│                    ↓                                     │
│  4. Si incorrecto: Profesor corrige                      │
│     → Respuesta correcta                                 │
│     → Explicación del por qué                           │
│     → Proceso paso a paso (matemáticas)                  │
│                    ↓                                     │
│  5. ATOM aprende de la corrección                        │
│                    ↓                                     │
│  6. Repetir con siguiente pregunta                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Coordinación entre Profesores

Los profesores trabajan de forma independiente, pero el sistema de evaluación coordina:

| Situación | Acción |
|-----------|--------|
| ATOM responde bien | Profesor marca como correcto, pasa a siguiente |
| ATOM responde mal | Profesor corrige y genera ejercicios similares |
| ATOM mejora en área | Profesor aumenta dificultad |
| ATOM empeora | Profesor genera ejercicios de refuerzo |

## Conexión con Otras Áreas

- **data/** almacena los datos generados por los profesores
- **evaluation/** usa los profesores para evaluar a ATOM
- **trainer/** usa los datos generados para entrenar
- **teachers/** contiene las configuraciones y prompts de los profesores

---

*Los profesores no son el cerebro de ATOM. Son los maestros que forman ese cerebro.*
