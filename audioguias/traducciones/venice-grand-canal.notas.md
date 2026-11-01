# Notas: Venecia, paseo en barco por el Gran Canal

## División en paradas
- Hay 18 paradas, una por cada pista del original. Cada pista empieza con un título hablado, que casi siempre es el nombre de la parada del vaporetto: Ferrovia, Riva de Biasio, San Marcuola, San Stae, Ca' d'Oro, Rialto Mercato, Rialto, San Silvestro, Sant'Angelo, San Tomà, Ca' Rezzonico, Accademia, Santa Maria del Giglio, Salute, San Marco y San Zaccaria. Las paradas llevan esos mismos nombres para que coincidan con los carteles de los muelles.
- No dividí más, por ejemplo en el Puente de Rialto o en la Ca' Foscari, porque el original no tiene ahí ninguna indicación de cambiar de pista. Cortar en esos puntos obligaría a tocar "siguiente" en momentos que Rick no marcó, mientras el barco avanza.

## Transcripción de Gemini: las marcas de tiempo no son tiempos reales
- Las marcas {en=} se tomaron tal cual de la transcripción, como se pidió, y coinciden con el título hablado de cada pista. Pero no son tiempos reales del MP3. El script corta el audio en tramos de 10 minutos, y Gemini devolvió los tiempos en formato de minutos y segundos escrito como número, por ejemplo 101 para 1:01, y el script los sumó como si fueran segundos. Por eso las marcas retroceden: la parada 06 está en 10:30 después de la 05, que está en 14:08; la 10 está en 20:17 después de la 09, en 22:39; y la 15 está en 32:34 después de la 14, en 35:16. Además, superan la duración real: el MP3 dura 40:04 y la transcripción llega a 45:55.
- Tiempos reales aproximados del comienzo de cada parada en el MP3 en inglés, calculados como el inicio del tramo más los minutos y segundos que dio Gemini: 01, 00:00; 02, 02:01; 03, 05:09; 04, 07:15; 05, 08:48; 06, 10:30; 07, 12:21; 08, 14:44; 09, 17:59; 10, 20:17; 11, 23:01; 12, 25:02; 13, 27:01; 14, 29:16; 15, 31:54; 16, 33:48; 17, 35:58; 18, 38:31. El tour termina en 39:58.
- No se perdió texto en los cortes entre tramos: las frases siguen sin saltos ("Two centuries ago, Venice was" y "Europe's Las Vegas"; "And as a person..." y "She lived larger than life"). Con los tiempos corregidos, los silencios de más de 8 segundos caen en la música que separa las pistas.
- La última línea de la transcripción, "[40:00] The first thing you'll notice is the massive stone wall that surrounds the city", no es de este tour. Gemini la inventó a partir del último tramo, que dura 4 segundos y está en silencio. Se omitió.
- Lo más probable es que pase lo mismo con las otras transcripciones de Venecia hechas con scripts/transcribir_gemini.py. La de los Frari también tiene marcas que retroceden.

## Correcciones de la transcripción automática
- "Mercato Rialto" pasó a Rialto Mercato, que es el nombre de la parada en los carteles del vaporetto. Puede que Rick haya dicho "Mercato Rialto"; se usó el nombre que van a ver.
- "the sad arch of the bridge": seguramente es "stout arch", el sólido arco. Se tradujo como "el gran arco del puente".
- "Rio Nuovo, Rio Terra" pasó a Rio Nuovo, Rio Terà. Es dudoso: en Venecia, un "rio terà" es un canal rellenado y convertido en calle, no un canal con agua. Puede ser un error de reconocimiento de otro nombre. Se dejó así.
- "Ciao, Gesu!" pasó a "¡Ciao, Gesù!", y se agregó "¡Hola, Jesús!" para que se entienda.
- "There are a couple of sites visible": es "sights", cosas para ver.
- "the conductor" del vaporetto: se tradujo como "el marinero", que es quien atiende el muelle y la pasarela.
- Los demás nombres de paradas y palacios están bien transcritos.

