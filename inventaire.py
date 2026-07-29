import logging
from pathlib import Path
import platform
import yaml
import subprocess
import json
import datetime
import argparse
logger = logging.getLogger(__name__)

def charger_hotes(chemin) :
 #ouverture et lecture du yaml pour en extraire les informations et en retourner le contenu
    try:
      with open(chemin, encoding="utf-8", mode="r") as fichier:
        donnees = yaml.safe_load(fichier)
        for user in donnees["hotes"]:
            logger.info("hôte lu : %s", user["nom"])
      return donnees
   #en cas d'erreur retourner faux
    except FileNotFoundError:
      logger.error("Le fichier %s est introuvable", chemin)
      return False
    except Exception as e:
            logger.error("Erreur dans charger_hotes : %s", e)
            return False  
        
def ping(adresse, timeout_s=1) :
    try:
                       
            if platform.system() == "Windows":
                cmd = ["ping", "-n", "1", adresse]
            else:
                cmd = ["ping", "-c", "1", adresse]
            
        # utilisation du subprocess avec le time out
            result = subprocess.run(cmd,capture_output=True,timeout=timeout_s + 1)    
    #en cas d'erreur retourner faux    
    except subprocess.TimeoutExpired:
        logger.warning("Ping timeout pour %s", adresse)
        return False
    except Exception as e:
        logger.error("Erreur dans ping: %s", e)
        return False
    #Si pas d'erreur on retourne le booléen du test
    return result.returncode == 0

def controler_hotes(hotes, timeout_s=1):
    #pour tout élemets de hotes on créer un dictionnaire hote et l'on revoie un tableau de dictionnaire avec le champ joignable
    
    try:
        rapport = []
        for hote in hotes["hotes"]:
            if not hote.get("adresse"):
                logger.warning("Attention l'hôte %s n'a pas d'adresse ip", hote.get("nom", "<inconnu>"))
            else:
               is_joignable =  ping(hote["adresse"],timeout_s)
               rapport.append({"nom": hote["nom"] , "adresse": hote["adresse"], "role": hote["role"], "joignable":is_joignable})
        
        return rapport
    except Exception as e:
            logger.error("Erreur dans controler_hotes: %s", e)
            return False
        
def ecrire_rapport(resultats, chemin):
    try:
        donnees_exploitables =[]
        if Path(chemin).exists():
            with open(chemin, encoding="utf-8", mode="r") as fichier:
             donnees_exploitables = json.load(fichier) # Pour exploiter les données dans un format compréhensible pour le Python, on va le charger avec .load()

        total = len(resultats)
        joignables = sum(1 for hote in resultats if hote.get("joignable"))
        injoignables = total - joignables
        #création de la variable qui remplira le json
        mon_js_file = {
            "genere_le": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "total": total,
            "joignables": joignables,
            "injoignables": injoignables,
            "hotes": resultats,
        }
        
        donnees_exploitables.append(mon_js_file)
        
        with open(chemin, encoding="utf-8", mode="w") as fichier:
            json.dump(donnees_exploitables, fichier, indent=2, ensure_ascii=False)
            return True

    except FileNotFoundError:
        logger.error("Le fichier %s est introuvable", chemin)
        return False

    except Exception as e:
        logger.error("Erreur dans ecrire_rapport: %s", e)
        return False 
                