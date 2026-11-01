# Notas: La Basílica de San Marcos, en Venecia

## Marcas de tiempo de la transcripción
- La transcripción de Gemini se hizo en tramos de 10 minutos, y los tiempos se reinician en cada tramo: después de [16:44] vuelve a [10:00], después de [25:49] vuelve a [20:00], después de [40:30] vuelve a [30:00] y después de [47:14] vuelve a [40:05]. Además, dentro de cada tramo los tiempos avanzan más rápido que el audio: el primer tramo llega a 16:44, aunque son 10 minutos de audio.
- Las marcas {en=} se copiaron tal como figuran en la transcripción, igual que en la traducción de los Frari, así que no son crecientes. La marca [40:05] aparece dos veces: en la Pala d'Oro, "Along the bottom row", y en "The bronze horses". La parada 18 corresponde a la segunda.
- Cualquier control automático que tome el inglés de cada parada por rango de tiempo, desde su marca hasta la de la parada siguiente, va a dar datos sin sentido para este tour: rangos vacíos o con texto de otro tramo. Por ejemplo, en generar_audio_gemini.py, los valores word_ratio, missing_numbers y en_min. Para ubicar cada parada en el inglés, conviene usar el comienzo del texto:
  - 01, 00:00: "St. Mark's Basilica."
  - 02, 02:34: "The tour begins: The Exterior."
  - 03, 08:20: "Entering the Church."
  - 04, 10:55: "The Atrium Mosaics: Noah's Ark."
  - 05, 13:49: "The Nave."
  - 06, 15:55: "The Pentecost Mosaic."
  - 07, 13:32: "The Greek cross floor plan."
  - 08, 15:32: "The central dome mosaic, the Ascension."
  - 09, 20:18: "Under the Ascension dome, the church as theater."
  - 10, 23:32: "The Discovery of Mark mosaic."
  - 11, 20:15: "The Treasury."
  - 12, 32:25: "The tomb of Saint Mark."
  - 13, 37:25: "The Golden Altarpiece, or Pala d'Oro."
  - 14, 33:45: "The North Transept: The Nicopeia Madonna."
  - 15, 38:50: "The San Marco Museum."
  - 16, 40:35: "Mosaic Fragments."
  - 17, 44:11: "The Sala dei Banchetti."
  - 18, 40:05: "The bronze horses."
  - 19, 45:04: "View of the church interior."
  - 20, 48:23: "The view of St. Mark's Square."

## Pasaje incompleto
- Parada 17, al final: la transcripción dice "We're on the home stretch. When you're ready to continue our tour," y ahí se corta. Es el límite del tramo que empieza en el minuto 40 del audio real, y lo siguiente que transcribió Gemini es el título "The bronze horses". Probablemente se perdieron las indicaciones para llegar a los caballos. Se completó con el sentido más probable: "sigan la ruta del museo hasta los caballos de bronce originales". Conviene escuchar el original alrededor del minuto 40 por si da alguna otra indicación.
- En los otros tres límites de tramo la frase sigue sin cortes ("on the heads... of the 12 apostles", "In the bottom... Left panel"), y en el de [25:49] a [20:00] el sentido también sigue. No parece faltar nada, aunque no se puede descartar que se haya perdido alguna palabra.

## Correcciones de la transcripción
- "Also in the church, you'll see the flood in full force" → "in the arch": se tradujo "También en el arco", porque se refiere a las escenas del arco de Noé que se están mirando.
- "Matthew, Mark, Luca, and John" → Lucas.
- "In the bottom... / Left panel", cortado por el límite de tramo → "En el panel de abajo a la izquierda".
- "Ciborio di Anastasia" → "Ciborio de Anastasia".
- "the literary lion", en el candelabro: se tradujo literal, "el león literario". Puede ser un león con un libro, como el de san Marcos, o un error de reconocimiento por "the little lion", es decir, el leoncito.
- "Once inside the museum", dicho al entrar al Tesoro → "Una vez adentro", para que no se confunda con el Museo de San Marcos, que se visita al final.
- Los nombres propios vinieron bien escritos: Nicopeia, Pala d'Oro, Pala Feriale, Paolo Veneziano, Sala dei Banchetti, Loggia dei Cavalli, Artaxerxes, San Giorgio Maggiore, Gene Openshaw.