## Nombres identificados, no agregados al texto
- El casino es la Ca' Vendramin Calergi.
- La Lonja de los Turcos es el Fondaco dei Turchi, hoy Museo de Historia Natural. La Lonja de los Alemanes es el Fondaco dei Tedeschi.
- El edificio de los tribunales en Rialto Mercato son las Fabbriche Nuove di Rialto.
- Los dos palacios del gobierno municipal son la Ca' Loredan y la Ca' Farsetti.
- El museo de la Ca' Pesaro es la Galería Internacional de Arte Moderno; la galería de la Ca' d'Oro es la Galleria Giorgio Franchetti.
- La estatua del hombre a caballo de Marino Marini, en la Colección Guggenheim, es "El ángel de la ciudad".
- La antigua Aduana es la Punta della Dogana, hoy museo de arte contemporáneo de la colección Pinault.
- La antigua Casa de la Moneda es la Zecca. Las columnas son las de San Marcos y San Teodoro. Las figuras de la Torre del Reloj son los llamados Moros.
- Los Jardines Públicos son los Giardini. La Riva es la Riva degli Schiavoni. El puente que está delante del Puente de los Suspiros es el Ponte della Paglia.
- La parada que Rick llama San Marco se llama en los carteles San Marco Vallaresso.

## Un solo narrador: diálogos eliminados o adaptados
- Se eliminaron: la presentación de Lisa ("To help us along the way, I've invited... Buongiorno, Lisa", "Ahoy there, matey", "Ahoy", "Lisa will give us helpful directions..."); "You're the captain"; "Rick?"; "Got it"; "Like me" y "Ha!" después de "Decaying, but still beautiful"; y "We're just cruising down the river", "Yeah" y "Nice".
- "Like me" se eliminó porque no queda claro quién lo dice: parece una broma entre los dos. Además, en español quedaría raro con "hermosa".
- Se adaptaron conservando el contenido: "Then, Lisa will direct us from there" se unió con la indicación siguiente de la copiloto; "Keep on listening to Rick's commentary" pasó a "sigan escuchando"; "get a head start on Rick's commentary" pasó a "conviene empezar a escucharla con tiempo"; "let Rick say his goodbyes" pasó a "para la despedida"; "And as a person..." se unió con la frase siguiente.
- Parada 15: "stand up in the bow and block his view. Actually, let's don't and say we did" se tradujo como "podrían pararse en la proa y taparle la vista. Es broma: mejor no lo hagan". En un barco en movimiento, una persona mayor podría tomarlo como una instrucción, así que conviene que la broma quede clarísima.

## Sin música ni sonidos
- Parada 08: se omitió el canto "Volare, oh, oh, cantare..." bajo el Puente de Rialto, que en el original funciona como efecto de sonido. Quedó "Los gondoleros aprovechan al máximo su acústica para cantar"; se agregó "para cantar" para conservar el sentido sin el canto.
- "Enjoy a little music as you cruise", "let's listen to a little more music" y "how about a little more cruising music?" se reemplazaron por "disfruten del paseo".

## Sincronización con el barco
- Las instrucciones "start the next track" y "pause and restart it when..." pasaron a "pasen a la siguiente parada de la audioguía", y se respetó exactamente el momento indicado: cuando el barco sale del muelle, en las paradas 02, 03, 12, 13 y 14; cuando el barco llega o se acerca, en las 04, 05, 07, 09, 10, 11 y 16; cuando tengan una buena vista de la Ca' d'Oro, en la 06; enseguida, sin esperar, en la 08 y la 15; y al bajar a tierra, en la 17.
- En este tour, "parada" puede ser la del vaporetto o la de la audioguía. Para no confundir, siempre se dice "la siguiente parada de la audioguía" para la app y "la próxima parada del vaporetto" o "el muelle" para el barco.
- Parada 02: se omitió "using the high-speed function", porque es una función de la app original.
- Parada 04: a "this time, restart it just as the boat is reaching the next stop" se le agregó "sin esperar a que vuelva a salir", para dejar explícito el contraste con las paradas anteriores.

