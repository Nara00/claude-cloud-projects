"""Arma webapp/data/tours.json desde audioguias/traducciones/*.md.

Lee los .md con el formato "# Título" + "## NN · Parada {en=mm:ss}" + texto.
Para cada parada, geocodifica el nombre contra Nominatim (con cache). Las paradas
no geocodificables (p. ej. 'Introducción') heredan las coordenadas de la anterior.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
TRAD = os.path.abspath(os.path.join(BASE, "audioguias", "traducciones"))
OUT = os.path.abspath(os.path.join(BASE, "webapp", "data", "tours.json"))
CACHE = os.path.abspath(os.path.join(BASE, "webapp", "build", "geo_cache.json"))
# mapa=NN (opcional): número de la parada en el mapa oficial, si difiere del número de pista
STOP_RE = re.compile(r"^## (\d+) · (.+?) \{en=(\d+):(\d+)(?: mapa=(\d+[a-z]?))?\}\s*$")

CITIES = {
    "rome": {"name": "Roma", "country": "Italia", "nominatim_city": "Roma, Italia",
             "center": [41.9028, 12.4964], "zoom": 14,
             "tours": ["rome-pantheon", "rome-colosseum", "rome-forum", "rome-heart",
                       "rome-jewish-ghetto", "rome-ostia-antica", "rome-sistine-chapel",
                       "rome-st-peters-basilica", "rome-trastevere", "rome-vatican-museums",
                       "rome-vatican-pinacoteca"]},
    "florence": {"name": "Florencia", "country": "Italia", "nominatim_city": "Firenze, Italia",
                 "center": [43.7696, 11.2558], "zoom": 15,
                 "tours": ["florence-accademia-david", "florence-bargello",
                            "florence-renaissance-walk", "florence-san-marco-museum",
                            "florence-uffizi-gallery", "pitti-palatine-gallery"]},
    "siena": {"name": "Siena", "country": "Italia", "nominatim_city": "Siena, Italia",
              "center": [43.3188, 11.3307], "zoom": 15, "tours": ["siena-city-walk"]},
    "sangimignano": {"name": "San Gimignano", "country": "Italia", "nominatim_city": "San Gimignano, Italia",
                     "center": [43.4677, 11.0432], "zoom": 16, "tours": ["sangimignano-walk"]},
    "venice": {"name": "Venecia", "country": "Italia", "nominatim_city": "Venezia, Italia",
               "center": [45.4380, 12.3358], "zoom": 15,
               "tours": ["venice-grand-canal", "venice-st-marks-square", "venice-st-marks-basilica",
                         "venice-frari-church"]},
    "barcelona": {"name": "Barcelona", "country": "España", "nominatim_city": "Barcelona, España",
                   "center": [41.3851, 2.1734], "zoom": 14,
                   "tours": ["barcelona-city-walk", "barcelona-eixample-walk"]},
    "madrid": {"name": "Madrid", "country": "España", "nominatim_city": "Madrid, España",
                "center": [40.4168, -3.7038], "zoom": 15, "tours": ["madrid-city-walk"]},
    "seville": {"name": "Sevilla", "country": "España", "nominatim_city": "Sevilla, España",
                 "center": [37.3886, -5.9823], "zoom": 15, "tours": ["sevilla-city-walk"]},
}

# URL del PDF del mapa oficial de Rick Steves para cada tour.
# Son los links reales del CDN; se abren directo en el navegador del teléfono.
TOUR_MAPS = {
    "rome-pantheon": "https://d3dqioy2sca31t.cloudfront.net/Projects/cms/production/000/004/454/original/c9bf7131f52c3012c39c5db21f945984/pantheon.pdf",
    "rome-colosseum": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-colosseum.pdf",
    "rome-forum": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-forum.pdf",
    "rome-heart": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/heart-of-rome-walk-map-1.pdf",
    "rome-jewish-ghetto": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-rome-jewish-ghetto.pdf",
    "rome-ostia-antica": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-rome-ostia-antica.pdf",
    "rome-sistine-chapel": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-rome-sistine.pdf",
    "rome-st-peters-basilica": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-st-peters-basilica.pdf",
    "rome-trastevere": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-rome-trastevere.pdf",
    "rome-vatican-museums": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/vatican-musems-map.pdf",
    "rome-vatican-pinacoteca": "https://www.ricksteves.com/rome-pinacoteca-audio-tour-map.pdf",
    "florence-accademia-david": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-accademia.pdf",
    "florence-bargello": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-florence-bargello-museum.pdf",
    "florence-renaissance-walk": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-florence-renaissance-walk.pdf",
    "florence-san-marco-museum": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-florence-sanmarco-museum.pdf",
    "florence-uffizi-gallery": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-florence-uffizi.pdf",
    "pitti-palatine-gallery": "maps/pitti-croquis.png",
    # Varios mapas por tour: el primero es el principal.
    "siena-city-walk": ["maps/siena-mapa-oficial.jpg", "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-siena-city-walk-map.pdf"],
    "venice-grand-canal": "https://www.ricksteves.com/watch-read-listen/audio/map-audiotours-venice-grand-canal.pdf",
    "venice-st-marks-square": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-venice-san-marco-square.pdf",
    "venice-st-marks-basilica": ["https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-venice-san-marco-basilica.pdf", "maps/basilica-san-marcos-croquis.png"],
    "venice-frari-church": ["https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-venice-frari.pdf", "maps/frari-croquis.png"],
    "barcelona-city-walk": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-barcelona-city-walk.pdf",
    "barcelona-eixample-walk": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/barcelona-eixample-walk-map-rick-steves.pdf",
    "madrid-city-walk": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/map-audiotours-madrid-city-walk.pdf",
    "sevilla-city-walk": "https://www.ricksteves.com/watch-read-listen/audio/audio-tours/sevilla-city-walk-map-rick-steves.pdf",
}


def map_label(url):
    if url.endswith(".pdf"):
        return "Ver mapa oficial de Rick Steves (PDF)"
    if "oficial" in url:
        return "Ver mapa oficial con los números del audio"
    return "Ver croquis del recorrido"


def tour_maps(tour):
    m = TOUR_MAPS.get(tour) or []
    return [{"url": u, "label": map_label(u)} for u in ([m] if isinstance(m, str) else m)]

# Coordenadas aproximadas del punto de inicio de cada tour (centro del lugar).
# Las paradas internas heredan la coord del tour. Mejora futura: coord por parada.
TOUR_COORDS = {
    "rome-pantheon": [41.8986, 12.4769],
    "rome-colosseum": [41.8902, 12.4922],
    "rome-forum": [41.8925, 12.4853],
    "rome-heart": [41.9009, 12.4833],  # Piazza Venezia
    "rome-jewish-ghetto": [41.8921, 12.4777],
    "rome-ostia-antica": [41.7556, 12.2914],
    "rome-sistine-chapel": [41.9029, 12.4545],
    "rome-st-peters-basilica": [41.9022, 12.4539],
    "rome-trastevere": [41.8882, 12.4680],
    "rome-vatican-museums": [41.9064, 12.4536],
    "rome-vatican-pinacoteca": [41.9064, 12.4536],
    "florence-accademia-david": [43.7766, 11.2594],
    "florence-bargello": [43.7703, 11.2576],
    "florence-renaissance-walk": [43.7731, 11.2559],  # Piazza del Duomo
    "florence-san-marco-museum": [43.7786, 11.2585],
    "florence-uffizi-gallery": [43.7678, 11.2553],
    "pitti-palatine-gallery": [43.7651, 11.2500],
    "siena-city-walk": [43.3188, 11.3307],
    "sangimignano-walk": [43.4677, 11.0432],
    "venice-grand-canal": [45.4410, 12.3210],
    "venice-st-marks-square": [45.4341, 12.3380],
    "venice-st-marks-basilica": [45.4345, 12.3397],
    "venice-frari-church": [45.4369, 12.3266],
    "barcelona-city-walk": [41.3851, 2.1734],
    "barcelona-eixample-walk": [41.3917, 2.1649],
    "madrid-city-walk": [40.4168, -3.7038],
    "sevilla-city-walk": [37.3886, -5.9823],
}

# Puntos del recorrido (aprox.) para dibujar el mapa dentro del tour cuando no hay PDF oficial.
# label = número de parada que se muestra; stop = parada que reproduce; kind "info" = no es parada.
TOUR_POINTS = {
    "siena-city-walk": [
        {"label": "🚌", "name": "Colectivo 131R a Florencia (Via Tozzi / Piazza Gramsci, aprox.)", "coord": [43.3228, 11.3310], "kind": "info"},
        {"label": "1-2", "name": "Il Campo", "coord": [43.3187, 11.3316], "stop": 1},
        {"label": "3", "name": "Palazzo Pubblico", "coord": [43.3181, 11.3320], "stop": 3},
        {"label": "4", "name": "Fonte Gaia", "coord": [43.3189, 11.3312], "stop": 4},
        {"label": "5", "name": "Via di Città", "coord": [43.3182, 11.3307], "stop": 5},
        {"label": "6", "name": "Palazzo Chigi-Saracini", "coord": [43.3177, 11.3310], "stop": 6},
        {"label": "7", "name": "Quattro Cantoni", "coord": [43.3167, 11.3297], "stop": 7},
        {"label": "8", "name": "Fachada del Duomo", "coord": [43.3177, 11.3286], "stop": 8},
        {"label": "9-12", "name": "Interior del Duomo y Biblioteca Piccolomini", "coord": [43.3180, 11.3291], "stop": 9},
        {"label": "13", "name": "La iglesia inconclusa (Duomo Nuovo)", "coord": [43.3178, 11.3295], "stop": 16},
        {"label": "14", "name": "Camino a la Piazza dell'Indipendenza", "coord": [43.3184, 11.3296], "stop": 17},
        {"label": "15", "name": "Piazza dell'Indipendenza y Loggia", "coord": [43.3192, 11.3305], "stop": 18},
        {"label": "16", "name": "Banchi di Sopra", "coord": [43.3194, 11.3313], "stop": 19},
        {"label": "17", "name": "Piazza Salimbeni (fin)", "coord": [43.3212, 11.3308], "stop": 20},
    ],
    "sangimignano-walk": [
        {"label": "P", "name": "Estacionamiento P2 Montemaggio (aprox.)", "coord": [43.4641, 11.0424], "kind": "info"},
        {"label": "1-2", "name": "Porta San Giovanni", "coord": [43.4655, 11.0425], "stop": 1},
        {"label": "3", "name": "Piazza della Cisterna", "coord": [43.4671, 11.0433], "stop": 3},
        {"label": "4", "name": "Colegiata", "coord": [43.4678, 11.0430], "stop": 4},
        {"label": "5", "name": "Palacio Comunal y Torre Grossa", "coord": [43.4677, 11.0436], "stop": 5},
        {"label": "6", "name": "Rocca di Montestaffoli", "coord": [43.4686, 11.0418], "stop": 6},
        {"label": "7", "name": "Iglesia de San Agustín", "coord": [43.4712, 11.0425], "stop": 7},
    ],
    "venice-grand-canal": [
        {"label": "1-3", "name": "Ferrovia: estación de tren y salida del vaporetto línea 1", "coord": [45.4405, 12.3218], "stop": 1},
        {"label": "4", "name": "Riva de Biasio", "coord": [45.4415, 12.3268], "stop": 4},
        {"label": "5", "name": "San Marcuola", "coord": [45.4437, 12.3300], "stop": 5},
        {"label": "6", "name": "San Stae", "coord": [45.4413, 12.3329], "stop": 6},
        {"label": "7", "name": "Ca' d'Oro", "coord": [45.4407, 12.3346], "stop": 7},
        {"label": "8", "name": "Rialto Mercato", "coord": [45.4393, 12.3341], "stop": 8},
        {"label": "9", "name": "Rialto", "coord": [45.4374, 12.3362], "stop": 9},
        {"label": "10", "name": "San Silvestro", "coord": [45.4367, 12.3343], "stop": 10},
        {"label": "11", "name": "Sant'Angelo", "coord": [45.4353, 12.3327], "stop": 11},
        {"label": "12", "name": "San Tomà", "coord": [45.4346, 12.3290], "stop": 12},
        {"label": "13", "name": "Ca' Rezzonico", "coord": [45.4335, 12.3267], "stop": 13},
        {"label": "14", "name": "Accademia", "coord": [45.4317, 12.3280], "stop": 14},
        {"label": "15", "name": "Santa Maria del Giglio", "coord": [45.4320, 12.3333], "stop": 15},
        {"label": "16", "name": "La Salute", "coord": [45.4312, 12.3348], "stop": 16},
        {"label": "17", "name": "San Marco (Vallaresso)", "coord": [45.4326, 12.3367], "stop": 17},
        {"label": "18", "name": "San Zaccaria: fin del recorrido", "coord": [45.4337, 12.3420], "stop": 18},
    ],
    "venice-st-marks-square": [
        {"label": "1-2", "name": "La plaza, desde el extremo opuesto a la basílica", "coord": [45.4339, 12.3366], "stop": 1},
        {"label": "3", "name": "Los cafés", "coord": [45.4341, 12.3378], "stop": 3},
        {"label": "4", "name": "Fachada de la Basílica", "coord": [45.4344, 12.3392], "stop": 4},
        {"label": "5", "name": "Torre del Reloj", "coord": [45.4348, 12.3390], "stop": 5},
        {"label": "6", "name": "Tiendas bajo los arcos", "coord": [45.4346, 12.3375], "stop": 6},
        {"label": "7-8", "name": "El Campanile", "coord": [45.4340, 12.3389], "stop": 7},
        {"label": "9-10", "name": "Palacio Ducal y la Piazzetta (Loggetta)", "coord": [45.4336, 12.3396], "stop": 9},
        {"label": "11-12", "name": "La laguna y las góndolas (las dos columnas)", "coord": [45.4331, 12.3398], "stop": 11},
        {"label": "13", "name": "Por la Riva", "coord": [45.4332, 12.3407], "stop": 13},
        {"label": "14-15", "name": "Puente de los Suspiros (desde el Ponte della Paglia)", "coord": [45.4335, 12.3412], "stop": 14},
    ],
    "venice-frari-church": [
        {"label": "🚤", "name": "Vaporetto San Tomà (a 10 min a pie)", "coord": [45.4346, 12.3290], "kind": "info"},
        {"label": "1-2", "name": "Campo dei Frari: exterior de la iglesia", "coord": [45.4369, 12.3257], "stop": 1},
        {"label": "3-11", "name": "Interior de la iglesia (ver croquis)", "coord": [45.4367, 12.3266], "stop": 3},
    ],
    "barcelona-city-walk": [
        {"label": "1-2", "name": "Plaça de Catalunya", "coord": [41.387, 2.17], "stop": 1},
        {"label": "3", "name": "La Rambla y la Font de Canaletes", "coord": [41.3855, 2.1697], "stop": 3},
        {"label": "4", "name": "Bajando por La Rambla", "coord": [41.385, 2.1702], "stop": 4},
        {"label": "5", "name": "Carrer de Santa Anna e iglesia de Santa Anna", "coord": [41.3858, 2.1716], "stop": 5},
        {"label": "6", "name": "Avinguda del Portal de l'Àngel", "coord": [41.386, 2.1726], "stop": 6},
        {"label": "7", "name": "Els Quatre Gats", "coord": [41.3857, 2.1736], "stop": 7},
        {"label": "8", "name": "Font de Santa Anna", "coord": [41.3849, 2.174], "stop": 8},
        {"label": "9", "name": "Plaça Nova y torres romanas", "coord": [41.3843, 2.175], "stop": 9},
        {"label": "10", "name": "Casa de l'Ardiaca", "coord": [41.384, 2.1757], "stop": 10},
        {"label": "11", "name": "Catedral: fachada (Pla de la Seu)", "coord": [41.3844, 2.1758], "stop": 11},
        {"label": "12-15", "name": "Interior de la catedral", "coord": [41.3839, 2.1764], "stop": 12},
        {"label": "16", "name": "Claustro de la catedral", "coord": [41.3838, 2.1761], "stop": 16},
        {"label": "17", "name": "Monumento a los Mártires (Plaça de Garriga i Bachs)", "coord": [41.3835, 2.1758], "stop": 17},
        {"label": "18", "name": "Plaça de Sant Felip Neri", "coord": [41.3834, 2.1751], "stop": 18},
        {"label": "19", "name": "El Call (Placeta de Manuel Ribé)", "coord": [41.3827, 2.1755], "stop": 19},
        {"label": "20", "name": "Carrer del Bisbe y su puente", "coord": [41.3833, 2.1764], "stop": 20},
        {"label": "21", "name": "Plaça de Sant Jaume", "coord": [41.3827, 2.177], "stop": 21},
        {"label": "22", "name": "Templo romano de Augusto", "coord": [41.3834, 2.1772], "stop": 22},
        {"label": "23", "name": "Plaça del Rei (fin)", "coord": [41.3841, 2.1775], "stop": 23},
    ],
    "barcelona-eixample-walk": [
        {"label": "M", "name": "Metro Diagonal (salida Passeig de Gràcia)", "coord": [41.396, 2.1603], "kind": "info"},
        {"label": "1-2", "name": "Passeig de Gràcia (desde Diagonal)", "coord": [41.3956, 2.1609], "stop": 1},
        {"label": "3", "name": "La Pedrera / Casa Milà (vista desde la esquina de enfrente)", "coord": [41.3947, 2.1616], "stop": 3},
        {"label": "4", "name": "Carrer de Provença", "coord": [41.3942, 2.161], "stop": 4},
        {"label": "5", "name": "Rambla de Catalunya", "coord": [41.3934, 2.1603], "stop": 5},
        {"label": "6", "name": "Casa Juncosa", "coord": [41.3922, 2.1622], "stop": 6},
        {"label": "7", "name": "Fundació Antoni Tàpies", "coord": [41.3916, 2.1637], "stop": 7},
        {"label": "8", "name": "Manzana de la Discordia: Casa Batlló", "coord": [41.3917, 2.165], "stop": 8},
        {"label": "9", "name": "Casa Amatller", "coord": [41.3915, 2.1652], "stop": 9},
        {"label": "10", "name": "Casa Lleó Morera", "coord": [41.3913, 2.1656], "stop": 10},
        {"label": "11", "name": "Manzana de la Discordia desde la vereda de enfrente", "coord": [41.3919, 2.1657], "stop": 11},
        {"label": "12", "name": "Carrer d'Aragó y Pau Claris", "coord": [41.3933, 2.1661], "stop": 12},
        {"label": "13", "name": "Carrer de València (Casa Elizalde y Queviures Múrria)", "coord": [41.3945, 2.1656], "stop": 13},
        {"label": "14", "name": "Floristeria Navarro", "coord": [41.3955, 2.1668], "stop": 14},
        {"label": "15", "name": "Mercat de la Concepció", "coord": [41.3959, 2.1682], "stop": 15},
        {"label": "16", "name": "Del mercado a la iglesia (Aragó y Bruc)", "coord": [41.3951, 2.1683], "stop": 16},
        {"label": "17", "name": "Iglesia de la Concepció", "coord": [41.3946, 2.1675], "stop": 17},
        {"label": "18", "name": "Carrer d'Aragó, de vuelta al Passeig de Gràcia", "coord": [41.3938, 2.1666], "stop": 18},
        {"label": "19", "name": "Passeig de Gràcia hacia la Plaça de Catalunya (fin)", "coord": [41.3904, 2.1671], "stop": 19},
    ],
    "madrid-city-walk": [
        {"label": "1-2", "name": "Puerta del Sol (estatua de Carlos III)", "coord": [40.4171, -3.7036], "stop": 1},
        {"label": "3", "name": "Real Casa de Correos y Kilómetro Cero", "coord": [40.4167, -3.7037], "stop": 3},
        {"label": "4", "name": "Confitería La Mallorquina", "coord": [40.4166, -3.7047], "stop": 4},
        {"label": "5", "name": "Calle de Postas y Museo del Jamón", "coord": [40.4161, -3.7057], "stop": 5},
        {"label": "6", "name": "Calle de Postas hacia la Plaza Mayor", "coord": [40.4158, -3.7064], "stop": 6},
        {"label": "7-8", "name": "Plaza Mayor (estatua de Felipe III)", "coord": [40.4155, -3.7074], "stop": 7},
        {"label": "9", "name": "Bar La Torre del Oro (Plaza Mayor 26)", "coord": [40.4159, -3.7078], "stop": 9},
        {"label": "10", "name": "Mercado de San Miguel", "coord": [40.4153, -3.709], "stop": 10},
        {"label": "11", "name": "Plaza del Conde de Miranda (convento del Corpus Christi)", "coord": [40.4148, -3.7098], "stop": 11},
        {"label": "12", "name": "Plaza de la Villa y Casa de la Villa", "coord": [40.4154, -3.7103], "stop": 12},
        {"label": "13", "name": "Calle Mayor (monumento del atentado de 1906)", "coord": [40.4154, -3.7121], "stop": 13},
        {"label": "14", "name": "Catedral de la Almudena", "coord": [40.4157, -3.7145], "stop": 14},
        {"label": "15", "name": "Palacio Real (Plaza de la Armería)", "coord": [40.4168, -3.7141], "stop": 15},
        {"label": "16", "name": "Plaza de Oriente (estatua de Felipe IV)", "coord": [40.4183, -3.7122], "stop": 16},
        {"label": "17", "name": "Teatro Real y Plaza de Isabel II", "coord": [40.4181, -3.7096], "stop": 17},
        {"label": "18", "name": "Calle del Arenal e iglesia de San Ginés", "coord": [40.4176, -3.7078], "stop": 18},
        {"label": "19", "name": "Chocolatería San Ginés", "coord": [40.4168, -3.7068], "stop": 19},
        {"label": "20", "name": "Calle del Arenal, segunda parte", "coord": [40.4172, -3.7057], "stop": 20},
        {"label": "21", "name": "Puerta del Sol: la Mariblanca (fin)", "coord": [40.4169, -3.7045], "stop": 21},
    ],
    "sevilla-city-walk": [
        {"label": "1-2", "name": "Plaza Virgen de los Reyes (fuente)", "coord": [37.3863, -5.9919], "stop": 1},
        {"label": "3", "name": "Catedral y Giralda", "coord": [37.3866, -5.9922], "stop": 3},
        {"label": "4", "name": "Puerta del Perdón (calle Alemanes)", "coord": [37.3867, -5.9933], "stop": 4},
        {"label": "5", "name": "Avenida de la Constitución (Puerta de la Asunción)", "coord": [37.3858, -5.9939], "stop": 5},
        {"label": "6", "name": "Archivo de Indias y Plaza del Triunfo", "coord": [37.3851, -5.9922], "stop": 6},
        {"label": "7", "name": "Real Alcázar: Patio de Banderas", "coord": [37.3845, -5.9914], "stop": 7},
        {"label": "8", "name": "Entrada al Barrio de Santa Cruz (callejón de la Judería)", "coord": [37.3841, -5.9904], "stop": 8},
        {"label": "9", "name": "Callejón del Agua", "coord": [37.3845, -5.9893], "stop": 9},
        {"label": "10", "name": "Plaza de Santa Cruz", "coord": [37.3851, -5.9884], "stop": 10},
        {"label": "11", "name": "Casa de Murillo y convento de Santa Teresa", "coord": [37.3857, -5.989], "stop": 11},
        {"label": "12", "name": "Callejones del beso (calle Reinoso)", "coord": [37.3855, -5.9896], "stop": 12},
        {"label": "13", "name": "Plaza de los Venerables", "coord": [37.3851, -5.9898], "stop": 13},
        {"label": "14", "name": "Plaza de Doña Elvira", "coord": [37.3848, -5.9905], "stop": 14},
        {"label": "15", "name": "Convento de la Encarnación: dulces de las monjas (fin)", "coord": [37.3857, -5.9917], "stop": 15},
    ],
}

# Pistas regeneradas: versión > 1 para que la app no use la copia vieja guardada en el celular.
AUDIO_VERSIONS = {
    "siena-city-walk": {n: 2 for n in range(11, 21)},  # numeración del mapa oficial (nov. 2026)
}

TOUR_TITLES = {
    "rome-pantheon": "Panteón",
    "rome-colosseum": "Coliseo",
    "rome-forum": "Foro Romano",
    "rome-heart": "El corazón de Roma",
    "rome-jewish-ghetto": "Barrio Judío",
    "rome-ostia-antica": "Ostia Antica",
    "rome-sistine-chapel": "Capilla Sixtina",
    "rome-st-peters-basilica": "Basílica de San Pedro",
    "rome-trastevere": "Trastévere",
    "rome-vatican-museums": "Museos Vaticanos",
    "rome-vatican-pinacoteca": "Pinacoteca Vaticana",
    "florence-accademia-david": "Galería de la Accademia (David)",
    "florence-bargello": "Bargello",
    "florence-renaissance-walk": "Paseo del Renacimiento",
    "florence-san-marco-museum": "Museo de San Marcos",
    "florence-uffizi-gallery": "Galería Uffizi",
    "pitti-palatine-gallery": "Palacio Pitti: Galería Palatina",
    "siena-city-walk": "Paseo por Siena",
    "sangimignano-walk": "Paseo por San Gimignano",
    "venice-grand-canal": "Paseo en barco por el Gran Canal",
    "venice-st-marks-square": "Plaza San Marcos",
    "venice-st-marks-basilica": "Basílica de San Marcos",
    "venice-frari-church": "Iglesia de los Frari",
    "barcelona-city-walk": "Paseo por Barcelona",
    "barcelona-eixample-walk": "Paseo por el Eixample",
    "madrid-city-walk": "Paseo por Madrid",
    "sevilla-city-walk": "Paseo por Sevilla",
}


def parse_md(path):
    title, stops = None, []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
        elif m := STOP_RE.match(line):
            stops.append({"n": int(m[1]), "name": m[2].strip(), "label": m[5],
                          "en_start": int(m[3]) * 60 + int(m[4]), "text": ""})
        elif stops:
            stops[-1]["text"] += line + "\n"
    for s in stops:
        s["text"] = re.sub(r"\n{3,}", "\n\n", s["text"]).strip()
    return title, stops


def load_cache():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    return {}


def save_cache(c):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(c, open(CACHE, "w"), ensure_ascii=False, indent=1)


# Pistas: nombres de parada que no son lugares (se heredan). También traducciones.
NO_GEO_HINTS = [
    r"^introducci[oó]n", r"^bienvenid", r"^resumen", r"^fin\b",
    r"^despedida", r"^cierre", r"^pr[óo]ximo", r"salida\s+del",
    r"^conclusi[oó]n", r"^antes de empezar", r"^palabras finales",
]


def should_skip_geo(name):
    low = name.lower()
    return any(re.search(p, low) for p in NO_GEO_HINTS)


def geocode(query, cache):
    if query in cache:
        return cache[query]
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": query, "format": "json", "limit": 1, "accept-language": "es"})
    req = urllib.request.Request(url, headers={"User-Agent": "audioguias-personales/1 (noreply@anthropic.com)"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=20))
        time.sleep(1.1)  # política de Nominatim: 1 req/segundo
        if r:
            cache[query] = [float(r[0]["lat"]), float(r[0]["lon"])]
        else:
            cache[query] = None
    except Exception as e:
        print(f"  geocode ERROR '{query}': {e}", file=sys.stderr)
        cache[query] = None
    return cache[query]


def main():
    cache = load_cache()
    data = {"cities": {}, "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    for cid, city in CITIES.items():
        city_entry = {k: city[k] for k in ("name", "country", "center", "zoom")}
        city_entry["tours"] = []
        for tour in city["tours"]:
            md = os.path.join(TRAD, tour + ".md")
            if not os.path.exists(md) or not os.path.exists(md[:-3] + ".notas.md"):
                print(f"  AVISO: falta {md} o sus notas (traducción sin terminar)", file=sys.stderr); continue
            full_title, stops = parse_md(md)
            tour_coord = TOUR_COORDS.get(tour, city["center"])
            for s in stops:
                s["coord"] = tour_coord
                s["coord_source"] = "tour"
            city_entry["tours"].append({
                "id": tour,
                "title": TOUR_TITLES.get(tour, tour),
                "full_title": full_title,
                "coord": tour_coord,
                "maps": tour_maps(tour),
                "map_url": (tour_maps(tour) or [{"url": None}])[0]["url"],
                "points": TOUR_POINTS.get(tour),
                "stops": [{"n": s["n"], "label": s["label"], "v": AUDIO_VERSIONS.get(tour, {}).get(s["n"], 1),
                            "name": s["name"], "text": s["text"],
                            "en_start": s["en_start"], "coord": s["coord"]} for s in stops],
            })
            print(f"  {tour}: {len(stops)} paradas", file=sys.stderr)
        data["cities"][cid] = city_entry
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"Escrito {OUT}", file=sys.stderr)


main()
