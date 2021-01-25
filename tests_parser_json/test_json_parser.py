import json
import xml.etree.ElementTree as ET

from pytest import fixture

from tv_grab_fr_telerama import Telerama
from tv_grab_fr_teleloisirs import TeleLoisirs

@fixture
def xmltv_data():
    """Mock grabber write_xmltv method"""

    tree = ET.parse('xmltv_data.xml')
    
    return tree.getroot()

def test_parser_json_telerama(xmltv_data):
    fake_xmltv_data = xmltv_data

    json_file = 'xmltv_test_parser_json.json'

    json_data = Telerama().parser_json(fake_xmltv_data, json_file)

    with open(json_file, "r") as read_file:
        data = json.load(read_file)

    assert data['channels'] == [{
                                "id": "98.api.telerama.fr",
                                "nom": "MULTISPORTS"
                                }, {
                                "id" : "321.api-tel.programme-tv.net",
                                "nom": "BOOMERANG"
                                }]
    assert data['programmes'][0] == {
                                    "start": "20210127230000 +0100",
                                    "stop": "20210128000500 +0100",
                                    "channel": "59.api.telerama.fr",
                                    "audio_subtitles": True,
                                    "sub-title": "Les fantômes",
                                    "desc": "Les années passées à Pise ont fait d'Elena une jeune femme élégante, cultivée et désinhibée. En revenant pour les vacances à Luzzati, le quartier de son enfance, à Naples, elle trouve une Lila battue par son mari et découragée, entièrement dévouée à son rôle de mère. Terrifiée par Stefano, Lila confie ses journaux intimes à Elena...",
                                    "icon": "https://television.telerama.fr/sites/tr_master/files/sheet_media/media/973e5c12-5168-454f-ad4a-91501017d3bb.jpg",
                                    "url": "https://television.telerama.fr/tele/serie/lamie-prodigieuse,n5953605,saison2,episode7.php",
                                    "episode-num": "1.6.0/1",
                                    "public": 12,
                                    "titles": [
                                        "L'amie prodigieuse"
                                    ],
                                    "directors": [
                                        "Saverio Costanzo"
                                    ],
                                    "categories": [
                                        "Série",
                                        "Série dramatique",
                                        "Movie / Drama"
                                    ],
                                    "actors": [
                                        {
                                            "actor": "Gaia Girace",
                                            "role": "Lila Cerullo"
                                        },
                                        {
                                            "actor": "Margherita Mazzucco",
                                            "role": "Elena Greco"
                                        },
                                        {
                                            "actor": "Giovanni Amura",
                                            "role": "Stefano Carracci"
                                        },
                                        {
                                            "actor": "Valentina Acca",
                                            "role": "Nunzia Cerullo"
                                        },
                                        {
                                            "actor": "Giorgia Gargano",
                                            "role": "Nadia Galiani"
                                        },
                                        {
                                            "actor": "Lia Zinno",
                                            "role": "Giuseppina Peluso"
                                        },
                                        {
                                            "actor": "Antonio Milo",
                                            "role": "Silvio Solara"
                                        },
                                        {
                                            "actor": "Christian Giroso",
                                            "role": "Antonio Cappuccio"
                                        }
                                    ],
                                    "writers": [
                                        "Elena Ferrante",
                                        "Francesco Piccolo",
                                        "Laura Paolucci",
                                        "Saverio Costanzo"
                                    ],
                                    "composers": [],
                                    "countries": [
                                        "Italie"
                                    ]
                                }

    assert data['programmes'][1] == {
                                    "start": "20210127230500 +0100",
                                    "stop": "20210128005000 +0100",
                                    "channel": "1399.api.telerama.fr",
                                    "audio_subtitles": True,
                                    "sub-title": "A Dijon",
                                    "desc": "Au sommaire : Mystérieux incendie. Le 28 janvier 2010 les pompiers de Fontaine-lès-Dijon sont appelés pour un incendie. - Qui a tué la femme du maire ? Le 16 avril 2006, Marcelle est retrouvée assassinée. - La cavale du père de famille. Le 21 décembre 1996, à Dijon, un homme signale qu'un meurtre a sans doute été commis rue de la Prévôté.",
                                    "icon": "https://television.telerama.fr/sites/tr_master/files/sheet_media/media/9f2e217e14b228a19fd557bcfc44316e7df5ae84.jpg",
                                    "url": "https://television.telerama.fr/tele/magazine/crimes,12029897,emission76313169.php",
                                    "episode-num": "2..0/1",
                                    "public": 10,
                                    "titles": [
                                        "Crimes"
                                    ],
                                    "directors": [
                                        "Jean-Marc Morandini"
                                    ],
                                    "categories": [
                                        "Magazine",
                                        "Magazine de société",
                                        "Magazines / Reports / Documentary"
                                    ],
                                    "actors": [],
                                    "writers": [],
                                    "composers": [],
                                    "countries": [
                                        "français"
                                    ]
                                }

    assert data['programmes'][2] == {
                                    "start": "20210128235900 +0100",
                                    "stop": "20210129002200 +0100",
                                    "channel": "924.api.telerama.fr",
                                    "audio_subtitles": False,
                                    "sub-title": "Caniche contre gargouille",
                                    "desc": "Alors qu'il tourne une série TV bas de gamme dans un vieil immeuble gothique empli de gargouilles, le tournage et la carrière de Daniel Valentino sont fortement compromis suite à l'attaque d'une gargouille qui semble avoir pris vie. Toute son équipe de techniciens démissionne, aussitôt remplacée par Scooby et ses amis qui prennent l'enquête an main : qui en veut au réalisateur au point de ruiner son film ?...",
                                    "icon": "https://television.telerama.fr/sites/tr_master/files/sheet_media/media/42c7e9b018c03ea3fe00406f1f51ccd37593b911.jpg",
                                    "url": "https://television.telerama.fr/tele/dessin-anime/trop-cool-scooby-doo,17734304,saison1,episode4.php",
                                    "episode-num": "0.3.0/1",
                                    "public": 0,
                                    "titles": [
                                        "Trop cool, Scooby-Doo !",
                                        "Be Cool Scooby-Doo"
                                    ],
                                    "directors": [
                                        "Shaunt Nigoghossian"
                                    ],
                                    "categories": [
                                        "Jeunesse",
                                        "Dessin animé",
                                        "Children's / Youth programmes"
                                    ],
                                    "actors": [],
                                    "writers": [
                                        "Joe Ballarini",
                                        "Marly Halpern-Graser",
                                        "Joe Ruby",
                                        "Ken Spears"
                                    ],
                                    "composers": [],
                                    "countries": [
                                        "américain"
                                    ]
                                }

