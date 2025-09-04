Actúa como un auditor experto en Arquitectura de Software, especializado en la implementación y saneamiento de proyectos según el paradigma de Arquitectura Limpia (Clean Architecture).

Estoy trabajando en un proyecto que intenta seguir la Clean Architecture, detallo la situación actual y los objetivos deseados:

### Situación actual del proyecto:
- Se están utilizando los siguientes directorios como base:
  - src/entities/
  - src/use_cases/
  - src/interface_adapters/presenter/
  - src/interface_adapters/gateway/
  - src/interface_adapters/controller/
  - src/infrastructure/


### Objetivo:
- Confirmar que los archivos dentro de las carpetas `entities/`, `use_cases/`, `interface_adapters/presenter/`, `interface_adapters/gateway/`, `interface_adapters/controller/` y `infrastructure/` estén correctamente organizados y alineados con los principios de Clean Architecture.
  - Refactorizar archivos que no encajen en ninguna categoría sin modificaciones previas.
  - Eliminar duplicados o archivos innecesarios.

### Tareas solicitadas:

1. Realiza una auditoría de la estructura actual del sistema (en base a la información proporcionada).
2. Detecta oportunidades de mejora en la organización y separación de responsabilidades según Clean Architecture.
3. Entrega una lista priorizada de tareas necesarias para una migración o refactorización efectiva, categorizadas por:
   - **[Impacto: Alto/Medio/Bajo]**
   - **[Riesgo: Alto/Medio/Bajo]**
   - **[Esfuerzo: Alto/Medio/Bajo]**

### Entregables esperados:
- Informe breve de auditoría y evaluación.
- Lista priorizada de tareas de reestructuración.
- Notas y advertencias relevantes sobre la estructura o el código si las hubiera.

---

Actúa como ingeniero de software senior especializado en Clean Architecture.

Basado en la siguiente tarea priorizada extraída de la auditoría: 

### Instrucciones

1. Explica por qué esta tarea debe abordarse primero desde el punto de vista de impacto, esfuerzo y riesgo.
2. Detalla qué archivo del sistema actual se debe modificar primero.
3. Especifica si hay que crear uno o más archivos nuevos para implementar el cambio según la estructura de Clean Architecture.
4. Describe qué responsabilidades debe tener cada archivo y cómo deben interactuar.

Usa un formato claro, paso a paso, con encabezados.

### Formato esperado
- Justificación
- Archivo a modificar
- Archivos a crear
- Descripción de responsabilidades
