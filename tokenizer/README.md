# 📁 tokenizer/ — Procesamiento de Lenguaje

Gestiona cómo ATOM interpreta y procesa el lenguaje. El tokenizer es el traductor entre el texto humano y los números que el modelo entiende.

## Propósito

El tokenizer convierte texto en secuencias de números (tokens) que ATOM puede procesar, y viceversa. Es la puerta de entrada y salida del modelo: sin él, ATOM no puede leer ni escribir.

## ¿Qué es un Tokenizer?

```
Texto humano:  "Hola, ¿cómo estás?"
       ↓ Tokenizer
Tokens:        [15234, 234, 891, 4521, 234]
       ↓ Modelo ATOM
Procesamiento: [0.23, -0.45, 0.78, ...]
       ↓ Tokenizer
Texto humano:  "Estoy bien, gracias"
```

## Método: BPE (Byte-Pair Encoding)

ATOM utiliza **BPE**, el mismo método usado por GPT, LLaMA y Qwen.

### ¿Por qué BPE?

| Ventaja | Descripción |
|---------|-------------|
| Probado | Usado por los modelos más exitosos del mundo |
| Eficiente | Balance entre vocabulario y compresión |
| Multilenguaje | Maneja bien español e inglés |
| Flexible | Puede aprender nuevas palabras combinando subpalabras |

### ¿Cómo funciona BPE?

1. Empieza con caracteres individuales: `a`, `b`, `c`, ...
2. Encuentra los pares más frecuentes: `es` → `es`
3. Combina: `es` + `ta` → `esta`
4. Repite hasta tener un vocabulario de ~32k-50k tokens

## Vocabulario

| Característica | Valor |
|----------------|-------|
| Idiomas | Español + Inglés |
| Tamaño de vocabulario | 32,000 - 50,000 tokens |
| Tokens especiales | `<bos>`, `<eos>`, `<pad>`, `<unk>`, `<sep>` |

### Tokens especiales

| Token | Función |
|-------|---------|
| `<bos>` | Beginning of Sequence — inicio de texto |
| `<eos>` | End of Sequence — fin de texto |
| `<pad>` | Padding — relleno para igualar longitudes |
| `<unk>` | Unknown — token desconocido |
| `<sep>` | Separator — separador entre secciones |

## Estructura

```
tokenizer/
├── configs/              ← Configuraciones del tokenizer
│   ├── bpe-config.json   ← Configuración BPE principal
│   └── vocab-es-en.json  ← Vocabulario español-inglés
│
├── training/             ← Entrenamiento del tokenizer
│   ├── train_tokenizer.py← Script para entrenar desde cero
│   └── corpus/           ← Corpus de texto para entrenar
│       ├── es/           ← Textos en español
│       └── en/           ← Textos en inglés
│
├── vocabularies/         ← Vocabularios generados
│   ├── atom-bpe-32k.json ← Vocabulario de 32k tokens
│   └── atom-bpe-50k.json ← Vocabulario de 50k tokens
│
├── scripts/              ← Utilidades
│   ├── encode.py         ← Texto → tokens
│   ├── decode.py         ← Tokens → texto
│   └── analyze.py        ← Análisis de eficiencia
│
└── tests/                ← Pruebas del tokenizer
    ├── test_spanish.py   ← Pruebas en español
    ├── test_english.py   ← Pruebas en inglés
    └── test_edge_cases.py← Casos límite
```

## Proceso de Creación

```
1. Recopilar corpus de texto (español + inglés)
              ↓
2. Entrenar tokenizer BPE con corpus
              ↓
3. Generar vocabulario (32k-50k tokens)
              ↓
4. Probar con textos de ejemplo
              ↓
5. Ajustar si es necesario
              ↓
6. Guardar vocabulario final
```

## Métricas de Calidad

| Métrica | Objetivo | Descripción |
|---------|----------|-------------|
| Tokens por palabra | 1.5 - 2.5 | Menos tokens = más eficiente |
| Cobertura | >99% | Porcentaje de texto tokenizado correctamente |
| Equilibrio es/en | ~50/50 | Balance entre tokens de cada idioma |
| Sin `<unk>` | 0% | No debería generar tokens desconocidos |

## Ejemplo de Uso

```python
# Encoding (texto → tokens)
tokens = tokenizer.encode("Hola, ¿cómo estás?")
# Resultado: [15234, 234, 891, 4521, 234]

# Decoding (tokens → texto)
text = tokenizer.decode([15234, 234, 891, 4521, 234])
# Resultado: "Hola, ¿cómo estás?"
```

## Conexión con Otras Áreas

- **trainer/** usa el tokenizer para procesar datos antes de entrenar
- **models/** guarda el tokenizer junto al modelo para consistencia
- **data/** necesita el tokenizer para convertir texto en datos entrenables
- **src/** usa el tokenizer para las entradas y salidas del chatbot