## Un solo narrador y adaptaciones
- Se eliminaron: la presentación de Lisa ("I've invited a good friend... Welcome, Lisa. Buongiorno. Lisa will give us helpful directions..."); las instrucciones de la app sobre el ícono de actualizaciones ("press the icon at the lower right", "pause for just a moment right now to review our updates", "It's okay, we'll wait", "So again, be sure to check our updates page..."); y "Ooh, heavy.", la reacción de la copiloto después de la iconoclasia.
- Parada 03: de "And there are other rules. So again, be sure to check our updates page" quedó solo "Y hay otras normas.". Ver más abajo las normas de vestimenta y de bolsos.
- Se convirtieron a un solo narrador: "Listen as Rick points some things out" → "mientras les señalo algunas cosas"; "time Rick's commentary with the flow of traffic" → "para que mis explicaciones vayan al ritmo del avance de la gente"; "Don't let Rick rush you" → "No se apuren"; "while listening to Rick's description" → "mientras escuchan mi descripción"; "while Rick gives a quick overview" → "mientras les doy un rápido panorama".
- Parada 12: "Shh. As you continue... Shh. Quietly." es un intercambio entre las dos voces; quedó "Ahora, en silencio, por favor.".
- Se dejaron en boca del único narrador: "Hey, you're reading like a medieval peasant. Easy, huh?", "Okay, now you can scoff." y "Make like a Doge".
- Pausas: "Pause the audio guide and restart it once you're inside the atrium", "When you see a stone canopy, start the next track", "Pause the audio guide while you climb the stairs and buy your ticket. Meet you upstairs", "Stroll as you listen" y "you may need to either pause the audio guide or skip ahead" se adaptaron a la división por paradas. "Feel free to pause the audio guide and see things at your own pace" pasó a "tómense su tiempo y vean las cosas a su propio ritmo".
- Parada 14: "One of those offerings is our next stop" pasó a "es lo próximo que vamos a ver", porque el fusil está dentro de la misma parada.
- Final: se omitieron la mención de la guía impresa de la que sale el tour, la lista de otras audioguías (Plaza de San Marcos, Frari y Gran Canal), la publicidad de la guía y del sitio web y los créditos de producción. Se dejó el agradecimiento a Gene Openshaw y la despedida.
- Adaptaciones culturales: "football field" → "una cancha de fútbol"; "Oh boy, Wilbur, have we done some traveling!", que alude a Mister Ed, la serie del caballo que habla → "¡Uf, compañero, sí que hemos viajado!"; "What goes around comes around, and Napoleon came around" → "todo lo que va, vuelve, y Napoleón vino"; "early ransack", un juego con los nombres de los períodos del arte → "en broma, estilo 'saqueo temprano'"; "monstrous monstrances" → "enormes custodias". Se mantuvieron Ben-Hur y "sin necesidad de un manual de conversación de Rick Steves".
- Parada 20: "the music from the orchestras" se tradujo tal cual, porque son las orquestas reales de los cafés de la plaza, no música del audio.

## Indicaciones dudosas
- Parada 07: "When you reach the center of the church where the altar is, look up into the dome." Hasta donde sé, el altar mayor está detrás del iconostasio, en el presbiterio, y no bajo la cúpula central; puede que se refiera a un altar que a veces se arma en el crucero. Se tradujo tal cual. Lo importante es pararse bajo la gran cúpula del centro.
- Parada 08: "Busquen los nombres: Mateo, Marcos, Lucas y Juan". Probablemente en el mosaico estén escritos en latín, algo como Matheus, Marcus, Lucas, Iohannes, así que pueden no reconocerlos en español.
- Parada 11: el recorrido por el Tesoro, con la vitrina central, la pared de la derecha, el rincón del fondo a la izquierda y la sala contigua, depende de cómo esté montado hoy. Rick mismo avisa que las piezas cambian de lugar. Se tradujo tal cual.
- Paradas 15 a 19: el orden y el recorrido del museo pueden variar, como dice Rick. El "galopen unos pasos hacia la izquierda" de la parada 18, para llegar a la balaustrada, depende de ese recorrido.
- Parada 17: la indicación final está completada; ver "Pasaje incompleto".

