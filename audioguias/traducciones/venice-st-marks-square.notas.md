# Notas: La Plaza San Marcos, en Venecia

## Transcripción y marcas de tiempo
- La transcripción es de Gemini. Para controlarla, se hizo aparte una transcripción con Whisper `small.en` del MP3 original (no se guardó en el repositorio). El contenido coincide casi palabra por palabra: Gemini no perdió ningún pasaje, ni siquiera en los cortes entre tramos de 10 minutos. Las pocas diferencias están en la lista de correcciones.
- **Las marcas `{en=}` se copiaron de la transcripción, como se pidió, pero no son tiempos reales y no van en orden.** El script transcribe en tramos de 10 minutos, y Gemini devolvió los segundos en formato minutos-segundos (por ejemplo, 109 en lugar de 69 para 1:09). Por eso, dentro de cada tramo las marcas están infladas, y al empezar cada tramo vuelven atrás, a 10:00, 20:00, 30:00 y 40:00. Las paradas 05, 09, 12 y 15 tienen una marca menor que la parada anterior. El MP3 dura 43:05, aunque la transcripción llega a 44:18.
- Consecuencia práctica: la comparación del inglés con el español por rangos de tiempo que hace `scripts/generar_audio_gemini.py` no va a funcionar bien en este tour. En las paradas 04, 08, 11 y 14 el texto en inglés va a salir vacío, porque la parada siguiente tiene una marca menor, y en otras va a mezclar texto de dos paradas. Lo mismo pasa con `venice-frari-church.md`, que también tiene marcas fuera de orden.
- Tiempos reales de comienzo de cada parada en el MP3, según Whisper, por si sirven:

  - 01 Introducción: 00:00
  - 02 La plaza: 01:45
  - 03 Los cafés: 06:37
  - 04 La Basílica de San Marcos, el exterior: 09:11
  - 05 La Torre del Reloj: 12:12
  - 06 Tiendas y artesanías: 14:51
  - 07 El Campanile: 16:51
  - 08 Las inundaciones en Venecia: 18:31
  - 09 El Palacio Ducal: 21:12
  - 10 La Piazzetta: 24:35
  - 11 La laguna: 28:16
  - 12 Las góndolas: 31:39
  - 13 La elegante decadencia: 34:48
  - 14 El Puente de los Suspiros: PENDIENTE
  - 15 Venecia de noche: PENDIENTE

## Correcciones de la transcripción
- "mostly seriously in March and November" → "most seriously", más grave en marzo y noviembre (así lo oye Whisper).
- "Aqua Alta" → acqua alta.
- "tiny past square" → "time-passed square", una placita olvidada por el tiempo. Whisper oye "time pass square".
- "kneeling before Gods": las dos transcripciones dicen "gods", pero casi seguro es "God". En los cuadros del Palacio Ducal los dux aparecen arrodillados ante Cristo, la Virgen o los santos. Se tradujo "arrodillados ante Dios".
- "What, little old me?": Whisper oye "Why, little old me?". El sentido es el mismo; se tradujo "¿Quién? ¿Yo, tan poquita cosa?".
- "And a large winged lion": Whisper oye "An alert winged lion". Se dejó "un gran león alado".
- "pigeon poopulation": el juego de palabras entre "poop", caca, y "population" se adaptó como "la popoblación de palomas, digo, la población".
- Nombres que Whisper transcribió mal y Gemini bien, para quien compare las dos: Correr ("Carrere"), Loggetta ("Logeta"), Marciana ("Marchiana"), Danieli ("Daniele"), Giardinetti Reali ("Riale"), forcola ("forkula"), livello marea ("livello maria"), siroco ("shirako").

