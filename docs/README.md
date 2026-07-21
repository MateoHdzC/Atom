# 📁 docs/ — Documentación del Proyecto

Almacena toda la documentación, ideas, diseños y planificación del proyecto ATOM.

## Propósito

Esta carpeta es la memoria escrita del proyecto. Contiene decisiones de diseño, planificación, guías y referencia para que cualquier persona (o el futuro tú) pueda entender por qué se hicieron las cosas de cierta manera.

## Estructura

```
docs/
├── architecture/           ← Decisiones de arquitectura
│   ├── decisions/          ← ADRs (Architecture Decision Records)
│   │   ├── 001-framework.md
│   │   ├── 002-tokenizer.md
│   │   └── template.md
│   └── diagrams/           ← Diagramas del sistema
│       ├── system-overview.md
│       └── training-pipeline.md
│
├── guides/                 ← Guías de uso
│   ├── setup.md            ← Cómo configurar el entorno
│   ├── training.md         ← Cómo entrenar un modelo
│   ├── evaluation.md       ← Cómo evaluar un modelo
│   └── deployment.md       ← Cómo desplegar ATOM
│
├── planning/               ← Planificación del proyecto
│   ├── roadmap.md          ← Hoja de ruta general
│   ├── milestones.md       ← Hitos y objetivos
│   └── backlog.md          ← Tareas pendientes
│
├── design/                 ← Diseños técnicos
│   ├── model-architecture.md  ← Diseño de la arquitectura del modelo
│   ├── training-pipeline.md   ← Diseño del pipeline de entrenamiento
│   └── evaluation-system.md   ← Diseño del sistema de evaluación
│
├── references/             ← Material de referencia
│   ├── papers.md           ← Papers relevantes
│   ├── resources.md        ← Recursos útiles
│   └── glossary.md         ← Glosario de términos
│
└── changelog/              ← Registro de cambios
    └── CHANGELOG.md        ← Historial de cambios del proyecto
```

## Tipos de Documentación

### Architecture Decision Records (ADRs)
Documentan decisiones técnicas importantes con su contexto, opciones consideradas y rationale.

```markdown
# ADR-001: Framework de Entrenamiento

## Estado: Aceptado
## Contexto
Necesitamos un framework para entrenar ATOM desde cero.
## Decisión
PyTorch + HuggingFace Transformers.
## Rationale
- Estándar de la industria
- Gran comunidad
- Optimizado para modelos de lenguaje
```

### Guías
Instrucciones paso a paso para tareas comunes.

### Planificación
Documentos de planificación que definen la dirección del proyecto.

### Diseños
Especificaciones técnicas detalladas de componentes del sistema.

## Convenciones de Escritura

| Elemento | Convención |
|----------|------------|
| Idioma | Inglés para nombres técnicos, español para explicaciones |
| Formato | Markdown |
| Nombres | lowercase-with-dashes.md |
| Encabezados | Jerarquía clara (H1 → H2 → H3) |
| Diagramas | Mermaid o ASCII art |

## Conexión con Otras Áreas

- **Todas las áreas** contribuyen documentación aquí
- Las decisiones de diseño en docs/ guían la implementación en src/, trainer/, etc.
- Los ADRs documentan por qué se tomaron ciertas decisiones
