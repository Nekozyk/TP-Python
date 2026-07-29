import platform
import yaml
import sys
import subprocess
import json
import datetime

def charger_hotes(chemin) :
 #ouverture et lecture du yaml pour en extraire les informations et en retourner le contenu
    try:
      with open(chemin, encoding="utf-8", mode="r") as fichier:
        donnees = yaml.safe_load(fichier)
        for user in donnees["hotes"]:
            print(user["nom"])
      return donnees
   
    except FileNotFoundError:
      print("Le fichier "+chemin+" est introuvable "+sys.exit(1))
      return False
    except Exception as e:
            print(f"erreur dans charger hotes: {e}")
            return False  
        
def ping(adresse, timeout_s=1) :
    try:
                       
            if platform.system() == "Windows":
                cmd = ["ping", "-n", "1", adresse]
            else:
                cmd = ["ping", "-c", "1", adresse]
            
        # utilisation du subprocess avec le time out
            result = subprocess.run(cmd,capture_output=True,timeout=timeout_s + 1)    
        
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"Erreur dans ping: {e}")
        return False
    
    return result.returncode == 0

def controler_hotes(hotes, timeout_s=1):
    #pour tout élemets de hotes on créer un dictionnaire hote et l'on revoie un tableau de dictionnaire avec le champ joignable
    
    try:
        rapport = []
        for hote in hotes["hotes"]:
            if hote["adresse"] == "" or hote["adresse"] == None :
                print(f"Attenttion l'hote  {hote["nom"]} n'a pas d'adresse ip")
            else:
               is_joignable =  ping(hote["adresse"],timeout_s)
               rapport.append({"nom": hote["nom"] , "adresse": hote["adresse"], "role": hote["role"], "joignable":is_joignable})
        
        return rapport
    except Exception as e:
            print(f"Erreur dans controler_hotes: {e}")
            return False
        
def ecrire_rapport(resultats, chemin):
    try:
        total = len(resultats)
        joignables = sum(1 for hote in resultats if hote.get("joignable"))
        injoignables = total - joignables

        mon_js_file = {
            "genere_le": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "total": total,
            "joignables": joignables,
            "injoignables": injoignables,
            "hotes": resultats,
        }

        with open(chemin, encoding="utf-8", mode="w") as fichier:
            json.dump(mon_js_file, fichier, indent=2, ensure_ascii=False)
            return True

    except FileNotFoundError:
        print("Le fichier " + chemin + " est introuvable " + sys.exit(1))
        return False

    except Exception as e:
        print(f"erreur dans charger hotes: {e}")
        return False 
                