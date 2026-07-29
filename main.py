import logging
import inventaire
import argparse
import sys
parser = argparse.ArgumentParser(description="Contrôle de l'inventaire des machines")
parser.add_argument("--fichier",metavar="fichier" ,default="hotes.yaml", help="Chemin du fichier YAML d'inventaire")
parser.add_argument("--rapport",metavar="rapport", default="rapport.json", help="Chemin du rapport JSON de sortie")
parser.add_argument("--log",metavar="log", default="inventaire.log", help="Chemin du fichier de log")
parser.add_argument("--timeout",metavar="timeout", default=1, type=int, help="Timeout ping en secondes")

arguments = parser.parse_args()

nb_non_joignable =0
#configuration de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(arguments.log, mode="a",encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
#création de l'instance logging
logger = logging.getLogger(__name__)

info_yaml = inventaire.charger_hotes(arguments.fichier)  # chargement du fichier
if info_yaml is False:
    logger.error("Impossible de charger l'inventaire %s", arguments.fichier)
    sys.exit(1)

rapport = inventaire.controler_hotes(info_yaml, arguments.timeout)  # utilisation des données pour ping et construction du rapport
if rapport is False:
    logger.error("Le contrôle des hôtes a échoué. Vérifiez l'inventaire et réessayez.")
    sys.exit(1)

nb_non_joignable = 0
if inventaire.ecrire_rapport(rapport, arguments.rapport):
    nb_non_joignable = sum(1 for h in rapport if not h.get("joignable"))
    logger.info(
        "Le rapport a été créé avec %d hôtes (%d joignables, %d injoignables)",
        len(rapport),
        len(rapport) - nb_non_joignable,
        nb_non_joignable,
    )
else:
    logger.error("Une erreur est survenue à la création du rapport %s", arguments.rapport)
    sys.exit(1)

if nb_non_joignable > 0:
    sys.exit(2)

sys.exit(0)  