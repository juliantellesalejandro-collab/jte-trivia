#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  JTE TRIVIA  ·  juego de preguntas en español
#  © juliantelles · 2026 · todos los derechos reservados
#  Hecho a mano, con 🧠. No uses este código sin permiso.
#  ─────────────────────────────────────────────────────────────
import hashlib
import json
import os
import random
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta

ES_WINDOWS = sys.platform == "win32"
if ES_WINDOWS:
    import msvcrt
else:
    import termios
    import tty

NOMBRE_JUGADOR = ""
NOMBRE_JUGADOR = ""
VERSION = "1.3"
TIEMPO_RELOJ = 10
ULTIMA_PARTIDA = None

PREGUNTAS = {
    "Ciencia": [
        ("¿Cuál es el planeta más grande del sistema solar?", ["Tierra", "Marte", "Júpiter", "Saturno"], 2),
        ("¿Cuál es el símbolo químico del oro?", ["Au", "Ag", "Fe", "Cu"], 0),
        ("¿Cuántos huesos tiene el cuerpo humano adulto?", ["206", "192", "240", "180"], 0),
        ("¿Qué gas respiramos principalmente del aire?", ["Oxígeno", "Nitrógeno", "Hidrógeno", "Dióxido de carbono"], 1),
        ("¿Cuál es la velocidad aproximada de la luz en el vacío?", ["300.000 km/s", "150.000 km/s", "1.000.000 km/s", "3.000 km/s"], 0),
        ("¿Qué teoría explica la formación del universo?", ["Deriva continental", "Big Bang", "Gravedad cuántica", "Evolución química"], 1),
        ("¿Cuál es el órgano más grande del cuerpo humano?", ["El hígado", "Los pulmones", "La piel", "El cerebro"], 2),
        ("¿Cuántos electrones tiene el átomo de hidrógeno?", ["1", "2", "4", "0"], 0),
        ("¿Qué vitamina produce nuestro cuerpo con la luz del sol?", ["La vitamina D", "La vitamina C", "La vitamina B12", "La vitamina A"], 0),
        ("¿Cuál es el planeta conocido como el planeta rojo?", ["Marte", "Venus", "Júpiter", "Mercurio"], 0),
        ("¿Cuántos planetas tiene el sistema solar?", ["8", "7", "9", "10"], 0),
        ("¿Qué gas es el más abundante en la atmósfera de la Tierra?", ["Nitrógeno", "Oxígeno", "Dióxido de carbono", "Argón"], 0),
        ("¿Quién formuló la teoría de la gravedad universal?", ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking"], 0),
        ("¿Cuál es el animal terrestre más rápido del mundo?", ["El guepardo", "El león", "El caballo", "El antílope"], 0),
        ("¿Qué célula del cuerpo humano es la más grande?", ["El óvulo", "El espermatozoide", "El glóbulo rojo", "La neurona"], 0),
        ("¿Qué proteína de la sangre transporta el oxígeno?", ["La hemoglobina", "La insulina", "El colágeno", "La queratina"], 0),
        ("¿Qué órgano produce la insulina?", ["El páncreas", "El hígado", "El estómago", "Los riñones"], 0),
        ("¿Cuál es el metal más ligero que existe?", ["El litio", "El hierro", "El aluminio", "El cobre"], 0),
        ("¿Cuántas veces al año gira la Tierra alrededor del Sol?", ["1", "2", "12", "365"], 0),
        ("¿Cuál es la unidad básica de la vida?", ["La célula", "El átomo", "El tejido", "El órgano"], 0),
        ("¿Cuál es el elemento más abundante en el universo?", ["Helio", "Hidrógeno", "Oxígeno", "Carbono"], 1),
        ("¿Quién formuló las tres leyes del movimiento?", ["Albert Einstein", "Galileo Galilei", "Isaac Newton", "Nikola Tesla"], 2),
        ("¿Qué fuerza atrae los objetos hacia la Tierra?", ["La inercia", "La gravedad", "El magnetismo", "La fricción"], 1),
        ("¿Qué tipo de animal es la ballena?", ["Un pez", "Un anfibio", "Un reptil", "Un mamífero"], 3),
        ("¿Cuál es el planeta más cercano al Sol?", ["Venus", "Marte", "Mercurio", "La Tierra"], 2),
        ("¿Cuántos dientes tiene un adulto promedio?", ["32", "28", "30", "34"], 0),
        ("¿Qué hueso protege el cerebro?", ["La columna", "El cráneo", "Las costillas", "La pelvis"], 1),
        ("¿Qué gas usan las plantas en la fotosíntesis?", ["Oxígeno", "Nitrógeno", "Hidrógeno", "Dióxido de carbono"], 3),
        ("¿En qué unidad se mide la frecuencia?", ["El vatio", "El hercio", "El julio", "El voltio"], 1),
        ("¿Qué parte del ojo enfoca la luz?", ["La retina", "El cristalino", "La pupila", "El iris"], 1),
    ],
    "Historia": [
        ("¿En qué año llegó Cristóbal Colón a América?", ["1492", "1521", "1488", "1519"], 0),
        ("¿Quién fue el primer emperador romano?", ["Julio César", "Augusto", "Nerón", "Marco Aurelio"], 1),
        ("¿Qué civilización construyó Machu Picchu?", ["Inca", "Maya", "Azteca", "Olmeca"], 0),
        ("¿En qué año terminó la Segunda Guerra Mundial?", ["1943", "1944", "1945", "1946"], 2),
        ("¿Qué muro cayó en 1989?", ["El de Berlín", "El de Adriano", "La Gran Muralla China", "El Muro de las Lamentaciones"], 0),
        ("¿Quién escribió las obras El Quijote?", ["Lope de Vega", "Miguel de Cervantes", "Garcilaso de la Vega", "Francisco de Quevedo"], 1),
        ("¿En qué país se originó el Renacimiento?", ["Francia", "Inglaterra", "Italia", "España"], 2),
        ("¿Quién fue la primera mujer en ganar un Premio Nobel?", ["Marie Curie", "Ada Lovelace", "Rosalind Franklin", "Jane Goodall"], 0),
        ("¿En qué año cayó Tenochtitlan en manos de los españoles?", ["1521", "1492", "1519", "1550"], 0),
        ("¿Quién escribió la Declaración de Independencia de los EE.UU.?", ["Thomas Jefferson", "George Washington", "Benjamín Franklin", "Abraham Lincoln"], 0),
        ("¿Qué imperio se disolvió al terminar la Primera Guerra Mundial?", ["El otomano", "El romano", "El español", "El mongol"], 0),
        ("¿Qué civilización inventó el número cero?", ["La maya", "La egipcia", "La griega", "La romana"], 0),
        ("¿Quién dirigió la independencia de la India por la vía no violenta?", ["Mahatma Gandhi", "Jawaharlal Nehru", "León Tolstói", "Martin Luther King"], 0),
        ("¿En qué año se fundó la ONU?", ["1945", "1939", "1950", "1960"], 0),
        ("¿Qué ciudad fue la capital del Imperio Azteca?", ["Tenochtitlan", "Cusco", "Chichén Itzá", "Teotihuacán"], 0),
        ("¿Cuál fue la ruta comercial más importante entre China y Europa?", ["La Ruta de la Seda", "La Ruta de la Pimienta", "El Camino de Santiago", "La Ruta de la Sal"], 0),
        ("¿Quién fue el primer presidente de los Estados Unidos?", ["George Washington", "John Adams", "Thomas Jefferson", "James Monroe"], 0),
        ("¿Qué pueblo construyó las pirámides de Giza?", ["Los egipcios", "Los mayas", "Los aztecas", "Los sumerios"], 0),
        ("¿Quién fue rey de Francia conocido como 'el Rey Sol'?", ["Luis XIV", "Napoleón Bonaparte", "Luis XVI", "Carlos IX"], 0),
        ("¿En qué año se disolvió la Unión Soviética?", ["1991", "1989", "1985", "2000"], 0),
        ("¿Quién fue el primer presidente de México?", ["Guadalupe Victoria", "Benito Juárez", "Porfirio Díaz", "Vicente Guerrero"], 0),
        ("¿En qué año llegó Hernán Cortés a territorio mexicano?", ["1492", "1519", "1521", "1494"], 1),
        ("¿Qué civilización construyó las pirámides de Teotihuacán?", ["Los mexicas", "Los olmecas", "Los teotihuacanos", "Los mayas"], 2),
        ("¿En qué año se consumó la Independencia de México?", ["1810", "1821", "1824", "1848"], 1),
        ("¿Quién escribió 'El llano en llamas'?", ["Juan Rulfo", "Octavio Paz", "Carlos Fuentes", "Elena Poniatowska"], 0),
        ("¿Qué faraona gobernó el Antiguo Egipto?", ["Hatshepsut", "Cleopatra", "Nefertiti", "Isis"], 0),
        ("¿En qué año comenzó la Revolución Francesa?", ["1776", "1789", "1812", "1848"], 1),
        ("¿Qué emperador romano mandó construir el Coliseo?", ["Augusto", "Nerón", "Vespasiano", "Trajano"], 2),
        ("¿Qué país invadió la Unión Soviética en 1941?", ["Alemania", "Italia", "Japón", "Turquía"], 0),
        ("¿Quién fue el primer humano en pisar la Luna?", ["Buzz Aldrin", "Michael Collins", "Yuri Gagarin", "Neil Armstrong"], 3),
    ],
    "Geografía": [
        ("¿Cuál es el río más largo del mundo?", ["El Amazonas", "El Nilo", "El Yangtsé", "El Misisipi"], 0),
        ("¿Cuál es el país más grande del mundo?", ["Canadá", "China", "Rusia", "Estados Unidos"], 2),
        ("¿En qué continente está el desierto del Sahara?", ["Asia", "África", "Australia", "América"], 1),
        ("¿Cuál es la capital de Australia?", ["Sídney", "Melbourne", "Canberra", "Perth"], 2),
        ("¿Cuál es la montaña más alta del mundo?", ["El Kilimanjaro", "El Everest", "El Aconcagua", "El Mont Blanc"], 1),
        ("¿Cuántos países tiene la Unión Europea actualmente?", ["23", "25", "27", "30"], 2),
        ("¿Cuál es el océano más grande?", ["El Atlántico", "El Índico", "El Pacífico", "El Ártico"], 2),
        ("¿Qué país tiene forma de bota en Europa?", ["España", "Portugal", "Italia", "Grecia"], 2),
        ("¿Cuál es la capital de Japón?", ["Tokio", "Osaka", "Kioto", "Sapporo"], 0),
        ("¿Qué estrecho separa Europa de África?", ["El de Gibraltar", "El Bósforo", "El de Magallanes", "El de la Mancha"], 0),
        ("¿Cuál es la isla más grande del mundo?", ["Groenlandia", "Madagascar", "Sumatra", "Borneo"], 0),
        ("¿Cuál es el punto más bajo de la superficie terrestre?", ["El Mar Muerto", "El Mar Caspio", "El Mar Rojo", "El Mar Mediterráneo"], 0),
        ("¿Cuál es la capital de Canadá?", ["Ottawa", "Toronto", "Montreal", "Vancouver"], 0),
        ("¿Qué cordillera atraviesa Sudamérica de norte a sur?", ["Los Andes", "Las Rocosas", "Los Alpes", "Los Urales"], 0),
        ("¿Cuál es el país más pequeño del mundo?", ["El Vaticano", "Mónaco", "San Marino", "Liechtenstein"], 0),
        ("¿Qué mar se encuentra entre Europa y África?", ["El Mediterráneo", "El Báltico", "El Negro", "El Norte"], 0),
        ("¿Cuál es la capital de Turquía?", ["Ankara", "Estambul", "Esmirna", "Antalya"], 0),
        ("¿Qué río atraviesa la ciudad de El Cairo?", ["El Nilo", "El Éufrates", "El Jordán", "El Tigris"], 0),
        ("¿Cuál es el continente más seco del planeta?", ["Antártida", "África", "Australia", "Asia"], 0),
        ("¿Qué país tiene la mayor cantidad de husos horarios?", ["Francia", "Rusia", "China", "Estados Unidos"], 0),
        ("¿Qué país europeo ocupa la mayor superficie?", ["Francia", "Rusia", "Ucrania", "España"], 1),
        ("¿Cuál es el lago más grande del mundo?", ["El Titicaca", "El Victoria", "El Caspio", "El Superior"], 2),
        ("¿En qué océano se encuentra Madagascar?", ["El Atlántico", "El Pacífico", "El Índico", "El Ártico"], 2),
        ("¿Cuál es la capital de Argentina?", ["Buenos Aires", "Córdoba", "Rosario", "Mendoza"], 0),
        ("¿Qué desierto cubre el sur de Mongolia y el norte de China?", ["El Gobi", "El Sahara", "El de Atacama", "El de Arabia"], 0),
        ("¿Cuál es el río más caudaloso del mundo?", ["El Nilo", "El Amazonas", "El Misisipi", "El Yangtsé"], 1),
        ("¿En qué continente está Brasil?", ["África", "Asia", "Europa", "América"], 3),
        ("¿Cuál es la capital de Egipto?", ["Alejandría", "El Cairo", "Luxor", "Giza"], 1),
        ("¿Qué país europeo tiene forma de bota?", ["Italia", "Portugal", "Grecia", "Croacia"], 0),
        ("¿Cuál es el volcán activo más alto del mundo?", ["El Ojos del Salado", "El Teide", "El Popocatépetl", "El Cotopaxi"], 0),
    ],
    "Arte y Cultura": [
        ("¿Quién pintó la Mona Lisa?", ["Miguel Ángel", "Rafael", "Leonardo da Vinci", "Caravaggio"], 2),
        ("¿En qué país se originó el tango?", ["México", "Argentina", "Cuba", "Brasil"], 1),
        ("¿Quién escribió 'Cien años de soledad'?", ["Julio Cortázar", "Pablo Neruda", "Gabriel García Márquez", "Mario Vargas Llosa"], 2),
        ("¿Qué instrumento tiene 88 teclas?", ["El piano", "El órgano", "El clavecín", "El acordeón"], 0),
        ("¿Quién es considerado el padre de la literatura española?", ["Miguel de Cervantes", "Federico García Lorca", "Antonio Machado", "Benito Pérez Galdós"], 0),
        ("¿Cuál es la obra más famosa de Shakespeare?", ["Hamlet", "Romeo y Julieta", "Macbeth", "Otelo"], 1),
        ("¿En qué ciudad está el museo del Louvre?", ["Londres", "Madrid", "París", "Roma"], 2),
        ("¿Qué estilo musical se originó en Jamaica?", ["El reggae", "El jazz", "El blues", "El bossa nova"], 0),
        ("¿Quién escribió 'La Divina Comedia'?", ["Dante Alighieri", "Petrarca", "Boccaccio", "Virgilio"], 0),
        ("¿Qué pintor vendió su oreja y es famoso por sus girasoles?", ["Vincent van Gogh", "Pablo Picasso", "Salvador Dalí", "Claude Monet"], 0),
        ("¿Quién compuso 'Las cuatro estaciones'?", ["Antonio Vivaldi", "Johann Sebastian Bach", "Wolfgang Mozart", "Ludwig Beethoven"], 0),
        ("¿Qué escultura en mármol creó Miguel Ángel?", ["El David", "El Pensador", "La Venus de Milo", "La Victoria de Samotracia"], 0),
        ("¿Quién escribió 'Orgullo y prejuicio'?", ["Jane Austen", "Mary Shelley", "Charlotte Brontë", "Emily Brontë"], 0),
        ("¿Qué artista pintó 'El grito'?", ["Edvard Munch", "Pablo Picasso", "Salvador Dalí", "Joan Miró"], 0),
        ("¿Qué género musical dio origen al rock and roll?", ["El blues", "El jazz", "El country", "El gospel"], 0),
        ("¿Quién es conocido como el Rey del Pop?", ["Michael Jackson", "Elvis Presley", "Prince", "Freddie Mercury"], 0),
        ("¿Qué instrumento de tres cuerdas es típico de la música rusa?", ["La balalaica", "La bandurria", "El sitar", "La cítara"], 0),
        ("¿Quién escribió 'La Odisea'?", ["Homero", "Sófocles", "Platón", "Esopo"], 0),
        ("¿Qué lugar famoso se encuentra en Londres?", ["El Big Ben", "La Torre Eiffel", "El Coliseo", "La Estatua de la Libertad"], 0),
        ("¿Qué artista pintó el techo de la Capilla Sixtina?", ["Miguel Ángel", "Leonardo da Vinci", "Rafael", "Donatello"], 0),
        ("¿Quién pintó 'La última cena'?", ["Miguel Ángel", "Leonardo da Vinci", "Rafael", "Botticelli"], 1),
        ("¿En qué país nació el compositor Mozart?", ["Italia", "Francia", "Austria", "Alemania"], 2),
        ("¿Qué escritor mexicano ganó el Premio Nobel de Literatura?", ["Octavio Paz", "Juan Rulfo", "Carlos Fuentes", "Alfonso Reyes"], 0),
        ("¿Quién esculpió 'El Pensador'?", ["Miguel Ángel", "Auguste Rodin", "Donatello", "Bernini"], 1),
        ("¿Qué género musical mexicano se interpreta con guitarrón y trompetas?", ["El mariachi", "La banda", "El son", "El bolero"], 0),
        ("¿Quién escribió 'Rayuela'?", ["Julio Cortázar", "Mario Vargas Llosa", "Gabriel García Márquez", "Vicente Huidobro"], 0),
        ("¿Qué pintor es famoso por sus autorretratos con la oreja vendada?", ["Vincent van Gogh", "Paul Gauguin", "Paul Cézanne", "Rembrandt"], 0),
        ("¿Qué instrumento de cuerda tiene 47 cuerdas?", ["El arpa", "La guitarra", "El violín", "El contrabajo"], 0),
        ("¿Qué película dirigió Steven Spielberg?", ["Avatar", "Titanic", "Parque Jurásico", "Interstellar"], 2),
        ("¿En qué museo se exhibe 'La Gioconda'?", ["El Prado", "Los Uffizi", "El Louvre", "El British"], 2),
    ],
    "Deportes": [
        ("¿Cuántos jugadores tiene un equipo de fútbol en la cancha?", ["9", "10", "11", "12"], 2),
        ("¿Cada cuántos años se celebran los Juegos Olímpicos de verano?", ["2", "4", "3", "5"], 1),
        ("¿Qué país ganó el primer Mundial de fútbol en 1930?", ["Brasil", "Italia", "Uruguay", "Argentina"], 2),
        ("¿Cuántos puntos vale un triple en baloncesto?", ["2", "3", "4", "5"], 1),
        ("¿Quién es conocido como 'El Rey' del tenis español?", ["Rafael Nadal", "Carlos Alcaraz", "David Ferrer", "Juan Martín del Potro"], 0),
        ("¿Cuántos sets se necesitan para ganar un partido de tenis en un Grand Slam masculino?", ["2", "3", "4", "5"], 3),
        ("¿Qué deporte se juega en el estadio de Wembley?", ["Cricket", "Fútbol", "Rugby", "Béisbol"], 1),
        ("¿Qué país es conocido como la cuna del críquet?", ["India", "Australia", "Inglaterra", "Pakistán"], 2),
        ("¿Cuántos anillos tiene el símbolo olímpico?", ["5", "4", "6", "7"], 0),
        ("¿Qué país ha ganado más Copas del Mundo de fútbol?", ["Brasil", "Alemania", "Italia", "Argentina"], 0),
        ("¿Qué deporte se juega en la Copa Davis?", ["Tenis", "Bádminton", "Squash", "Pádel"], 0),
        ("¿En qué país se inventó el fútbol moderno?", ["Inglaterra", "Brasil", "Uruguay", "España"], 0),
        ("¿Cuántos jugadores tiene un equipo de baloncesto en cancha?", ["5", "6", "7", "8"], 0),
        ("¿Cuál es la distancia oficial de una maratón?", ["42,195 km", "40 km", "50 km", "35 km"], 0),
        ("¿Qué boxeador fue conocido como 'The Greatest'?", ["Muhammad Ali", "Mike Tyson", "Manny Pacquiao", "Floyd Mayweather"], 0),
        ("¿En qué deporte se usa un taco y bolas de colores?", ["Billar", "Bolos", "Golf", "Curling"], 0),
        ("¿Qué equipo ganó la primera Copa de Europa en 1956?", ["El Real Madrid", "El Barcelona", "El Benfica", "El Milan"], 0),
        ("¿En qué juego se usan fichas llamadas torres, alfiles y caballos?", ["El ajedrez", "Las damas", "El go", "El backgammon"], 0),
        ("¿Qué país organizó los Juegos Olímpicos de 2008?", ["China", "Japón", "Reino Unido", "Corea del Sur"], 0),
        ("¿Qué deporte se practica en Wimbledon?", ["El tenis", "El críquet", "El golf", "El polo"], 0),
        ("¿Qué selección ganó el Mundial de fútbol de 1986?", ["Brasil", "Italia", "Alemania", "Argentina"], 3),
        ("¿Cuántas jugadoras juegan por equipo en un partido de vóley?", ["Tres", "Dos", "Seis", "Cinco"], 2),
        ("¿En qué país se inventó el baloncesto?", ["Estados Unidos", "Canadá", "Reino Unido", "España"], 0),
        ("¿Cuántos jugadores disputan por equipo un partido de balonmano?", ["7", "6", "5", "9"], 0),
        ("¿Qué tenista ganó 20 títulos de Grand Slam en individuales?", ["Roger Federer", "Rafael Nadal", "Novak Djokovic", "Andy Murray"], 0),
        ("¿Cuál es el deporte nacional de Japón?", ["El kendo", "El sumo", "El judo", "El karate"], 1),
        ("¿En qué país se celebra el Tour de Francia?", ["España", "Italia", "Francia", "Bélgica"], 2),
        ("¿Qué boxeador mexicano se conoce como 'El Cañón'?", ["Julio César Chávez", "Jorge Arce", "Canelo Álvarez", "Rubén Olivares"], 0),
        ("¿Cuántos jugadores forman un equipo de béisbol en el campo?", ["9", "10", "8", "11"], 0),
        ("¿Qué atleta jamaicano batió récords en los 100 metros?", ["Usain Bolt", "Yohan Blake", "Asafa Powell", "Michael Johnson"], 0),
    ],
    "Tecnología": [
        ("¿Qué significa CPU?", ["Unidad Central de Proceso", "Unidad de Cómputo Personal", "Circuito de Procesamiento Universal", "Unidad de Control de Programas"], 0),
        ("¿Quién es conocido como el padre de la computadora moderna?", ["Alan Turing", "Bill Gates", "Steve Jobs", "Charles Babbage"], 0),
        ("¿Qué sistema operativo desarrolló Google para móviles?", ["iOS", "Android", "Windows Phone", "HarmonyOS"], 1),
        ("¿Qué es la RAM?", ["Memoria de acceso aleatorio", "Memoria de archivos rápidos", "Repositorio de aplicaciones móviles", "Red de área amplia"], 0),
        ("¿En qué año se lanzó el primer iPhone?", ["2005", "2006", "2007", "2008"], 2),
        ("¿Qué lenguaje de programación se usa principalmente para crear páginas web interactivas?", ["C++", "Python", "JavaScript", "Ruby"], 2),
        ("¿Qué significa el término 'código abierto'?", ["Software libre y modificable", "Software con código cifrado", "Software solo para programadores", "Software gratuito sin licencia"], 0),
        ("¿Cuál es la unidad de medida del almacenamiento más grande?", ["Gigabyte", "Megabyte", "Terabyte", "Kilobyte"], 2),
        ("¿Qué empresa creó el sistema operativo Windows?", ["Microsoft", "Apple", "IBM", "Google"], 0),
        ("¿Qué significa USB?", ["Bus serie universal", "Unidad de sistema básico", "Bus de seguridad universal", "Unidad superior binaria"], 0),
        ("¿Qué lenguaje se usa para estructurar una página web?", ["HTML", "SQL", "Python", "Java"], 0),
        ("¿Cuántos bits tiene un byte?", ["8", "16", "32", "64"], 0),
        ("¿Qué formato de imagen comprime con pérdida de calidad?", ["JPEG", "PNG", "GIF", "BMP"], 0),
        ("¿Qué significa LED?", ["Diodo emisor de luz", "Láser eléctrico digital", "Línea eléctrica de datos", "Dispositivo emisor de tonalidad"], 0),
        ("¿Qué sistema operativo móvil es de código abierto?", ["Android", "iOS", "Windows Phone", "HarmonyOS"], 0),
        ("¿Qué dispositivo usa satélites para ubicarse?", ["El GPS", "El USB", "El Bluetooth", "El decodificador"], 0),
        ("¿Qué mujer es considerada la primera programadora de la historia?", ["Ada Lovelace", "Grace Hopper", "Margaret Hamilton", "Katherine Johnson"], 0),
        ("¿Qué red conecta dispositivos sin cables a corta distancia?", ["El Bluetooth", "El GPS", "El láser", "El NFC"], 0),
        ("¿Cuál es el buscador más usado del mundo?", ["Google", "Bing", "DuckDuckGo", "Yahoo"], 0),
        ("¿Cuál es el sistema operativo de Apple para sus computadoras?", ["macOS", "iOS", "Linux", "Windows"], 0),
        ("¿En qué año se lanzó la primera versión pública de Windows?", ["1985", "1990", "1981", "1995"], 0),
        ("¿Qué significa HTTP?", ["Protocolo de transferencia de hipertexto", "Sistema de transmisión de páginas", "Lenguaje de marcado web", "Red de hipertexto común"], 0),
        ("¿Qué empresa fabrica los procesadores Ryzen?", ["Intel", "AMD", "Qualcomm", "NVIDIA"], 1),
        ("¿Qué conector usan los cargadores de teléfonos modernos?", ["USB Type-C", "Micro-USB", "Lightning", "USB-B"], 0),
        ("¿Qué lenguaje de programación usa la extensión .js?", ["Python", "JavaScript", "Java", "Ruby"], 1),
        ("¿Cómo se llama el servicio de nube de Apple?", ["iCloud", "Google Drive", "OneDrive", "Dropbox"], 0),
        ("¿Qué personas crearon WhatsApp?", ["Mark Zuckerberg", "Larry Page", "Jack Dorsey", "Brian Acton y Jan Koum"], 3),
        ("¿Qué chip de 8 bits fue famoso en los ordenadores de los 80?", ["El 6502", "El Pentium", "El Core i7", "El Snapdragon"], 0),
        ("¿Qué significa SSD?", ["Unidad de estado sólido", "Disco de estado sólido", "Sistema de datos sólido", "Almacenamiento sólido digital"], 0),
        ("¿Qué red social fundó Jack Dorsey?", ["Instagram", "Facebook", "Twitter", "LinkedIn"], 2),
    ],
}

LETRAS = "ABCD"

AZUL = "\033[94m"
CIAN = "\033[96m"
MORADO = "\033[95m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
NEGRITA = "\033[1m"
RESET = "\033[0m"


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\n  [ENTER] para continuar... ")


def separador():
    print(CIAN + "-" * 46 + RESET)


def titulo():
    letras = [
        ["██████", "    ██", "    ██", "██  ██", " ████ "],
        ["██████", "  ██  ", "  ██  ", "  ██  ", "  ██  "],
        ["██████", "██    ", "██████", "██    ", "██████"],
    ]
    colores = [CIAN, AZUL, MORADO]
    ancho = 50

    def fila(contenido="", visible=None):
        if visible is None:
            visible = len(contenido)
        print(AZUL + "|" + RESET + contenido + " " * max(0, ancho - visible) + AZUL + "|" + RESET)

    print(AZUL + "+" + "-" * ancho + "+" + RESET)
    for r in range(5):
        piezas = [colores[i] + letras[i][r] + RESET for i in range(3)]
        fila("   " + "  ".join(piezas), 3 + 25)
    fila()
    tagline = MORADO + NEGRITA + "✦ JTE TRIVIA ✦" + RESET + CIAN + "  Gran juego de preguntas" + RESET
    fila("   " + tagline, 3 + 14 + 27)
    print(AZUL + "+" + "-" * ancho + "+" + RESET)
    print(CIAN + "   ✦ Hecho por juliantelles • 2026 · v" + VERSION + " ✦" + RESET)


def menu_principal():
    limpiar_pantalla()
    titulo()
    print()
    print("  [1] ⚡ Jugar partida rápida")
    print("  [2] 🎯 Elegir categoría")
    print("  [3] 📝 Preguntas personalizadas")
    print("  [4] 🏆 Clasificación (Ranked)")
    print("  [5] 📊 Ver mis récords")
    print("  [6] 🔒 Cuenta privada")
    print("  [7] 🎲 Desafío diario")
    print("  [8] 🏅 Mis logros")
    print("  [0] Salir")

    while True:
        opcion = input("  Elige una opción: ").strip()
        if opcion in ("1", "2", "3", "4", "5", "6", "7", "8", "0"):
            return opcion
        print("  ⚠ Opción inválida, intenta de nuevo.")


def elegir_modo():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  ⚡ MODO DE JUEGO" + RESET + "\n")
    print("  [1] 🐢 Normal (sin tiempo)")
    print(f"  [2] ⏱ Contrarreloj ({TIEMPO_RELOJ} s por pregunta)")
    print()
    while True:
        opcion = input("  Elige una opción: ").strip()
        if opcion == "1":
            return "normal"
        if opcion == "2":
            return "reloj"
        print("  ⚠ Opción inválida, intenta de nuevo.")


def input_con_tiempo(prompt, segundos):
    if not sys.stdin.isatty():
        return input(prompt + " ").strip().upper()
    sys.stdout.write(prompt + "  ⏱ " + AMARILLO + f"[{segundos}s]{RESET} ")
    sys.stdout.flush()
    inicio = time.monotonic()
    resto = segundos
    respuesta = ""
    fd = sys.stdin.fileno()

    if ES_WINDOWS:
        respuesta = ""
        while time.monotonic() - inicio < segundos:
            if msvcrt.kbhit():
                tecla = msvcrt.getwch()
                if tecla in ("\r", "\n"):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    return respuesta.strip().upper()
                if tecla in ("\x00", "\xe0"):
                    msvcrt.getwch()
                    continue
                if tecla == "\b":
                    if respuesta:
                        respuesta = respuesta[:-1]
                        sys.stdout.write("\b \b")
                    continue
                respuesta += tecla
                sys.stdout.write(tecla)
            restante = segundos - int(time.monotonic() - inicio)
            if restante != resto:
                resto = restante
                sys.stdout.write("\r\033[K" + prompt + "  ⏱ " + AMARILLO +
                                 f"[{resto}s]{RESET} " + respuesta)
            sys.stdout.flush()
        sys.stdout.write("\r\033[K" + prompt + "  ⏱ " + ROJO + "[tiempo agotado]" + RESET + "\n")
        return ""
    try:
        viejo = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        import select
        while time.monotonic() - inicio < segundos:
            restante = segundos - int(time.monotonic() - inicio)
            if restante != resto:
                resto = restante
                sys.stdout.write("\r\033[K" + prompt + "  ⏱ " + AMARILLO +
                                 f"[{resto}s]{RESET} " + respuesta)
                sys.stdout.flush()
            listo, _, _ = select.select([fd], [], [], 0.1)
            if not listo:
                continue
            tecla = os.read(fd, 1).decode(errors="replace")
            if tecla in ("\r", "\n"):
                sys.stdout.write("\r\033[K\n")
                sys.stdout.flush()
                return respuesta.strip().upper()
            if tecla == "\x7f":
                if respuesta:
                    respuesta = respuesta[:-1]
                    sys.stdout.write("\b \b")
                continue
            respuesta += tecla
            sys.stdout.write(tecla)
            sys.stdout.flush()
        sys.stdout.write("\r\033[K" + prompt + "  ⏱ " + ROJO + "[tiempo agotado]" + RESET + "\n")
        return ""
    finally:
        sys.stdout.write("\r\033[K")
        termios.tcsetattr(fd, termios.TCSADRAIN, viejo)


def elegir_categoria():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  CATEGORÍAS DISPONIBLES:" + RESET + "\n")
    categorias = list(PREGUNTAS.keys())
    for i, cat in enumerate(categorias, 1):
        print(f"  {CIAN}[{i}]{RESET} {cat}")
    print(f"  {CIAN}[{len(categorias)+1}]{RESET} 🎲 Mixta (todas las categorías)")
    print()

    while True:
        opcion = input("  Elige una categoría: ").strip()
        if opcion.isdigit():
            n = int(opcion)
            if 1 <= n <= len(categorias):
                return categorias[n - 1]
            if n == len(categorias) + 1:
                return None
        print("  ⚠ Opción inválida, intenta de nuevo.")


def preparar_banco(categoria):
    if isinstance(categoria, list):
        banco = list(categoria)
    elif categoria is None:
        banco = []
        for preguntas in PREGUNTAS.values():
            banco.extend(preguntas)
    else:
        banco = list(PREGUNTAS[categoria])

    usadas = set(cargar_historial())
    nuevas = [q for q in banco if q[0] not in usadas]
    repetidas = [q for q in banco if q[0] in usadas]
    random.shuffle(nuevas)
    random.shuffle(repetidas)
    limite = 10 if len(banco) > 10 else len(banco)
    banco = nuevas[:limite]
    if len(banco) < limite:
        banco += repetidas[:limite - len(banco)]

    for i in range(len(banco)):
        respuesta, opciones, correcta = banco[i]
        emparejadas = [(j, opciones[j]) for j in range(len(opciones))]
        random.shuffle(emparejadas)
        nuevas_opciones = [o for _, o in emparejadas]
        nueva_correcta = next(j for j, (idx, _) in enumerate(emparejadas) if idx == correcta)
        banco[i] = (respuesta, nuevas_opciones, nueva_correcta)

    random.shuffle(banco)
    return banco[:10] if len(banco) > 10 else banco


def jugar(banco, categoria, modo="normal", repetir=True):
    global ULTIMA_PARTIDA
    ULTIMA_PARTIDA = None
    limpiar_pantalla()
    titulo()
    print()
    total = len(banco)
    aciertos = 0
    tiempos = []
    print(CIAN + NEGRITA + f"  {'CATEGORÍA MIXTA' if categoria is None else 'CATEGORÍA: ' + categoria.upper()}" + RESET)
    print(f"  {AMARILLO}{total}{RESET} preguntas | Jugador: {NOMBRE_JUGADOR}"
          + (f" | ⏱ Contrarreloj ({TIEMPO_RELOJ}s)" if modo == "reloj" else "") + "\n")
    input("  Pulsa ENTER para empezar...")

    for i, (pregunta, opciones, correcta) in enumerate(banco, 1):
        limpiar_pantalla()
        titulo()
        print()
        print(CIAN + NEGRITA + f"  Pregunta {i}/{total}" + RESET + f"  |  Aciertos: {AMARILLO}{aciertos}{RESET}")
        separador()
        print(f"  {pregunta}\n")

        for j, opcion in enumerate(opciones):
            print(f"    {LETRAS[j]}) {opcion}")

        print()
        if modo == "reloj":
            t0 = time.monotonic()
            respuesta = input_con_tiempo("  Tu respuesta (A/B/C/D o S): ", TIEMPO_RELOJ)
            tiempos.append(time.monotonic() - t0)
            if respuesta == "S":
                print("\n  Partida abandonada. ¡Nos vemos!\n")
                return False
            if respuesta not in LETRAS:
                print(ROJO + "\n  ⏱ ¡Tiempo agotado! Esta pregunta no cuenta." + RESET)
                respuesta = ""
        else:
            while True:
                respuesta = input("  Tu respuesta (A/B/C/D o S para salir): ").strip().upper()
                if respuesta == "S":
                    print("\n  Partida abandonada. ¡Nos vemos!\n")
                    return False
                if respuesta in LETRAS:
                    break
                print("  ⚠ Escribe una letra válida (A, B, C o D).")

        if respuesta in LETRAS:
            letra_correcta = LETRAS[correcta]
            if respuesta == letra_correcta:
                print(VERDE + NEGRITA + "\n  ✅ ¡Correcto! Muy bien." + RESET)
                aciertos += 1
            else:
                print(ROJO + NEGRITA + "\n  ❌ Incorrecto." + RESET +
                      f" La respuesta era {letra_correcta}) {opciones[correcta]}")
        else:
            print(ROJO + "\n  ⏱ Sin respuesta: fallo." + RESET)

        pausa()

    limpiar_pantalla()
    titulo()
    print()
    print(VERDE + NEGRITA + "  🏁 FIN DE LA PARTIDA" + RESET)
    separador()
    print(f"  Aciertos: {AMARILLO}{aciertos}{RESET} de {total}")
    porcentaje = (aciertos / total) * 100
    print(f"  Porcentaje: {VERDE}{porcentaje:.0f}%{RESET}")
    separador()

    if porcentaje == 100:
        mensaje = "🌟 ¡PERFECTO! Eres un robot de trivia."
    elif porcentaje >= 75:
        mensaje = "🏆 ¡Excelente! Nivel experto."
    elif porcentaje >= 50:
        mensaje = "👍 Bien jugado, pero puedes mejorar."
    elif porcentaje >= 25:
        mensaje = "🙂 No está mal, ¡sigue practicando!"
    else:
        mensaje = "😬 Tocará estudiar un poquito..."
    print(NEGRITA + f"  {mensaje}" + RESET)
    separador()

    if modo == "reloj" and tiempos:
        total_t = sum(tiempos)
        bonus = 0
        for t in tiempos:
            bonus += max(0, TIEMPO_RELOJ - round(t))
        rapida = min(tiempos)
        print(f"  ⏱ Tiempo total: {total_t:.1f}s  |  Respuesta más rápida: {rapida:.1f}s")
        print(f"  ⚡ Bonus por rapidez: {VERDE}+{bonus}{RESET} puntos (no afecta el ranking)")
        separador()

    ULTIMA_PARTIDA = {"aciertos": aciertos, "total": total}
    guardar_record(aciertos, total, categoria)
    guardar_historial(banco)

    if servidor_online():
        resp = pedir_http("/api/resultado", {"nombre": NOMBRE_JUGADOR, "clave": CLAVE_ACTUAL,
                                             "aciertos": aciertos, "total": total})
        if resp and resp.get("ok"):
            resp["tier"] = tier_del(resp["rating"])
            cambio = resp
        else:
            SERVIDOR_EN_LINEA = False
            registrar_resultado(aciertos, total)
            cambio = actualizar_ranking(NOMBRE_JUGADOR, aciertos, total)
    else:
        registrar_resultado(aciertos, total)
        cambio = actualizar_ranking(NOMBRE_JUGADOR, aciertos, total)

    print()
    print(MORADO + NEGRITA + "  🏆 TU RANKING" + RESET)
    if cambio["delta"] >= 0:
        signo = VERDE + f"+{cambio['delta']}"
    else:
        signo = ROJO + str(cambio["delta"])
    print(f"  Puntos: {signo}{RESET}  →  ⭐ {AMARILLO}{cambio['rating']}{RESET}  ({cambio['tier']})")
    racha = f"   🔥 racha {cambio['racha']} partidas" if cambio["racha"] else ""
    print(f"  Posición en el ranking: #{cambio['pos']}{racha}")
    if cambio["pos"] == 1:
        print(AMARILLO + "  🥇 ¡ERES EL NÚMERO UNO!" + RESET)
    separador()

    nuevos = verificar_logros(resultado=ULTIMA_PARTIDA, modo=modo)
    if nuevos:
        print(AMARILLO + "  🏅 ¡Logros desbloqueados: " + ", ".join(nuevos) + "!" + RESET)
        pausa()

    if repetir:
        return jugar_otra_vez()
    return False


def cargar_historial():
    if not os.path.exists(HISTORIAL):
        return []
    try:
        with open(HISTORIAL) as f:
            datos = json.load(f)
        return datos if isinstance(datos, list) else []
    except (ValueError, OSError):
        return []


def guardar_historial(banco):
    usadas = [p for p, _, _ in banco]
    hist = cargar_historial()
    for p in usadas:
        if p not in hist:
            hist.append(p)
    hist = hist[-30:]
    with open(HISTORIAL, "w") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)