## Un solo narrador: diálogos eliminados o adaptados
- Se eliminaron: la presentación de Lisa ("To help us along the way, I've invited... Ciao, Lisa. Buongiorno, Rick. Lisa will give us helpful directions..."); "Uh, yeah, thanks for that image, Rick"; "Rick?"; "Yeah, that one", que Lisa dice después de nombrar Las cuatro estaciones y se refiere a la música que suena en el original; "Rick, put the lace tea cozy down and back away"; y la interrupción "Rick!" y el "Okay" de la digresión de las góndolas.
- Se convirtieron a un solo narrador, conservando el contenido: "listen to the next track as Rick talks about the cafes" pasó a "escuchen la siguiente parada, en la que les hablo de los cafés"; "While we're here, Rick, tell us more about the flooding" pasó a "Ya que estamos aquí, les cuento más sobre las inundaciones"; "Did someone mention shopping?" quedó como pregunta retórica, "¿Alguien dijo compras?"; el juego de encontrar cuatro leones en 20 segundos, que en el original es un diálogo entre Rick y Lisa, quedó en boca del narrador; "Uh, oh. Venice does this to me, I'm sorry. I digress." pasó a "Ay, perdón. Venecia me hace esto. Me fui por las ramas."; y "What happened in Venice? Stayed in Venice." quedó como una sola frase.

## Omitido
- Las instrucciones de la app: revisar las actualizaciones del tour con el ícono de abajo a la derecha, "pause for just a moment right now to review our updates and special tips. It's okay, we'll wait."
- Al final: la lista de otras audioguías de Venecia, la mención de la guía impresa de Rick Steves y de su sitio web, y el crédito de producción. Se dejó, dentro de la parada 04, la mención breve de la audioguía de la Basílica de San Marcos, porque es parte del contenido.
- La música de los interludios entre secciones. Según la regla 11b, no se promete ningún sonido: lo que se dice de las orquestas de los cafés, de las campanas del Campanile, de los moros de la Torre del Reloj y de la sirena del agua alta se refiere a lo que pasa en el lugar, no al audio.

## Adaptaciones
- "Nebraskans in shorts" → "turistas norteamericanos en pantalones cortos".
- "his Air Force One" → "que era como su avión presidencial".
- "without so much as a Miranda warning" → "sin que nadie les leyera siquiera sus derechos".
- "CEO" → "director general". "Mardi Gras" → "la fiesta de varias semanas antes de la Cuaresma".
- "has slices of ham over her eyes": es el dicho italiano "avere le fette di prosciutto sugli occhi". Se tradujo literal y se agregó "es decir, no ve lo que tiene delante", para que se entienda.
- "bam, bam, bam" → "pum, pum, pum"; "uno, due, tre" se dejó en italiano.
- "the guy balancing on a big bronze ball" → "la figura que hace equilibrio sobre una gran bola de bronce". La estatua de la Aduana es la Fortuna, una figura femenina, así que se evitó "el tipo".
- El poema de Lord Byron es la primera estrofa del canto cuarto de La peregrinación de Childe Harold. Se tradujo en prosa, sin rima, para que se entienda al oído.
- "count inland seven columns" → "cuenten siete columnas hacia adentro, alejándose del agua"; "look inland" → "miren hacia el interior de la ciudad, de espaldas a la laguna". Solo se aclaró qué quiere decir "inland"; la dirección es la misma.
- Para la navegación por paradas, se agregaron cierres breves: en la 05, "Pueden pasar a la siguiente parada mientras las recorren"; en la 06, "Cuando lleguen, pasen a la siguiente parada"; en la 09, "Cuando estén en la base del Campanile, pasen a la siguiente parada"; y en la 13, "Cuando estén arriba del puente, pasen a la siguiente parada". En la 02 y la 12, "listen to the next track" pasó a "escuchen la siguiente parada".