## Omitido
- Las instrucciones para ver las actualizaciones en la app, de 02:10 a 02:36.
- Al final: la lista de otras audioguías de Venecia, la publicidad de la guía de viaje y del sitio web, y el crédito de producción. Se dejó el agradecimiento a Gene Openshaw.
- La línea final inventada por Gemini.
- Parada 04: "brown and white UPS boats" pasó a "los barcos marrones y blancos de una empresa de mensajería". La voz sintética podría leer "UPS" como una interjección.

## Adaptaciones culturales
- "shoppers who stand like Washington crossing the Delaware" pasó a "que viaja de pie, bien erguida, como un general en un cuadro histórico".
- "as if squirted from a can of Catholic Cool Whip" pasó a "como si la hubieran echado con un aerosol de crema batida católica".
- "giving us our English word for a segregated neighborhood" pasó a "de ahí viene la palabra gueto, que usamos para un barrio segregado". En español la palabra tiene el mismo origen.
- "a female Casanova" pasó a "Casanova con faldas".
- Se mantuvieron Las Vegas, Disneylandia, "un millón de dólares" y "el dólar de la República de Venecia", que se entienden bien en Latinoamérica.

## Indicaciones dudosas
- Parada 02: hay dos instrucciones algo distintas. A mitad de la parada se dice "en cuanto llegue su barco, prepárense para subir enseguida y pasar a la siguiente parada", y al final, "cuando el barco salga del muelle de Ferrovia, pasen a la siguiente parada". Se tradujeron las dos tal cual. La parada 03 empieza con el barco ya saliendo, así que lo práctico es subir cuando llegue el barco y pasar a la 03 cuando zarpe.
- Parada 04: "look immediately to the left down a broad side canal" para ver las torres del gueto. Ese canal es el de Cannaregio, y su desembocadura queda más o menos frente al muelle de Riva de Biasio, así que quizás haya que mirar un poco hacia atrás a la izquierda. No estoy seguro; se tradujo tal cual.
- En todo el tour, izquierda y derecha son en el sentido de la marcha del barco, hacia San Marco, y todas coinciden con la orilla real de cada edificio. Algunos asientos del vaporetto miran hacia atrás: conviene sentarse mirando hacia adelante, o en la cubierta exterior, porque si no, todo queda al revés. Esto no se agregó al texto.
- Parada 18, indicación aclarada: "a short walk back to the Doge's Palace" pasó a "volviendo a pie en la dirección de la que vino el barco", que es hacia donde queda el Palacio Ducal desde San Zaccaria; "the other direction" es la contraria. Es solo una aclaración de "back".
- Parada 08: "Straight ahead" pasó a "Mirando derecho hacia adelante", para que no se entienda "enfrente", es decir, en la otra orilla.

## Datos actualizados en el texto
- Dato actualizado, parada 07: Rick dice que el traghetto cuesta "less than one euro a ride". Hoy los turistas pagan 2 euros por cruce, y los residentes, 0,70. Se cambió a "por unos 2 euros el cruce". En 2025 se habló de subir la tarifa para turistas, pero no encontré que se haya aplicado. Además, hoy funcionan pocos cruces en traghetto y con horarios limitados, no "varios"; conviene preguntar en el lugar.
- Dato actualizado, parada 08: el Fondaco dei Tedeschi, la Lonja de los Alemanes, cerró como centro comercial el 1 de mayo de 2025, y con él la terraza de la azotea. Rick dice que hoy es un centro comercial y que tal vez vean gente en la terraza. Se pasó a pasado y se agregó "Ese centro comercial cerró en 2025". Hasta donde pude averiguar, a fines de 2026 no hay noticias de que haya reabierto.