def leer_tecla():
    if ES_WINDOWS:
        primero = msvcrt.getwch()
        if primero in ("\x00", "\xe0"):
            segundo = msvcrt.getwch()
            if segundo in ("H", "K"):
                return "ARRIBA"
            if segundo in ("P", "M"):
                return "ABAJO"
            return None
        if primero in ("\r", "\n"):
            return "ENTER"
        if primero == "\x03":
            raise KeyboardInterrupt
        return None
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.buffer.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    if ch == b"\x1b":
        seq = sys.stdin.buffer.read(2)
        if seq in (b"[A", b"[D"):
            return "ARRIBA"
        if seq in (b"[B", b"[C"):
            return "ABAJO"
        return None
    if ch in (b"\r", b"\n"):
        return "ENTER"
    if ch == b"\x03":
        raise KeyboardInterrupt
    return None


def jugar_otra_vez():
    if not sys.stdin.isatty():
        while True:
            r = input("\n  ¿Jugar otra partida? (s/n): ").strip().lower()
            if r in ("s", "si", "sí", "yes", "y"):
                return True
            if r in ("n", "no"):
                return False
            print("  ⚠ Responde s o n.")

    print()
    print(AMARILLO + "  🎮 ¿Quieres jugar otra partida?" + RESET)
    print(CIAN + "  Usa las flechas  ◀ ▲ ▼ ▶  para elegir y ENTER para confirmar." + RESET)
    seleccion = 0

    def pintar():
        if seleccion == 0:
            linea = "  " + VERDE + "▶ [Sí]" + RESET + "  [No]"
        else:
            linea = "  [Sí]  " + VERDE + "▶ [No]" + RESET
        sys.stdout.write("\r\033[2K" + linea)
        sys.stdout.flush()

    pintar()
    while True:
        tecla = leer_tecla()
        if tecla == "ARRIBA":
            seleccion = 0
        elif tecla == "ABAJO":
            seleccion = 1
        elif tecla == "ENTER":
            sys.stdout.write("\r\033[2K\n")
            sys.stdout.flush()
            return seleccion == 0
        else:
            continue
        pintar()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDS = os.path.join(BASE_DIR, ".trivia_records.txt")