## Indicaciones dudosas
- Parada 02: "the tourist office is to your right in the corner of the square, and a pay toilet is behind you, just outside the piazza". Un poco antes, Rick les pide que salgan a la plaza, le den la espalda a la iglesia y miren hacia arriba, y después nunca les dice que se den vuelta. Si siguen de espaldas a la basílica, la derecha y el "detrás" quedan invertidos. Hasta donde sé, el punto de información turística está en la esquina suroeste, cerca de la entrada del Museo Correr, y los baños públicos, detrás del ala de Napoleón; eso coincide con la indicación si se la entiende mirando hacia la basílica. Se tradujo tal cual. Un revisor podría agregar "mirando hacia la basílica".
- Parada 07: la placa de la inundación de 1966 está "about knee-high, or three feet above the pavement". Tres pies son unos 90 centímetros, bastante más arriba de la rodilla. Se tradujeron las dos cosas. Tampoco pude confirmar que la placa siga en ese lugar.
- Parada 10: Rick pide salir a uno de los muelles de madera de las góndolas. No es un error de orientación, pero esos muelles son para subir a las góndolas, pueden estar resbaladizos y los gondoleros a veces no dejan pasar a quien no va a contratar un paseo. Para personas mayores, conviene mirar desde la orilla.

## Datos imprecisos (traducidos tal cual)
- Parada 04: "dedicated in 1063". La basílica actual se empezó a construir en 1063 y se consagró en 1094.
- Paradas 02, 06 y 07: el Campanile no mide 300 pies, unos 90 metros, sino 98,6 metros. Además, el ascensor no sube hasta la punta sino hasta la celda de las campanas, bastante más abajo.
- Parada 07: Rick cuenta que el Campanile crujió una noche y se cayó a la mañana siguiente. En realidad las grietas aparecieron unos días antes, y se derrumbó el 14 de julio de 1902, a media mañana. Lo de que el ángel cayó de pie es más leyenda que dato.
- Parada 07: la inundación del 4 de noviembre de 1966 llegó a 194 centímetros en el mareógrafo oficial. Rick dice 196; Whisper oye lo mismo.
- Parada 08: "around 30 centimeters or 20 inches". 20 pulgadas son unos 50 centímetros; se tradujo solo "30 centímetros". Por otra parte, hasta donde sé, el centro de mareas de Venecia indica que la parte más baja de la plaza empieza a inundarse con mareas de unos 80 centímetros; las cifras de Rick, 30 y 65 centímetros, quizás se miden desde otro nivel de referencia.
- Parada 08: no pude confirmar que en 2006 se haya levantado y elevado el pavimento de toda la plaza.
- Parada 03: "all three cafes". En la plaza hay más de tres cafés con orquesta: el Florian, el Quadri y el Lavena, y además el Chioggia, en la Piazzetta. El propio Rick habla después de "los otros cafés".
- Parada 05: el "primer reloj digital del mundo" es una broma de Rick; el indicador con números que cambia cada cinco minutos es del siglo diecinueve.
- Parada 10: la Loggetta es de 1537 a 1549, y la Biblioteca Marciana se empezó en 1537; Rick dice "hacia 1530".
- Parada 10: el pórfido no es un mármol, es una roca volcánica; Rick dice "porphyry marble".
- Parada 10: las dos columnas llegaron de Oriente en el siglo doce, pero su origen exacto no se conoce con certeza. La estatua de san Teodoro que está arriba es una copia; el original está en el Palacio Ducal.
- Parada 04: los caballos de bronce de la fachada son copias. Los originales están dentro de la basílica, en el Museo de San Marcos, que se paga aparte. Rick no lo dice.
- Parada 11: la ceremonia del casamiento con el mar se hacía el día de la Ascensión, frente al Lido.
- Parada 12: la ley que obligó a pintar de negro las góndolas suele fecharse en 1562, en el siglo dieciséis; Rick dice siglo diecisiete.

