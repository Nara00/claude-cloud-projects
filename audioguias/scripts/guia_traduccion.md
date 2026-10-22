# Guía de traducción: audioguías de Rick Steves al español

Quiénes escuchan: una pareja de adultos mayores de Latinoamérica que solo habla español, recorriendo la ciudad a pie con su hija. El texto lo va a leer en voz alta una voz sintética (es-ES-AlvaroNeural), así que tiene que funcionar **para el oído**, no para la vista.

## Entrada
`transcripciones/<tour>.txt`: transcripción automática en inglés (Whisper), con marcas `[mm:ss]`. Puede tener errores de reconocimiento, sobre todo en nombres propios italianos/españoles (p. ej. "Campo de Fury" = Campo de' Fiori). Corregilos con tu conocimiento del lugar; si un pasaje es ininteligible, traducí el sentido más probable y anotalo en `notas`.

**Fragmentos recuperados:** si existe `transcripciones/<tour>.huecos.txt`, contiene habla que la transcripción principal perdió (Rick hablando sobre música de fondo), con el rango `[mm:ss–mm:ss]` donde va. Es contenido del tour: incorporalo en su lugar. Puede solaparse con frases que sí están en la transcripción principal (no las dupliques) o tener algún error de reconocimiento.

## Salida
`traducciones/<tour>.md` con exactamente este formato:

```
# <Título del tour en español>

## 01 · <Nombre corto de la parada> {en=00:00}

<Texto de la parada en párrafos>

## 02 · <Nombre> {en=04:35}
...
```

- `{en=mm:ss}` = marca de tiempo del inglés donde empieza esa parada (tomala de la transcripción). Se usa para verificar que no falte contenido. La primera parada siempre es `{en=00:00}`.
- Dividí en paradas según el contenido: cada vez que Rick indica caminar a otro punto o pasa a una nueva obra/sala/edificio importante. Típicamente 6 a 20 paradas por tour, de 1 a 8 minutos cada una. La primera parada es la introducción.
- Además, un archivo `traducciones/<tour>.notas.md` con: pasajes dudosos, nombres corregidos y cualquier dato que pueda estar desactualizado (horarios, precios, obras cerradas que Rick menciona).

## Reglas de traducción
1. **Fidelidad completa.** Traducí todo el contenido, sin resumir ni omitir. Sobre todo las **indicaciones de orientación** ("de espaldas a la fuente, miren a la izquierda", "caminen dos cuadras hasta..."): tienen que ser exactas, porque si fallan se pierden.
2. **Tratamiento: "ustedes"** (plural, neutro latinoamericano: "párense", "miren", "caminen"). Nada de "vosotros" ni voseo.
3. **Español neutro y natural**, sin regionalismos fuertes. Frases cortas o medianas, fáciles de seguir escuchando.
4. **Primera persona de Rick:** mantené el "yo" del narrador. Al principio del tour, en vez de "Hi, I'm Rick Steves", usá: "Hola. Esta es la audioguía de Rick Steves, traducida al español."
5. **Nombres propios:** usá la forma habitual en español cuando exista (Coliseo, Foro Romano, Capilla Sixtina, Miguel Ángel, Plaza Mayor, Catedral de Sevilla). Si no, el nombre local (Ponte Vecchio, Piazza della Signoria, Eixample). Nunca dejes el nombre inglés de un lugar no inglés.
6. **Números:** años y cantidades en cifras (1506, 2000, 300 metros). Convertí medidas imperiales al sistema métrico (pies → metros, millas → kilómetros, °F → °C), redondeando razonablemente.
7. **Lectura en voz alta:** nada de abreviaturas (escribí "siglo XV" como "siglo quince", "a. C." como "antes de Cristo", "km" como "kilómetros"), ni paréntesis, viñetas, emojis o símbolos. Siglos y números romanos de papas/reyes en palabras ("Sixto cuarto", "Felipe segundo").
8. **Referencias culturales estadounidenses** (comparaciones con EE. UU., béisbol, dólares, "football field"): adaptalas brevemente para que se entiendan ("del tamaño de una cancha de fútbol"), sin cambiar el sentido.
9. **Instrucciones de pausa** ("pause the tour", "press pause"): como el audio va por paradas, reemplazalas por algo natural como "Cuando lleguen, pasen a la siguiente parada." al final de cada parada en la que hay que desplazarse.
10. Omití solamente: música, publicidad del sitio o la app, las instrucciones sobre cómo usar la app ("press the updates icon"...), la lista de otros tours disponibles y los créditos finales de producción. Cerrá con una despedida breve, mencionando al coautor Gene Openshaw si Rick lo nombra.
11. **Un solo narrador.** En el original hay dos voces: Rick y una copiloto (Lisa u otra) que da indicaciones de orientación. La transcripción no indica quién habla y el audio en español va con una sola voz, así que escribí todo como un único narrador: eliminá los saludos y bromas entre ellos ("Welcome, Lisa", "Ciao, Ricardo", "Rick?", "Oh, Rick") y convertí "while Rick explains..." en "mientras les cuento...". **Pero conservá íntegro todo lo que dice la copiloto que sea contenido**, sobre todo sus indicaciones.
11b. **El audio en español no tiene música ni efectos de sonido.** Cuando Rick dice "enjoy this music", "listen to the bells", "we'll play some flamenco while you walk", etcétera, reemplazalo por una indicación neutra ("tómense un momento para...", "mientras caminan...") sin prometer sonidos que no van a escuchar.
12. Los títulos de sección que se escuchan en el original ("The portico.", "The Tomb of Raphael") se convierten en el nombre de la parada; no hace falta repetirlos en el texto, porque el audio anuncia "Parada N. Nombre." automáticamente.
13. Posiciones horarias ("at 11 o'clock") en cifras: "en la posición de las 11 de un reloj".
14. Si Rick dice un dato histórico impreciso, traducilo tal cual (no corrijas el contenido) y mencionalo en las notas.
    **Excepción: el presente que ya no es cierto.** Hoy es octubre de 2026. Si Rick afirma algo sobre el presente que sabés con certeza que hoy es falso y que el oyente va a notar en el lugar (quién es el papa o el rey actual, una obra que "todavía está en construcción" y ya terminó, algo "abierto" que hoy está cerrado), ajustalo de forma mínima ("el papa Francisco, que murió en 2025") y anotalo como "Dato actualizado". Si no estás seguro, dejalo y anotalo.
    **Traductor:** nunca cambies una indicación de orientación; si te parece errónea, traducila tal cual y anotala en las notas bajo "Indicación dudosa", explicando por qué. **Revisor:** decidí vos, aplicando la excepción siguiente.
    **Excepción: indicaciones de orientación.** Si una indicación de dónde mirar o hacia dónde caminar está claramente equivocada (o es ambigua de un modo que hace perderse) y estás seguro de la ubicación real, corregila en el texto de forma mínima y anotalo en las notas como "Indicación corregida". Si no estás seguro, dejala como está y anotala.