HISTORIAL = os.path.join(BASE_DIR, ".historial.json")
RANKINGS = os.path.join(BASE_DIR, "rankings.json")
RESULTADOS = os.path.join(BASE_DIR, "resultados.json")
ARCHIVO_SERVIDOR = os.path.join(BASE_DIR, "servidor_config.txt")

SERVIDOR_EN_LINEA = None
CLAVE_ACTUAL = ""


def url_servidor():
    env = os.environ.get("TRIVIA_SERVIDOR")
    if env:
        return env.rstrip("/")
    if os.path.exists(ARCHIVO_SERVIDOR):
        s = open(ARCHIVO_SERVIDOR, encoding="utf-8").read().strip()
        if s:
            return s.rstrip("/")
    return "http://127.0.0.1:8090"


def pedir_http(ruta, datos=None):
    url = url_servidor() + ruta
    try:
        peticion = urllib.request.Request(
            url,
            data=json.dumps(datos).encode() if datos is not None else None,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(peticion, timeout=3) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def servidor_online():
    global SERVIDOR_EN_LINEA
    if SERVIDOR_EN_LINEA is None:
        SERVIDOR_EN_LINEA = bool(pedir_http("/api/ping"))
    return SERVIDOR_EN_LINEA

TIERRAS = [
    (2000, "Maestro", "👑", AZUL),
    (1800, "Diamante", "💎", CIAN),
    (1600, "Oro", "🥇", AMARILLO),
    (1400, "Plata", "🥈", VERDE),
]


def tier_del(rating):
    for umbral, nombre, icono, _ in TIERRAS:
        if rating >= umbral:
            return f"{icono} {nombre}"
    return "🥉 Bronce"


def cargar_rankings():
    if not os.path.exists(RANKINGS):
        return {}
    try:
        with open(RANKINGS) as f:
            datos = json.load(f)
        return datos if isinstance(datos, dict) else {}
    except (ValueError, OSError):
        return {}


def guardar_rankings(datos):
    with open(RANKINGS, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def posicion_ranking(nombre):
    datos = cargar_rankings()
    orden = sorted(datos.items(), key=lambda kv: kv[1]["rating"], reverse=True)
    for i, (n, _) in enumerate(orden, 1):
        if n == nombre:
            return i
    return None


def actualizar_ranking(nombre, aciertos, total):
    datos = cargar_rankings()
    d = datos.get(nombre, {"rating": 1200, "partidas": 0, "racha": 0, "mejor": 0})
    pct = aciertos / total if total else 0
    delta = round(32 * (pct - 0.5) * 2)
    d["rating"] = max(100, d["rating"] + delta)
    d["partidas"] += 1
    d["mejor"] = max(d["mejor"], aciertos)
    if pct >= 0.5:
        d["racha"] += 1
    else:
        d["racha"] = 0
    datos[nombre] = d
    guardar_rankings(datos)
    return {"delta": delta, "rating": d["rating"], "tier": tier_del(d["rating"]),
            "pos": posicion_ranking(nombre), "racha": d["racha"]}


def ver_ranking():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  🏆 CLASIFICACIÓN (RANKED)" + RESET)
    separador()
    if servidor_online():
        resp = pedir_http("/api/ranking?" + urllib.parse.urlencode({"yo": NOMBRE_JUGADOR}))
        if resp and "ranking" in resp:
            orden = [(n, d) for n, d in resp["ranking"] if es_visible(n)]
        else:
            SERVIDOR_EN_LINEA = False
            orden = sorted(cargar_rankings().items(), key=lambda kv: kv[1]["rating"], reverse=True)
    else:
        orden = sorted(cargar_rankings().items(), key=lambda kv: kv[1]["rating"], reverse=True)
    orden = [(n, d) for n, d in orden if es_visible(n)]
    if not orden:
        print("\n  Todavía no hay clasificación.")
        print("  Juega una partida para entrar al ranking.")
    else:
        print()
        for i, (n, d) in enumerate(orden, 1):
            print(f"  {i:>2}.  🎮 {n:<14} ⭐ {d['rating']:>4}   {tier_del(d['rating'])}"
                  + (f"   🔥 racha {d['racha']}" if d["racha"] else ""))
    print()
    separador()
    pausa()


def cargar_resultados():
    if not os.path.exists(RESULTADOS):
        return []
    try:
        with open(RESULTADOS) as f:
            datos = json.load(f)
        return datos if isinstance(datos, list) else []
    except (ValueError, OSError):
        return []


def registrar_resultado(aciertos, total):
    datos = cargar_resultados()
    datos.append({"usuario": NOMBRE_JUGADOR, "aciertos": aciertos, "total": total,
                  "fecha": date.today().isoformat()})
    with open(RESULTADOS, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def mejores_del_periodo(dias, limite=10):
    datos = cargar_resultados()
    desde = (date.today() - timedelta(days=dias)).isoformat()
    acum = {}
    for r in datos:
        if r.get("fecha", "") < desde:
            continue
        d = acum.setdefault(r.get("usuario", ""), {"aciertos": 0, "partidas": 0})
        d["aciertos"] += r.get("aciertos", 0)
        d["partidas"] += 1
    orden = sorted(acum.items(), key=lambda kv: kv[1]["aciertos"], reverse=True)
    return orden[:limite]


def ver_mejores(dias, etiqueta):
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  " + etiqueta + RESET)
    separador()
    if servidor_online():
        resp = pedir_http("/api/periodo?" + urllib.parse.urlencode({"dias": dias, "yo": NOMBRE_JUGADOR}))
        if resp and "tabla" in resp:
            tabla = [(n["usuario"], {"aciertos": n["aciertos"], "partidas": n["partidas"]})
                     for n in resp["tabla"] if es_visible(n["usuario"])]
        else:
            SERVIDOR_EN_LINEA = False
            tabla = mejores_del_periodo(dias)
    else:
        tabla = mejores_del_periodo(dias)
    tabla = [(n, d) for n, d in tabla if es_visible(n)]
    if not tabla:
        print("\n  Sin datos en este periodo todavía.")
        print("  🎮 Juega una partida para aparecer aquí.")
    else:
        print()
        for i, (n, d) in enumerate(tabla, 1):
            if i <= 3:
                medalla = ["🥇", "🥈", "🥉"][i - 1]
            else:
                medalla = f"{i:>2}."
            print(f"  {medalla}  🎮 {n:<14} ✅ {d['aciertos']} aciertos  ({d['partidas']} partidas)")
    print()
    separador()
    pausa()


def ver_jugadores():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  👥 JUGADORES REGISTRADOS" + RESET)
    separador()
    if servidor_online():
        resp = pedir_http("/api/jugadores?" + urllib.parse.urlencode({"yo": NOMBRE_JUGADOR}))
        if resp and "nombres" in resp:
            usuarios = {n: "" for n in resp["nombres"] if es_visible(n)}
        else:
            SERVIDOR_EN_LINEA = False
            usuarios = cargar_usuarios()
    else:
        usuarios = cargar_usuarios()
    usuarios = {n: "" for n in usuarios if es_visible(n)}
    if not usuarios:
        print("\n  Nadie se ha registrado todavía.")
    else:
        print()
        for i, n in enumerate(sorted(usuarios), 1):
            print(f"  {i:>2}.  🎮 {n}")
    print()
    separador()
    pausa()


def menu_clasificacion():
    while True:
        limpiar_pantalla()
        titulo()
        print()
        print(MORADO + NEGRITA + "  🏆 CLASIFICACIÓN GENERAL" + RESET + "\n")
        print("  [1] 👥 Jugadores registrados")
        print("  [2] 🏆 Ranking general (todos los tiempos)")
        print("  [3] 🥇 Mejores de la semana")
        print("  [4] 🥈 Mejores del mes")
        print("  [5] 🏅 Mejores del año")
        print("  [0] ↩ Volver al menú")
        print()
        opcion = input("  Elige una opción: ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            ver_jugadores()
        elif opcion == "2":
            ver_ranking()
        elif opcion == "3":
            ver_mejores(7, "🥇 MEJORES DE LA SEMANA")
        elif opcion == "4":
            ver_mejores(30, "🥈 MEJORES DEL MES")
        elif opcion == "5":
            ver_mejores(365, "🏅 MEJORES DEL AÑO")
        else:
            print("  ⚠ Opción inválida, intenta de nuevo.")


def guardar_record(aciertos, total, categoria):
    os.makedirs(os.path.dirname(RECORDS), exist_ok=True)
    nombre_cat = "Mixta" if categoria is None else categoria
    with open(RECORDS, "a") as f:
        f.write(f"{NOMBRE_JUGADOR}|{aciertos}/{total}|{nombre_cat}\n")


def ver_records():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  📊 MIS RÉCORDS" + RESET)
    separador()
    if not os.path.exists(RECORDS):
        print("\n  Todavía no tienes récords. ¡Juega una partida!")
    else:
        with open(RECORDS) as f:
            lineas = [l.strip() for l in f if l.strip()]
        propios = [l for l in lineas if l.startswith(NOMBRE_JUGADOR + "|")]
        if not propios:
            print("\n  Todavía no tienes récords. ¡Juega una partida!")
        else:
            print()
            for i, linea in enumerate(propios[-10:], 1):
                partes = linea.split("|")
                if len(partes) == 3:
                    print(f"  {i}.  ✅ {partes[1]}  |  🗂 {partes[2]}")
    separador()
    pausa()


ARCHIVO_PERSONAL = os.path.join(BASE_DIR, "preguntas_personales.json")


def cargar_personalizadas():
    if not os.path.exists(ARCHIVO_PERSONAL):
        return []
    with open(ARCHIVO_PERSONAL) as f:
        try:
            datos = json.load(f)
        except (ValueError, OSError):
            return []
    preguntas = []
    for d in datos:
        if isinstance(d, dict) and "pregunta" in d and "opciones" in d and "correcta" in d:
            preguntas.append((d["pregunta"], list(d["opciones"]), int(d["correcta"])))
    return preguntas


def guardar_personalizadas(preguntas):
    os.makedirs(os.path.dirname(ARCHIVO_PERSONAL), exist_ok=True)
    datos = [{"pregunta": p, "opciones": o, "correcta": c} for p, o, c in preguntas]
    with open(ARCHIVO_PERSONAL, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def anadir_pregunta():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  ➕ AÑADIR PREGUNTA NUEVA" + RESET + "\n")
    pregunta = input(CIAN + "  Pregunta: " + RESET).strip()
    if not pregunta:
        print(ROJO + "  ⚠ La pregunta no puede estar vacía." + RESET)
        pausa()
        return
    opciones = []
    for j in range(4):
        while True:
            op = input(f"  {CIAN}Opción {LETRAS[j]}:{RESET} ").strip()
            if op:
                break
            print("  ⚠ La opción no puede estar vacía.")
        opciones.append(op)
    while True:
        respuesta = input("  ¿Cuál es la correcta? " + AMARILLO + "(1-4): " + RESET).strip()
        if respuesta in ("1", "2", "3", "4"):
            correcta = int(respuesta) - 1
            break
        print(ROJO + "  ⚠ Escribe 1, 2, 3 o 4." + RESET)
    preguntas = cargar_personalizadas()
    preguntas.append((pregunta, opciones, correcta))
    guardar_personalizadas(preguntas)
    print(VERDE + NEGRITA + "\n  ✅ ¡Pregunta guardada!" + RESET)
    pausa()


def ver_personalizadas():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  📃 MIS PREGUNTAS" + RESET)
    separador()
    preguntas = cargar_personalizadas()
    if not preguntas:
        print("\n  Todavía no tienes preguntas guardadas.")
    else:
        print()
        for i, (p, o, c) in enumerate(preguntas, 1):
            print(f"  {CIAN}{i}.{RESET} {p}")
            for j, op in enumerate(o):
                marca = VERDE + "✔" + RESET if j == c else "  "
                print(f"     {marca} {LETRAS[j]}) {op}")
            print()
    separador()
    pausa()


def borrar_personalizadas():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  🗑 BORRAR PREGUNTAS" + RESET)
    separador()
    print("\n  ⚠ Esta acción borrará TODAS tus preguntas.")
    print("  No se puede deshacer.\n")
    while True:
        confirmar = input("  ¿Seguro? " + AMARILLO + "(sí/no): " + RESET).strip().lower()
        if confirmar in ("si", "sí", "s"):
            guardar_personalizadas([])
            print(VERDE + "\n  ✅ Preguntas borradas." + RESET)
            pausa()
            return
        if confirmar in ("no", "n"):
            print("\n  ↩ Operación cancelada.")
            pausa()
            return
        print("  ⚠ Responde con sí o no.")


def menu_personalizadas():
    while True:
        limpiar_pantalla()
        titulo()
        print()
        print(MORADO + NEGRITA + "  📝 MIS PREGUNTAS PERSONALIZADAS" + RESET + "\n")
        print("  [1] ➕ Añadir pregunta nueva")
        print("  [2] ▶️  Jugar con mis preguntas")
        print("  [3] 📃 Ver mis preguntas")
        if cargar_personalizadas():
            print("  [4] 🗑 Borrar todas mis preguntas")
        print("  [0] ↩ Volver al menú")
        print()
        opcion = input("  Elige una opción: ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            anadir_pregunta()
        elif opcion == "2":
            preguntas = cargar_personalizadas()
            if not preguntas:
                print(ROJO + "\n  ⚠ No tienes preguntas guardadas. Añade alguna primero." + RESET)
                pausa()
            else:
                print(VERDE + f"\n  ¡Jugando con {len(preguntas)} preguntas tuyas!" + RESET)
                pausa()
                while jugar(preparar_banco(preguntas), "MIS PREGUNTAS"):
                    preguntas = cargar_personalizadas()
                    if not preguntas:
                        break
                return
        elif opcion == "3":
            ver_personalizadas()
        elif opcion == "4" and cargar_personalizadas():
            borrar_personalizadas()
        elif opcion == "":
            continue
        else:
            print("  ⚠ Opción inválida, intenta de nuevo.")


USUARIOS = os.path.join(BASE_DIR, "usuarios.json")


def cargar_usuarios():
    if not os.path.exists(USUARIOS):
        return {}
    try:
        with open(USUARIOS) as f:
            datos = json.load(f)
        return datos if isinstance(datos, dict) else {}
    except (ValueError, OSError):
        return {}


def guardar_usuarios(usuarios):
    with open(USUARIOS, "w") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)


PRIVADOS = os.path.join(BASE_DIR, "privados.json")


def cargar_privados():
    if not os.path.exists(PRIVADOS):
        return set()
    try:
        with open(PRIVADOS, encoding="utf-8") as f:
            datos = json.load(f)
        if isinstance(datos, list):
            return {str(n) for n in datos}
    except (ValueError, OSError):
        pass
    return set()


def guardar_privados(privados):
    try:
        with open(PRIVADOS, "w", encoding="utf-8") as f:
            json.dump(sorted(privados), f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def es_privado(nombre):
    if servidor_online():
        resp = pedir_http("/api/privados")
        if resp and isinstance(resp.get("privados"), list):
            return nombre in {str(n) for n in resp["privados"]}
    return nombre in cargar_privados()


def es_visible(nombre):
    if nombre == NOMBRE_JUGADOR:
        return True
    return not es_privado(nombre)


def cambiar_estado_cuenta(nuevo_estado):
    if servidor_online():
        clave = leer_contraseña(f"  Contraseña de '{NOMBRE_JUGADOR}' para confirmar: ")
        resp = pedir_http("/api/privado", {"nombre": NOMBRE_JUGADOR, "clave": clave, "privado": nuevo_estado})
        if not resp or not resp.get("ok"):
            return False, "Contraseña incorrecta o servidor no disponible."
        privados = cargar_privados()
        if nuevo_estado:
            privados.add(NOMBRE_JUGADOR)
        else:
            privados.discard(NOMBRE_JUGADOR)
        guardar_privados(privados)
        SERVIDOR_EN_LINEA = True
        return True, ""
    usuarios = cargar_usuarios()
    if NOMBRE_JUGADOR not in usuarios:
        return False, "Tu cuenta no está registrada en esta máquina."
    clave = leer_contraseña(f"  Contraseña de '{NOMBRE_JUGADOR}' para confirmar: ")
    if hash_contraseña(NOMBRE_JUGADOR, clave) != usuarios[NOMBRE_JUGADOR]:
        return False, "Contraseña incorrecta."
    privados = cargar_privados()
    if nuevo_estado:
        privados.add(NOMBRE_JUGADOR)
    else:
        privados.discard(NOMBRE_JUGADOR)
    guardar_privados(privados)
    return True, ""


def menu_cuenta():
    while True:
        limpiar_pantalla()
        titulo()
        print()
        print(MORADO + NEGRITA + "  🔒 CUENTA PRIVADA" + RESET)
        separador()
        privada = es_privado(NOMBRE_JUGADOR)
        print(f"\n  Cuenta: 🎮 {NOMBRE_JUGADOR}")
        if privada:
            print("  Estado: " + VERDE + "🔒 Privada — los demás NO verán tus datos ni tu nombre." + RESET)
            print("  [1] 🌐 Hacer mi cuenta pública")
        else:
            print("  Estado: " + AMARILLO + "🌐 Pública — todos pueden ver tus datos y tu nombre." + RESET)
            print("  [1] 🔒 Hacer mi cuenta privada")
        print("  [2] 👀 Ver cómo me ven los demás")
        print("  [0] ↩ Volver al menú")
        print()
        opcion = input("  Elige una opción: ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            ok, error = cambiar_estado_cuenta(not privada)
            if ok:
                print(VERDE + NEGRITA + (f"\n  ✅ Tu cuenta ahora es privada. Nadie más verá tus datos."
                                          if not privada else
                                          "\n  ✅ Tu cuenta ahora es pública. Todos podrán ver tus datos.") + RESET)
            else:
                print(ROJO + f"\n  ⚠ {error}" + RESET)
            pausa()
        elif opcion == "2":
            limpiar_pantalla()
            titulo()
            print()
            print(MORADO + NEGRITA + "  👀 LO QUE VEN LOS DEMÁS" + RESET)
            separador()
            privada_actual = es_privado(NOMBRE_JUGADOR)
            if privada_actual:
                print("\n  🔒 Tu cuenta es privada. Los demás NO verán:")
                print("     • Tu nombre en 'Jugadores registrados'")
                print("     • Tu puesto en el 'Ranking general'")
                print("     • Tus aciertos en la semana/mes/año")
            else:
                print("\n  🌐 Tu cuenta es pública. Todo el mundo ve tus datos.")
            separador()
            pausa()
        else:
            print("  ⚠ Opción inválida, intenta de nuevo.")


DESAFIOS = os.path.join(BASE_DIR, "desafios.json")


def cargar_desafios():
    if not os.path.exists(DESAFIOS):
        return {}
    try:
        with open(DESAFIOS, encoding="utf-8") as f:
            datos = json.load(f)
        return datos if isinstance(datos, dict) else {}
    except (ValueError, OSError):
        return {}


def guardar_desafios(datos):
    try:
        with open(DESAFIOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def banco_del_dia():
    todas = [(p, o, c) for cat in PREGUNTAS.values() for (p, o, c) in cat]
    rng = random.Random(date.today().toordinal())
    return rng.sample(todas, 10)


def menu_desafio():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  🎲 DESAFÍO DIARIO" + RESET)
    separador()
    hoy = date.today().isoformat()
    datos = cargar_desafios()
    d = datos.get(hoy, {}).get(NOMBRE_JUGADOR)
    if d:
        print(f"\n  Ya jugaste el desafío de hoy: ✅ {d['aciertos']}/{d['total']} aciertos.")
        print("  🌙 Vuelve mañana por un reto nuevo.")
    else:
        print("\n  ¡El reto de hoy! 10 preguntas de todas las categorías.")
        print(AMARILLO + "  ⚠ Solo una oportunidad al día y cuenta para tu rating." + RESET)
        print()
        confirmar = input("  ¿Empezar? (sí/no): ").strip().lower()
        if confirmar not in ("si", "sí", "s"):
            print("  ↩ Reto no iniciado.")
            pausa()
            separador()
            return
        banco = banco_del_dia()
        jugar(banco, "DESAFÍO DIARIO", "normal", repetir=False)
        if ULTIMA_PARTIDA:
            datos = cargar_desafios()
            por_dia = datos.setdefault(hoy, {})
            por_dia[NOMBRE_JUGADOR] = {"aciertos": ULTIMA_PARTIDA["aciertos"],
                                       "total": ULTIMA_PARTIDA["total"],
                                       "hecho": True}
            guardar_desafios(datos)
            nuevos = verificar_logros(resultado=ULTIMA_PARTIDA, extra={"desafio"})
            if nuevos:
                print(AMARILLO + "  🏅 ¡Logros desbloqueados: " + ", ".join(nuevos) + "!" + RESET)
                pausa()
    separador()
    pausa()


LOGROS = os.path.join(BASE_DIR, "logros.json")

LOGROS_TODO = [
    ("primer100", "🌟 Cerebro Total", "Consigue un 100% en una partida."),
    ("primera", "👣 Primer paso", "Termina tu primera partida."),
    ("racha5", "🔥 Imparable", "Consigue una racha de 5 partidas seguidas."),
    ("partidas10", "🎮 Pícaro", "Juega 10 partidas."),
    ("partidas50", "🏆 Veterano", "Juega 50 partidas."),
    ("aciertos100", "📚 Sabio", "Acumula 100 aciertos."),
    ("veloz", "⚡ A toda máquina", "Saca un 100% en modo contrarreloj."),
    ("desafio", "🌙 Madrugador", "Juega el desafío diario."),
]


def cargar_logros():
    if not os.path.exists(LOGROS):
        return {}
    try:
        with open(LOGROS, encoding="utf-8") as f:
            datos = json.load(f)
        return datos if isinstance(datos, dict) else {}
    except (ValueError, OSError):
        return {}


def guardar_logros(datos):
    try:
        with open(LOGROS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def _nombre_logro(ident):
    for i, nombre, _ in LOGROS_TODO:
        if i == ident:
            return nombre
    return ident


def verificar_logros(resultado=None, modo="normal", extra=None):
    estra = set(extra or [])
    datos = cargar_logros()
    logrados = set(datos.get(NOMBRE_JUGADOR, []))
    stats = estadisticas_jugador(NOMBRE_JUGADOR)
    partidas = stats["partidas"] if stats else 0
    aciertos = stats["aciertos"] if stats else 0
    racha = cargar_rankings().get(NOMBRE_JUGADOR, {}).get("racha", 0)

    if resultado:
        total = resultado.get("total", 0)
        ok = resultado.get("aciertos", 0)
        if total and ok >= total:
            estra.add("primer100")
            if modo == "reloj":
                estra.add("veloz")
        estra.add("primera")
    if racha >= 5:
        estra.add("racha5")
    if partidas >= 10:
        estra.add("partidas10")
    if partidas >= 50:
        estra.add("partidas50")
    if aciertos >= 100:
        estra.add("aciertos100")

    validos = {ident for ident, _, _ in LOGROS_TODO}
    nuevos = set(estra) & validos - logrados
    if not nuevos:
        return []
    nombres = [_nombre_logro(i) for i in sorted(nuevos)]
    datos[NOMBRE_JUGADOR] = sorted(logrados | nuevos)
    guardar_logros(datos)
    return nombres


def ver_logros():
    limpiar_pantalla()
    titulo()
    print()
    print(MORADO + NEGRITA + "  🏅 MIS LOGROS" + RESET)
    separador()
    logrados = set(cargar_logros().get(NOMBRE_JUGADOR, []))
    if not logrados:
        print("\n  📭 Todavía no tienes logros. ¡Juega para desbloquear el primero!")
    print()
    for ident, nombre, desc in LOGROS_TODO:
        marca = VERDE + "✅" + RESET if ident in logrados else "🔒"
        print(f"  {marca} {nombre}")
        print(f"     {CIAN}{desc}{RESET}")
        print()
    print(f"  {AMARILLO}{len(logrados)}/{len(LOGROS_TODO)}{RESET} logros desbloqueados")
    separador()
    pausa()


def hash_contraseña(nombre, clave):
    d = hashlib.sha256()
    d.update(nombre.encode())
    d.update(b":")
    d.update(clave.encode())
    return d.hexdigest()


def leer_contraseña(prompt):
    if not sys.stdin.isatty():
        return input(prompt).strip()
    if ES_WINDOWS:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        partes = []
        while True:
            tecla = msvcrt.getwch()
            if tecla in ("\r", "\n"):
                sys.stdout.write("\n")
                break
            if tecla in ("\x00", "\xe0"):
                msvcrt.getwch()
                continue
            if tecla in ("\x03", "\x1a"):
                raise KeyboardInterrupt
            if tecla == "\b":
                if partes:
                    partes.pop()
                    sys.stdout.write("\b \b")
                continue
            if not tecla.isprintable():
                continue
            partes.append(tecla)
            sys.stdout.write("*")
        sys.stdout.flush()
        return "".join(partes).strip()
    fd = sys.stdin.fileno()
    viejo = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        nuevo = termios.tcgetattr(fd)
        nuevo[3] = nuevo[3] & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, nuevo)
        texto = input(prompt)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, viejo)
    return texto.strip()


def estadisticas_jugador(nombre):
    partidas = aciertos = total_preg = 0
    if os.path.exists(RECORDS):
        with open(RECORDS) as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 3 and partes[0] == nombre:
                    try:
                        a, t = partes[1].split("/")
                        aciertos += int(a)
                        total_preg += int(t)
                    except (ValueError, IndexError):
                        continue
                    partidas += 1
    if partidas == 0:
        return None
    return {"partidas": partidas, "aciertos": aciertos, "total": total_preg}


def pedir_nombre():
    global NOMBRE_JUGADOR, CLAVE_ACTUAL
    limpiar_pantalla()
    titulo()
    print()
    en_linea = servidor_online()
    if en_linea:
        print(CIAN + "  🌐 Conectado al servidor JTE TRIVIA (modo online)." + RESET)
        print("  Los nombres, récords y rankings se comparten con todos los jugadores.\n")
    else:
        print(CIAN + "  🔐 Modo local (servidor no encontrado)." + RESET)
        print("  Los nombres y récords quedan solo en esta máquina.\n")

    while True:
        nombre = input("  ¿Cómo te llamas? ").strip()
        if not nombre:
            print("  ⚠ Escribe tu nombre.")
            continue

        existe = False
        if en_linea:
            consulta = "/api/existe?" + urllib.parse.urlencode({"nombre": nombre})
            resp = pedir_http(consulta)
            if resp is None:
                print(ROJO + "  ⚠ Se perdió la conexión con el servidor. Cambiando a modo local..." + RESET)
                en_linea = False
                SERVIDOR_EN_LINEA = False
            else:
                existe = resp.get("existe", False)

        if not existe:
            if en_linea:
                while True:
                    clave = input("  Define tu contraseña (se ve al escribir): ")
                    if not clave:
                        print("  ⚠ La contraseña no puede estar vacía.")
                        continue
                    repetida = leer_contraseña("  Repite la contraseña: ")
                    if clave == repetida:
                        break
                    print(ROJO + "  ⚠ Las contraseñas no coinciden." + RESET)
                resp = pedir_http("/api/registrar", {"nombre": nombre, "clave": clave})
                if not resp or not resp.get("ok"):
                    print(ROJO + "  ⚠ No se pudo registrar. Prueba con otro nombre." + RESET)
                    continue
                NOMBRE_JUGADOR = nombre
                CLAVE_ACTUAL = clave
                es_registro = True
                break
            usuarios = cargar_usuarios()
            while True:
                clave = input("  Define tu contraseña (se ve al escribir): ")
                if not clave:
                    print("  ⚠ La contraseña no puede estar vacía.")
                    continue
                repetida = leer_contraseña("  Repite la contraseña: ")
                if clave == repetida:
                    break
                print(ROJO + "  ⚠ Las contraseñas no coinciden." + RESET)
            usuarios[nombre] = hash_contraseña(nombre, clave)
            guardar_usuarios(usuarios)
            NOMBRE_JUGADOR = nombre
            es_registro = True
            break

        if en_linea:
            print(CIAN + f"  🔐 {nombre}, escribe tu contraseña." + RESET)
            for intento in range(1, 4):
                clave = leer_contraseña(f"  Contraseña de '{nombre}': ")
                resp = pedir_http("/api/login", {"nombre": nombre, "clave": clave})
                if resp and resp.get("ok"):
                    NOMBRE_JUGADOR = nombre
                    CLAVE_ACTUAL = clave
                    break
                print(ROJO + "  ❌ Contraseña incorrecta." + RESET)
                if intento == 1:
                    print(AMARILLO + f"  ⚠ El nombre '{nombre}' ya está registrado; solo su dueño puede usarlo." + RESET)
                if intento == 3:
                    print(AMARILLO + f"  No puedes usar '{nombre}': ese nombre ya está en uso." + RESET)
            if NOMBRE_JUGADOR:
                es_registro = False
                break
            continue
        else:
            usuarios = cargar_usuarios()
            print(CIAN + f"  🔐 {nombre}, escribe tu contraseña." + RESET)
            for intento in range(1, 4):
                clave = leer_contraseña(f"  Contraseña de '{nombre}': ")
                if hash_contraseña(nombre, clave) == usuarios[nombre]:
                    NOMBRE_JUGADOR = nombre
                    break
                print(ROJO + "  ❌ Contraseña incorrecta." + RESET)
                if intento == 1:
                    print(AMARILLO + f"  ⚠ El nombre '{nombre}' ya está registrado; solo su dueño puede usarlo." + RESET)
                if intento == 3:
                    print(AMARILLO + f"  No puedes usar '{nombre}': ese nombre ya está en uso." + RESET)
            if NOMBRE_JUGADOR:
                es_registro = False
                break

    if servidor_online():
        resp = pedir_http("/api/stats?" + urllib.parse.urlencode({"nombre": NOMBRE_JUGADOR}))
        if resp and "partidas" in resp:
            stats = resp if resp["partidas"] else None
        else:
            stats = None
    else:
        stats = estadisticas_jugador(NOMBRE_JUGADOR)
    if stats:
        pct = (stats["aciertos"] / stats["total"]) * 100 if stats["total"] else 0
        print(CIAN + f"\n  👋 ¡Hola de nuevo, {NOMBRE_JUGADOR}!" + RESET)
        print("  Ya me conoces: " +
              f"{AMARILLO}{stats['partidas']}{RESET} partidas jugadas y " +
              f"{stats['aciertos']}/{stats['total']} aciertos " +
              f"({VERDE}{pct:.0f}%{RESET}).")
    elif not es_registro:
        print(CIAN + f"\n  🎉 ¡Hola de nuevo, {NOMBRE_JUGADOR}! ¿Listo para otra ronda?" + RESET)
    else:
        print(VERDE + f"\n  👋 ¡Hola, {NOMBRE_JUGADOR}! ¡Buena suerte!" + RESET)
    nuevos = verificar_logros()
    if nuevos:
        print(AMARILLO + "\n  🏅 ¡Logros desbloqueados: " + ", ".join(nuevos) + "!" + RESET)
    pausa()


def main():
    pedir_nombre()
    while True:
        opcion = menu_principal()
        if opcion == "0":
            print("\n  ¡Gracias por jugar! 🎉")
            break
        if opcion == "3":
            menu_personalizadas()
            continue
        if opcion == "4":
            menu_clasificacion()
            continue
        if opcion == "5":
            ver_records()
            continue
        if opcion == "6":
            menu_cuenta()
            continue
        if opcion == "7":
            menu_desafio()
            continue
        if opcion == "8":
            ver_logros()
            continue
        if opcion == "2":
            tema = elegir_categoria()
        else:
            tema = None
        modo = elegir_modo()
        while jugar(preparar_banco(tema), tema, modo):
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  ¡Hasta pronto! 👋\n")
        sys.exit(0)