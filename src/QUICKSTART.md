# ATOM - Quick Start Guide

## Instalación

```bash
# 1. Instalar dependencias
cd src
pip install -r requirements.txt

# 2. Entrenar modelo de prueba
python scripts/train.py --epochs 3 --batch-size 4

# 3. Probar el modelo
python scripts/test_model.py

# 4. Chatear con el modelo
python scripts/test_model.py --chat
```

## Scripts

| Script | Descripción |
|--------|-------------|
| `train.py` | Entrena el modelo |
| `test_model.py` | Prueba el modelo o chatea con él |

## Estructura

```
src/
├── atom/               ← Paquete principal
│   ├── core/           ← Modelo, tokenizer, inferencia
│   ├── chatbot/        ← Lógica del chatbot
│   └── cli/            ← Interfaz de línea de comandos
├── config/             ← Configuraciones de entrenamiento
├── scripts/            ← Scripts de entrenamiento y prueba
├── tests/              ← Pruebas
└── requirements.txt    ← Dependencias
```

## Comandos

```bash
# Entrenar con configuración personalizada
python scripts/train.py --config config/atom-1b.yaml

# Entrenar con parámetros directos
python scripts/train.py --epochs 5 --batch-size 8

# Probar modelo
python scripts/test_model.py --model ./models/atom-1b

# Chatear
python scripts/test_model.py --chat --model ./models/atom-1b
```