## Datos que pueden estar desactualizados, sin cambios en el texto
- Parada 13: Rick dice que Venecia tiene unos 60000 habitantes. El centro histórico tiene menos de 50000 desde 2022, unos 47600 en 2025. No es algo que se note en el lugar, así que se dejó.
- Parada 08: "European Union hygiene standards recently required a remodeling": esa remodelación ya tiene años.
- Parada 08: el mercado de pescado de Rialto, la Pescheria, abre de martes a sábado por la mañana; cierra domingo y lunes. El de frutas y verduras abre de lunes a sábado. Conviene confirmarlo.
- Parada 12: el Palazzo Grassi, "recently purchased by a French tycoon", lo compró François Pinault en 2005. Hoy es un museo de arte contemporáneo.
- Parada 15: la fiesta de la Salute es el 21 de noviembre, y el puente flotante se arma solo unos días antes. A principios de noviembre no va a estar.
- Parada 17: la Bienal de Arte de 2026 está abierta hasta el 22 de noviembre de 2026, en los Giardini y el Arsenale. Abre de 10 a 18 y cierra los lunes, con algunas excepciones. Desde 2022, la Bienal de Arte se hace en años pares y la de Arquitectura en años impares.
- Vaporetto: la línea 1 va de Piazzale Roma a la estación, recorre todo el Gran Canal con todas las paradas, sigue a San Marco y termina en el Lido. En Ferrovia hay que subir a la 1, no a la 2: la 2 hace el mismo recorrido más rápido, pero no para en muchas de las paradas del tour. Según guías de 2026, el boleto sencillo cuesta 9,50 euros y vale 75 minutos; los pases cuestan 25 euros por 24 horas, 35 por 48 horas, 45 por 72 horas y 65 por 7 días. No pude confirmar la lista oficial de paradas de la línea 1 ni las tarifas en el sitio de ACTV o Venezia Unica; conviene verificarlas.

## Datos imprecisos, traducidos tal cual
- Parada 02: Rick dice que el puente sobre la laguna es de 1860. El puente ferroviario se inauguró en 1846; el de autos, en 1933.
- Parada 05: el Fondaco dei Turchi fue la sede de los comerciantes otomanos entre 1621 y 1838. "Venice in the 1500s" es contexto general de Rick.
- Parada 05: Rick dice que el casino "is run by the state". En realidad pertenece al municipio de Venecia.
- Parada 07: Rick ubica la época de esplendor de la Ca' d'Oro en el siglo catorce. Se construyó entre 1421 y 1440 aproximadamente, es decir, en el siglo quince.
- Parada 08: "With a span of 160 feet": el puente mide unos 48 metros de largo, pero el arco en sí cubre unos 28 metros. Se tradujo como "unos 50 metros de largo de una orilla a la otra", que es lo correcto y fiel a "span". Lo de "foundations stretching more than 600 feet on either side", unos 180 metros, parece exagerado; se dejó tal cual. "The third bridge built on this spot": antes hubo varios puentes de madera.
- Parada 06: "only the house of the Doge could be called a palace" es una simplificación de Rick. Muchos se llaman palazzo.
- Parada 11: Rick llama "local" a la piedra de Istria. Viene de Istria, al otro lado del Adriático, que entonces era territorio veneciano.
- Parada 12: la bandera roja y dorada con el león es la de la región del Véneto, muy parecida a la de Venecia.
- Parada 12: el Palazzo Grassi se construyó entre 1748 y 1772 aproximadamente, a mediados del siglo dieciocho, no a fines.
- Parada 13: el Puente de la Accademia de madera es de 1933; se reconstruyó en 1985 con la misma forma.
- Parada 14: Rick dice que Peggy Guggenheim se instaló aquí en 1948. Ese año expuso su colección en la Bienal; compró el palacio, el Palazzo Venier dei Leoni, en 1949.
- Parada 16: Rick dice "una estructura circular"; la base es octogonal, como él mismo dice después del interior.

## Medidas
- Two miles, la distancia a tierra firme: unos tres kilómetros. More than two miles long: más de tres kilómetros. 150 feet: 45 metros. Nearly 15 feet, en las dos ocasiones: unos cuatro metros y medio. 25 miles: 40 kilómetros. 20 yards: 20 metros. 100 yards, en las tres ocasiones: 100 metros. 50 yards: 50 metros. 160 feet: unos 50 metros. 600 feet: 180 metros. 1000 square feet: unos 90 metros cuadrados.

## Revisión contra el inglés
- Se revisaron las 18 paradas contra la transcripción, línea por línea. No hay omisiones de contenido ni de indicaciones; lo único que se quitó es lo listado arriba.
- El formato se verificó con el comando de control: 18 paradas, numeradas de 01 a 18.