## Datos que pueden estar desactualizados
- Tasa de acceso a Venecia: desde 2024 la ciudad cobra a los visitantes que no duermen en Venecia un "contributo di accesso", solo en algunos días, sobre todo fines de semana y feriados de primavera y verano, y en el horario de 8:30 a 16:00. En 2024 eran 5 euros; en 2025, 5 o 10 euros según la anticipación con que se reservara. Quienes se alojan en Venecia están exentos, pero tienen que pedir la exención en el sitio oficial. No sé con certeza qué días se cobra en 2026; a principios de noviembre seguramente no, pero conviene confirmarlo en el sitio oficial, cda.ve.it. Tiene que ver con lo que Rick dice en la parada 15 sobre los visitantes que vienen a pasar el día.
- Parada 02: el punto de información turística de la esquina de la plaza y la otra oficina de turismo que Rick menciona en la parada 10, cerca de los Giardinetti Reali, pueden haber cambiado de lugar o cerrado. Los baños públicos se pagan, alrededor de un euro y medio.
- Paradas 02 y 03: en la Plaza San Marcos hoy está prohibido dar de comer a las palomas, sentarse en el suelo o en los escalones de las arcadas y comer o hacer picnic, con multas. Cuando Rick habla de "sentarse aquí a ver pasar el mundo" y de quedarse por los alrededores, conviene hacerlo de pie o en las mesas de los cafés.
- Parada 02: el Museo Correr y el Palacio Ducal se visitan con una entrada combinada, los Museos de la Plaza San Marcos. Hoy conviene comprarla en línea, con horario, más que en la boletería del Correr. Tampoco pude confirmar que siga abierto el café del Museo Correr, que Rick recomienda en la parada 11.
- Parada 03: el precio de sentarse en los cafés de la plaza es hoy bastante mayor que los 15 euros de Rick. En el Florian, una bebida en la terraza ya cuesta más de 10 euros, y se suma un recargo por la música de unos 6 o 7 euros por persona. Las orquestas tocan en horarios fijos, y en invierno pueden tocar menos.
- Parada 07, el Campanile: se paga entrada y conviene reservar horario en línea; en temporada alta las filas son largas. Puede cerrar por mal tiempo o por obras. Confirmen horarios y precio antes de ir.
- Paradas 07 y 08, el agua alta: desde octubre de 2020 funciona el MOSE, un sistema de compuertas móviles en las bocas de la laguna que se levanta cuando se pronostican mareas muy altas, más o menos desde 110 centímetros. Desde entonces ya no hubo grandes inundaciones como la de noviembre de 2019, pero la plaza se sigue inundando con mareas más bajas, que no activan el sistema. Además, desde 2023 hay barreras de vidrio que protegen el atrio de la basílica. Las cifras de Rick, 50 inundaciones por invierno y 100 por año, y la idea de que "el agua va ganando" son de antes del MOSE. Rick no lo menciona. Noviembre es justamente temporada de agua alta: conviene mirar el pronóstico de mareas del Centro Maree de la ciudad. Si hay agua alta, se venden cubrebotas de plástico en la calle y se arman pasarelas elevadas.
- Parada 12, góndolas: la tarifa oficial cambió varias veces. En los últimos años rondaba los 90 euros por unos 30 minutos de día y unos 110 de noche, por góndola. Además, según tengo entendido, desde 2020 el máximo es de 5 pasajeros, no 6. Confirmen el precio antes de subir, como dice Rick.
- Parada 12: hay unos 430 gondoleros con licencia; la cifra de Rick, unos 400, sigue siendo aproximada.
- Parada 14: la visita al Palacio Ducal sigue incluyendo el Puente de los Suspiros y las prisiones.

## Medidas
- Dos acres y medio → alrededor de una hectárea.
- 300 pies → unos 90 metros, las tres veces que se menciona el Campanile.
- Tres pies → unos 90 centímetros, en la placa y en las barreras de las puertas.
- "More than six feet" → casi dos metros, junto a los 196 centímetros.
- 20 pulgadas → se omitió, porque Rick ya da la cifra en centímetros y las dos no coinciden.
- "A few inches" → varios centímetros.
- Medio acre → unos 2000 metros cuadrados.
- Casi 15 pies → casi 4 metros y medio.
- 212 millas cuadradas → unos 550 kilómetros cuadrados.
- 35 pies → unos 11 metros; 5 pies → un metro y medio; 1000 libras → unos 450 kilos; 3 millas por hora → unos 5 kilómetros por hora.
