# Creador de tests

## Resumen

Esto es un programa que crea exámenes tipo tests eligiendo las preguntas y poniendo el orden de las respuestas de manera aleatoria. Una vez generado el html se puede responder al examen y se autocorrige y da la nota que se ha sacado.

## Uso

Para generar exámenes, edita [config.json](/config.json) y ejecuta `python main.py`. Ya no es necesario modificar el código de `main.py`.

```json
{
  "folders": ["SIRE"],
  "numExams": 1,
  "numOfQuestions": 30,
  "style": "default"
}
```

- `folders`: Lista de carpetas de preguntas. Las rutas relativas se interpretan desde la carpeta de `config.json`; también se admiten rutas absolutas.
- `numExams`: Número de exámenes que se generan (por defecto, 1).
- `numOfQuestions`: Número total de preguntas por examen, combinando todas las carpetas seleccionadas (por defecto, 30).
- `style`: Estilo del examen: `default`, `legacy` o `dark` (por defecto, `default`).

Se buscan archivos `Unit*.json` en cada carpeta y en todas sus subcarpetas. Por ejemplo, puedes organizar las preguntas así:

```text
DXAR/
  Parcial1/
    Unit1.json
  Parcial2/
    Unit2.json
```

Con `"folders": ["DXAR"]` se incluyen ambos parciales; con `"folders": ["DXAR/Parcial1"]` se incluye solo el primero. También puedes combinar carpetas, por ejemplo `"folders": ["DXAR/Parcial1", "PIC"]`. Si seleccionas una carpeta y una de sus subcarpetas, cada archivo se lee una sola vez.

Las imágenes de cada pregunta se buscan respecto a la carpeta del JSON que la contiene. Los exámenes se guardan como `ExamenTest1.html`, `ExamenTest2.html`, etc., en la carpeta desde la que ejecutes el programa; si generas uno solo, se abre automáticamente en el navegador. Si solicitas más preguntas de las disponibles, se permiten repeticiones, como antes.

## Contribuir

**Importante:** Al hacer un pull request se realiza una comprobación de formateo que para pasarla deben estar los ficheros con un formato en específico. La mejor manera de asegurarse de que esto siempre ocurra es ejecutar la acción sobre formateo en el fork que has creado. Es necesario que sea en el fork; y solo se necesita una vez manualmente, ya que se ejecuta cada vez que haya un cambio en el fork. No se ejecuta de manera automática inicialmente por razones de seguridad en GitHub.

La manera fácil de contribuir es añadiendo más preguntas. Estas se encuentran en los ficheros .json que hay en la carpeta de cada asignatura. Los ficheros tienen que seguir el formato de empezar por `Unit` y acabar por `.json`. Cada fichero es un diccionario con una única clave `questions` cuyo valor es una lista de diccionarios. Más bajo se explica cada tipo de pregunta que está implementado. Antes de subir una pregunta nueva asegúrate de que está bien escrita, la respuesta es la correcta y que el programa sigue funcionando.

Para añadir tus cambios haz un fork con el nombre de la asignatura a la que quieres añadir preguntas y añade las preguntas. Luego haz un pull request y si todo está bien se añadirá al programa.

### `singleChoice`

Tiene que tener las siguientes claves:

- `question`: La pregunta que se quiere hacer.
- `options`: Una lista de strings con las opciones de respuesta.
- `correct_option`: Un entero que indica el índice de la lista de opciones que es la correcta. Este índice está en base 0.
- `questionType`: Un string que indica el tipo de pregunta. Tiene que ser `singleChoice` para este tipo de pregunta.

### `multipleChoice`

Tiene que tener las siguientes claves:

- `question`: La pregunta que se quiere hacer.
- `options`: Una lista de strings con las opciones de respuesta.
- `correct_options`: Una lista de enteros que indica los índices de la lista de opciones que son correctas. Estos índices están en base 0.
- `questionType`: Un string que indica el tipo de pregunta. Tiene que ser `multipleChoice` para este tipo de pregunta.

### Explicación opcional

Las preguntas `singleChoice` y `multipleChoice` pueden incluir un campo `explication` con un texto que explique la respuesta correcta. También se admite `explicacion`; si se incluyen ambos campos, se usa `explication`.

La explicación aparece debajo de la respuesta correcta únicamente después de pulsar **Enviar respuestas**, tanto si se acierta como si se falla o se deja la pregunta sin responder. Si el campo no existe, es `null` o está vacío, no se muestra nada y los JSON antiguos siguen funcionando sin cambios. El contenido se muestra como texto, no como HTML.

Ejemplo de pregunta con explicación:

```json
{
  "question": "¿Qué indica el overfitting?",
  "options": [
    "Que el modelo se ajusta demasiado a los datos de entrenamiento y generaliza mal.",
    "Que el modelo generaliza perfectamente a datos nuevos."
  ],
  "correct_option": 0,
  "questionType": "singleChoice",
  "explication": "El overfitting indica que el modelo se ha sobreajustado a los datos de entrenamiento, por lo que pierde capacidad de generalizar."
}
```

### Contribuir avanzado

Si quieres cambiar el código para mejorarlo o refactorizarlo, abre un issue y hablamos si los cambios que propones son útiles para este proyecto.
