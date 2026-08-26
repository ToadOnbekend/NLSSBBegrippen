import importlib.util
import os
import subprocess
import sys
from pathlib import Path

###
# Controleren of bestanden aanwezigzijn
###

stoppen = False

project_map = Path(__file__).resolve().parent
benodigde_bestanden = [
    "server.py",
    "database_maken.py",
    "databasemrg.py",
    "tussen_laag.py",

    "website/website_server.py",

    "website/templates/begripaanmaken.html",
    "website/templates/begrippagina.html",
    "website/templates/begrippenkader.html",
    "website/templates/begrippenkaderaanmaken.html",
    "website/templates/home.html",
    "website/templates/zoeken.html",

    "website/static/css/aanmaken.css",
    "website/static/css/begrip.css",
    "website/static/css/styles.css",
    "website/static/css/zoeken.css",

    "website/static/fonts/RobotoItalicVRF.ttf",
    "website/static/fonts/RobotoVRF.ttf",

    "website/static/js/scriptBegrip.js",
    "website/static/js/scriptBegripAanmaken.js",
    "website/static/js/scriptBegrippenkader.js",
    "website/static/js/scriptHome.js",
    "website/static/js/scriptKaderAanmaken.js",
    "website/static/js/scriptZoeken.js"
]

for bestand in benodigde_bestanden:
    pad_controleren = project_map / bestand

    if not pad_controleren.exists():
        print(f"[\033[31m!\033[0m] Bestand '{bestand}' niet gevonden")
        stoppen = True

if stoppen:
    print("Niet alle benodigde bestanden gevonden.")
    exit()

###
# TODO: Initialiseren? met config bestand.
###

###
# Controleren of modules aanwezig zijn
###

modules = ['flask', 'sqlalchemy', 'flask_cors', 'requests']

for module in modules:
    if importlib.util.find_spec(module) is None:
        print(f"Module '{module}' niet gevonden, installeren...")
        os.system(f"pip install {module}")


###
# Starten van servers
###

print("Starten...")

a1 = subprocess.Popen([sys.executable, "server.py"])
a2 = subprocess.Popen([sys.executable, "website/website_server.py"])

a1.wait()
a2.wait()

print("Klaar")
