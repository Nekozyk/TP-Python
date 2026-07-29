"""- `test_ping_localhost_repond` : `ping("127.0.0.1") is True` ;
- `test_ping_adresse_documentation_ne_repond_pas` : `ping("192.0.2.1") is False` ;
- `test_ecrire_rapport` : avec une liste de résultats fabriquée à la main et
  le dossier temporaire `tmp_path` fourni par pytest, vérifiez `total`,
  `joignables`, `injoignables` dans le JSON écrit."""

import inventaire

def test_ping_localhost_repond():
    assert inventaire.ping("127.0.0.1") is True
    
def test_ping_adresse_documentation_ne_repond_pas():
     assert inventaire.ping("19.0.2.1") is False
     
def test_ecrire_rapport():
    
    rapport=[]
    liste ={"nom": "test" , "adresse": "192.168.0.1", "role": "local ", "joignable":True}
    rapport.append(liste)
    liste ={"nom": "test" , "adresse": "localhost", "role": "local ", "joignable":True}
    rapport.append(liste)
    liste ={"nom": "test" , "adresse": "8.8.8.8", "role": "local ", "joignable":False}
    rapport.append(liste)
    liste ={"nom": "test" , "adresse": "127.0.0.1", "role": "local ", "joignable":True}
    rapport.append(liste)
    assert inventaire.ecrire_rapport(rapport,"rapport_test.json") is True