def test_parser_json_teleloisirs(xmltv_data):
    fake_xmltv_data = xmltv_data

    json_file = 'xmltv_test_parser_json.json'

    json_data = TeleLoisirs().parser_json(fake_xmltv_data, json_file)

    with open(json_file, "r") as read_file:
        data = json.load(read_file)

    assert data['channels'] == [{
                                "id": "98.api.telerama.fr",
                                "nom": "MULTISPORTS"
                                }, {
                                "id" : "321.api-tel.programme-tv.net",
                                "nom": "BOOMERANG"
                                }]
    assert data['programmes'][0] == {
                                    "start": "20210127230000 +0100",
                                    "stop": "20210128000500 +0100",
                                    "channel": "59.api.telerama.fr",
                                    "audio_subtitles": True,
                                    "sub-title": "Les fantômes",
                                    "desc": "Les années passées à Pise ont fait d'Elena une jeune femme élégante, cultivée et désinhibée. En revenant pour les vacances à Luzzati, le quartier de son enfance, à Naples, elle trouve une Lila battue par son mari et découragée, entièrement dévouée à son rôle de mère. Terrifiée par Stefano, Lila confie ses journaux intimes à Elena...",
                                    "icon": "https://television.telerama.fr/sites/tr_master/files/sheet_media/media/973e5c12-5168-454f-ad4a-91501017d3bb.jpg",
                                    "url": "https://television.telerama.fr/tele/serie/lamie-prodigieuse,n5953605,saison2,episode7.php",
                                    "episode-num": "1.6.0/1",
                                    "public": 12,
                                    "titles": [
                                        "L'amie prodigieuse"
                                    ],
                                    "directors": [
                                        "Saverio Costanzo"
                                    ],
                                    "categories": [
                                        "Série",
                                        "Série dramatique",
                                        "Movie / Drama"
                                    ],
                                    "actors": [
                                        {
                                            "actor": "Gaia Girace",
                                            "role": "Lila Cerullo"
                                        },
                                        {
                                            "actor": "Margherita Mazzucco",
                                            "role": "Elena Greco"
                                        },
                                        {
                                            "actor": "Giovanni Amura",
                                            "role": "Stefano Carracci"
                                        },
                                        {
                                            "actor": "Valentina Acca",
                                            "role": "Nunzia Cerullo"
                                        },
                                        {
                                            "actor": "Giorgia Gargano",
                                            "role": "Nadia Galiani"
                                        },
                                        {
                                            "actor": "Lia Zinno",
                                            "role": "Giuseppina Peluso"
                                        },
                                        {
                                            "actor": "Antonio Milo",
                                            "role": "Silvio Solara"
                                        },
                                        {
                                            "actor": "Christian Giroso",
                                            "role": "Antonio Cappuccio"
                                        }
                                    ],
                                    "writers": [
                                        "Elena Ferrante",
                                        "Francesco Piccolo",
                                        "Laura Paolucci",
                                        "Saverio Costanzo"
                                    ],
                                    "composers": [],
                                    "countries": [
                                        "Italie"
                                    ]
                                }

    assert data['programmes'][1] == {
                                    "start": "20210127230500 +0100",
                                    "stop": "20210128005000 +0100",
                                    "channel": "1399.api.telerama.fr",
                                    "audio_subtitles": True,
                                    "sub-title": "A Dijon",
                                    "desc": "Au sommaire : Mystérieux incendie. Le 28 janvier 2010 les pompiers de Fontaine-lès-Dijon sont appelés pour un incendie. - Qui a tué la femme du maire ? Le 16 avril 2006, Marcelle est retrouvée assassinée. - La cavale du père de famille. Le 21 décembre 1996, à Dijon, un homme signale qu'un meurtre a sans doute été commis rue de la Prévôté.",
                                    "icon": "https://television.telerama.fr/sites/tr_master/files/sheet_media/media/9f2e217e14b228a19fd557bcfc44316e7df5ae84.jpg",
                                    "url": "https://television.telerama.fr/tele/magazine/crimes,12029897,emission76313169.php",
                                    "episode-num": "2..0/1",
                                    "public": 10,
                                    "titles": [
                                        "Crimes"
                                    ],
                                    "directors": [
                                        "Jean-Marc Morandini"
                                    ],
                                    "categories": [
                                        "Magazine",
                                        "Magazine de société",
                                        "Magazines / Reports / Documentary"
                                    ],
                                    "actors": [],
                                    "writers": [],
                                    "composers": [],
                                    "countries": [
                                        "français"
                                    ]
                                }

    assert data['programmes'][2] == {
                                    "start": "20210128235900 +0100",
                                    "stop": "20210129002200 +0100",
                                    "channel": "924.api.telerama.fr",
                                    "audio_subtitles": False,
                                    "sub-title": "Caniche contre gargouille",
                                    "desc": "Alors qu'il tourne une série TV bas de gamme dans un vieil immeuble gothique empli de gargouilles, le tournage et la carrière de Daniel Valentino sont fortement compromis suite à l'attaque d'une gargouille qui semble avoir pris vie. Toute son équipe de techniciens démissionne, aussitôt remplacée par Scooby et ses amis qui prennent l'enquête an main : qui en veut au réalisateur au point de ruiner son film ?...",
                                    "icon": "https://television.telerama.fr/sites/tr_master/files/sheet_media/media/42c7e9b018c03ea3fe00406f1f51ccd37593b911.jpg",
                                    "url": "https://television.telerama.fr/tele/dessin-anime/trop-cool-scooby-doo,17734304,saison1,episode4.php",
                                    "episode-num": "0.3.0/1",
                                    "public": 0,
                                    "titles": [
                                        "Trop cool, Scooby-Doo !",
                                        "Be Cool Scooby-Doo"
                                    ],
                                    "directors": [
                                        "Shaunt Nigoghossian"
                                    ],
                                    "categories": [
                                        "Jeunesse",
                                        "Dessin animé",
                                        "Children's / Youth programmes"
                                    ],
                                    "actors": [],
                                    "writers": [
                                        "Joe Ballarini",
                                        "Marly Halpern-Graser",
                                        "Joe Ruby",
                                        "Ken Spears"
                                    ],
                                    "composers": [],
                                    "countries": [
                                        "américain"
                                    ]
                                }