## Datos imprecisos, traducidos tal cual
- Paradas 02 y 12: primero dice que el cuerpo estuvo en Egipto "siete siglos después de la muerte de Marcos" y después dice "ocho siglos más tarde". Marcos murió hacia el año 68, así que en 828 habían pasado unos 760 años.
- Parada 12: "en 828 construyeron la primera iglesia de San Marcos": el cuerpo llegó en 828; la primera iglesia se empezó enseguida y se terminó hacia 832.
- Parada 06: "Bizancio acababa de salir de dos siglos de iconoclasia". La iconoclasia duró algo más de un siglo, de 726 a 843, con una interrupción, y había terminado casi 300 años antes de este mosaico, que es de alrededor de 1125.
- Parada 09: Monteverdi escribió L'Orfeo, que suele considerarse la primera gran ópera, en 1607 en Mantua, antes de ser maestro de capilla de San Marcos, cargo que tuvo desde 1613. Lo que dice Rick es cierto, pero puede dar a entender que la escribió en Venecia.
- Parada 14: la Cuarta Cruzada no se organizó para rescatar a Bizancio de los turcos; su destino era Egipto y Tierra Santa, y terminó desviándose a Constantinopla por las deudas con Venecia y una disputa por el trono bizantino.
- Parada 13: la historia de la Pala d'Oro es más compleja: se encargó en Constantinopla en 976, se rehízo en 1105, se amplió después de 1204 con esmaltes saqueados y en 1345 la volvió a montar el orfebre veneciano Giovanni Paolo Boninsegna, que no era bizantino. Las cifras de piedras también varían según la fuente.
- Parada 11: la urna de Artajerjes es, hasta donde sé, un vaso egipcio de alabastro con el nombre del rey. Los reyes persas no se cremaban, así que es dudoso que haya contenido sus cenizas.
- Parada 18: el carbono 14 no sirve para fechar el bronce, y la fecha de los caballos sigue en discusión. Hay propuestas desde el siglo cuarto antes de Cristo hasta el siglo segundo o tercero después de Cristo.
- Parada 05: "casi 5000 yardas cuadradas" de mosaicos, es decir, unos 4200 metros cuadrados. La cifra que suele darse es de más de 8000 metros cuadrados.
- Parada 17: las claves de fa y de sol ya existían antes del siglo dieciséis; lo de Rick es una simplificación.

## Datos que pueden estar desactualizados, para verificar
- Parada 03: Rick dice "Lo mejor es reservar con anticipación". Según la nota de 2026 que nos pasaron, ahora la reserva es obligatoria y los precios subieron. Se tradujo tal cual; conviene reservar antes de ir.
- Horario actual, según los datos que nos pasaron: de lunes a sábado, de 9:30 a 17:15; los domingos, desde las 14:00. Rick no menciona horarios.
- Paradas 03, 10, 11 y 14: Rick dice que el Tesoro, la Pala d'Oro y el museo tienen entradas aparte, y habla de "una entrada pequeña". Con la suba de precios de 2026, conviene confirmar cuánto cuestan y si siguen siendo entradas separadas o si hay entrada combinada.
- Parada 03, "hay otras normas": según tengo entendido, para entrar hay que tener los hombros y las rodillas cubiertos, y no se permiten mochilas ni bolsos grandes; hay un guardarropa cerca de la basílica, el Ateneo San Basso. Conviene confirmarlo.
- Parada 03: el sistema de pasillos con cordones y sentido único puede cambiar.
- Parada 05: los reflectores que iluminan los mosaicos solo se encienden en algunos momentos del día; si quieren verlos iluminados, conviene averiguar el horario.
- Parada 14: la escalera al museo es empinada, como dice Rick; tenerlo en cuenta.
- Parada 14: no puedo confirmar que el fusil de 1848 siga colgado en el pilar.
- Parada 20: las orquestas de los cafés tocan sobre todo de tarde y de noche, y según la temporada; puede que no estén tocando a la hora de la visita.

## Medidas
- Casi 5000 yardas cuadradas → más de 4000 metros cuadrados. No hay otras medidas imperiales.

## Revisión contra el inglés
- Se revisaron las 20 paradas contra la transcripción, frase por frase. Todas las cifras del inglés están en la traducción: los siglos van en palabras, Artajerjes primero en palabras, "the 1700s" como "siglo dieciocho" y las yardas convertidas. No se omitió contenido ni indicaciones; los únicos cortes son los diálogos, las instrucciones de la app y los créditos listados arriba.

## Corrección posterior
- Parada 17: se recuperó del original la indicación cortada en el cambio de tramo: "double back the way you came through the displays of stone fragments from the church, finally arriving at the four big bronze horses". Reemplaza la indicación completada a mano.
