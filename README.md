# Creador de tests

Generador de exámenes tipo test a partir de archivos JSON, con preguntas y respuestas en orden aleatorio, corrección automática en el navegador y explicaciones opcionales.

Este repositorio es una versión independiente basada en [GRIA-TestCreator](https://github.com/AdanAgr/GRIA-TestCreator). Mantiene el reconocimiento a los autores y colaboradores del proyecto de origen y añade las modificaciones descritas a continuación.

## Modificaciones de esta versión

Cambios incorporados el **29 de septiembre de 2026**:

- **Archivo de configuración:** las carpetas, el número de exámenes, las preguntas por examen y el estilo se eligen desde `config.json`, sin editar `main.py`.
- **Varias carpetas por examen:** se pueden combinar preguntas de distintas asignaturas, temas o parciales.
- **Lectura de subcarpetas:** se buscan archivos de preguntas en todos los niveles de las carpetas seleccionadas, sin duplicar archivos cuando las rutas se solapan.
- **Explicaciones opcionales:** cada pregunta puede incluir el motivo de la respuesta correcta, que aparece después de corregir el examen. Los JSON anteriores siguen siendo compatibles.
- **Resolución de rutas:** las carpetas relativas se interpretan desde la ubicación de `config.json`, y las imágenes se buscan junto al JSON que las referencia.
- **Validación de la configuración:** se muestran errores cuando las carpetas no existen, los valores de configuración no son válidos o no se encuentran preguntas.

Se mantienen las preguntas de respuesta única y múltiple, las imágenes, la selección aleatoria, la corrección automática y los estilos `default`, `legacy` y `dark` del proyecto de origen.

## Requisitos y uso

Necesitas **Python 3.10 o superior** y un navegador con JavaScript habilitado. La generación de exámenes utiliza la biblioteca estándar de Python; no requiere instalar dependencias adicionales.

1. Descarga o clona este repositorio y abre una terminal en su carpeta.
2. Edita [config.json](config.json) para seleccionar las carpetas y las opciones del examen.
3. Ejecuta:

```bash
python main.py
```

En Windows también puedes usar `py main.py` si tienes instalado el lanzador de Python.

Los exámenes se guardan como `ExamenTest1.html`, `ExamenTest2.html`, etc., en la carpeta desde la que ejecutes el programa. Cuando generas un solo examen, se abre automáticamente en el navegador; si generas varios, abre el HTML que quieras resolver.

Responde a las preguntas y pulsa **Enviar respuestas** para ver la nota, las respuestas correctas y las explicaciones disponibles. Para generar un nuevo examen, vuelve a ejecutar el programa; se reutilizan los mismos nombres de archivo.

## Configuración

El archivo [config.json](config.json), situado junto a `main.py`, incluye inicialmente:

```json
{
  "folders": ["SIRE"],
  "numExams": 1,
  "numOfQuestions": 30,
  "style": "default"
}
```

| Campo | Descripción | Valor por defecto |
| --- | --- | --- |
| `folders` | Lista no vacía de carpetas que contienen preguntas. Admite rutas relativas a `config.json` y rutas absolutas. | Obligatorio |
| `numExams` | Número de exámenes que se generan; debe ser un entero mayor que cero. | `1` |
| `numOfQuestions` | Número total de preguntas de cada examen, combinando las carpetas seleccionadas; debe ser un entero mayor que cero. | `30` |
| `style` | Apariencia del examen: `default`, `legacy` o `dark`. | `"default"` |

Si solicitas más preguntas de las disponibles, el programa avisa y permite repeticiones.

### Carpetas y subcarpetas

Puedes organizar tus preguntas por asignatura, parcial o tema, por ejemplo:

```text
DXAR/
  Parcial1/
    Unit1.json
    imagenes/
      esquema.png
  Parcial2/
    Unit2.json
PIC/
  Unit2Students.json
```

| Selección en `folders` | Preguntas incluidas |
| --- | --- |
| `["DXAR"]` | Todos los parciales y subcarpetas de DXAR. |
| `["DXAR/Parcial1"]` | Solo el primer parcial y sus subcarpetas. |
| `["DXAR/Parcial1", "DXAR/Parcial2"]` | Ambos parciales. |
| `["DXAR/Parcial1", "PIC"]` | El primer parcial de DXAR y las preguntas de PIC. |

Estas rutas son ejemplos: crea las carpetas y sus archivos antes de seleccionarlas. Si incluyes una carpeta y una de sus subcarpetas, cada archivo se lee una sola vez.

## Crear archivos de preguntas

Guarda los archivos en **UTF-8**, con nombres que empiecen por `Unit`, `modulo` o `Final` y terminen en `.json`, como `Unit1.json`, `modulo1_2.json` o `Final1_1.json`. Se buscan también en las subcarpetas. Cada archivo contiene un objeto con la clave `questions` y una lista de preguntas.

Ejemplo completo con los dos tipos de pregunta:

```json
{
  "questions": [
    {
      "question": "¿Qué indica el overfitting?",
      "options": [
        "Que el modelo se ajusta demasiado a los datos de entrenamiento y generaliza mal.",
        "Que el modelo generaliza perfectamente a datos nuevos.",
        "Que el modelo no ha aprendido ningún patrón."
      ],
      "correct_option": 0,
      "questionType": "singleChoice",
      "explication": "El modelo se ha sobreajustado a los datos de entrenamiento, por lo que pierde capacidad de generalizar a datos nuevos."
    },
    {
      "question": "¿Cuáles de estos números son primos?",
      "options": ["2", "4", "5", "9"],
      "correct_options": [0, 2],
      "questionType": "multipleChoice",
      "explication": "El 2 y el 5 solo tienen dos divisores positivos: 1 y ellos mismos. El 4 y el 9 son compuestos."
    }
  ]
}
```

### Campos de cada pregunta

| Campo | Uso |
| --- | --- |
| `question` | Obligatorio. Texto del enunciado. |
| `options` | Obligatorio. Lista de textos con las opciones de respuesta. Utiliza al menos dos opciones distintas. |
| `questionType` | Obligatorio. `singleChoice` para respuesta única o `multipleChoice` para respuesta múltiple. |
| `correct_option` | Obligatorio en `singleChoice`. Índice de la opción correcta. |
| `correct_options` | Obligatorio en `multipleChoice`. Lista de índices de las opciones correctas. |
| `explication` | Opcional. Texto que explica la respuesta correcta; también se admite `explicacion`. |
| `images` | Opcional. Lista de rutas de imágenes relativas a la carpeta del JSON. |

Los índices empiezan en **0**: `correct_option: 0` indica la primera opción y `correct_options: [0, 2]` indica la primera y la tercera. Define los índices según el orden del JSON; el programa los actualiza al mezclar las respuestas.

### Explicaciones opcionales

La explicación aparece debajo de la respuesta correcta después de pulsar **Enviar respuestas**, tanto si se acierta como si se falla o se deja la pregunta sin responder. Si el campo no existe, es `null` o está vacío, no se muestra nada.

Puedes usar `explication` o `explicacion`; si aparecen ambos, tiene prioridad `explication`. El contenido se muestra como texto, no como HTML. Como las opciones se mezclan, las explicaciones deben referirse al contenido de las respuestas y no a sus letras o posiciones.

### Imágenes opcionales

Para incluir imágenes, añade un campo `images` al objeto de la pregunta, por ejemplo `"images": ["imagenes/esquema.png"]`.

Si la pregunta está en `DXAR/Parcial1/Unit1.json`, la imagen del ejemplo debe existir en `DXAR/Parcial1/imagenes/esquema.png`. Puedes incluir varias rutas en la lista u omitir `images` si la pregunta no necesita imágenes.

## Contribuir

Puedes proponer nuevas preguntas, corregir respuestas o mejorar el programa mediante issues y pull requests en este repositorio. Antes de enviar cambios, revisa el formato de los JSON y genera un examen para comprobar que las preguntas, las imágenes y las explicaciones se muestran correctamente.

Para formatear el código Python, instala las herramientas de desarrollo de [requirements.txt](requirements.txt) y ejecuta Black:

```bash
python -m pip install -r requirements.txt
python -m black .
```

## Créditos y licencia

Este proyecto deriva de [GRIA-TestCreator](https://github.com/AdanAgr/GRIA-TestCreator), el repositorio del que parte esta versión. Se reconoce el trabajo de sus autores y colaboradores en el código y en los bancos de preguntas.

Esta versión incorpora las modificaciones indicadas al inicio y mantiene la licencia **GNU General Public License v3.0 (GPLv3)** del proyecto de origen. Consulta [LICENSE](LICENSE) para leer sus términos completos.
