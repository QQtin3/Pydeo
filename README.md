# PyDEO
PyDEO est un petit éditeur vidéo écrit en Python avec une interface graphique (PySide6) et des utilitaires d'entrée/sortie basés sur MoviePy.

Ce dépôt contient une version modulaire et pédagogique d'un éditeur, avec :
- un visualiseur vidéo et des contrôles de lecture,
- un onglet "Sources" pour importer des fichiers multimédia,
- une vue de timeline (tracks vidéo / audio) basique,
- des contrôles d'édition (toolbar, undo/redo stub),
- un onglet "Effets" pour futurs traitements,
- un utilitaire d'export

## Dépendances
Les dépendances gérées dans `requirements.txt` sont :

- PySide6 (interface graphique)
- moviepy (lecture/écriture et manipulation des clips)
- numpy

Installez-les avec :

```powershell
python -m pip install -r requirements.txt
```

## Comment lancer
- Sur Windows (fichier inclus) : double-cliquer `launcher_windows.bat` ou lancer via PowerShell :

```powershell
python main.py
```

- Sur Linux/macOS :

```bash
./launch_linux.sh
# ou
python3 main.py
```

L'entrée principale est `main.py` qui initialise l'application PySide6 et ouvre la fenêtre principale `VideoEditor`.

## Fonctionnalités actuelles (implémentées)
- Import de vidéos (via l'onglet Sources) — prise en charge des formats courants (.mp4, .avi, .mkv, .mov, .flv, .wmv, .webm).
- Lecture / pause et navigation temporelle (preview + contrôles de transport).
- Timeline à pistes multiples (exemples de pistes vidéo et audio fournis).
- Ajout d'éléments dans la liste des sources et affichage de leur durée.
- Onglet Effets basique (interface prévue, intégration minimale avec TimelineController).
- Helpers pour la lecture/écriture de fichiers dans `controller/FileHandlerController.py` (utilise MoviePy).

Remarque importante : la commande d'export déclenchée depuis l'interface (`VideoEditor.exportVideo`) effectue actuellement une simulation d'export (affiche un message et un progrès simulé). Il existe néanmoins une fonction utilitaire `exportVideo` dans `controller/FileHandlerController.py` qui appelle `write_videofile` de MoviePy — cette fonction contient aujourd'hui des validations rudimentaires et peut nécessiter des corrections avant usage en production.

## Structure principale du projet
- `main.py` — point d'entrée de l'application.
- `views/` — interfaces PySide6 (fenêtre principale, widgets, onglets, timeline widget).
- `controller/` — gestion des opérations (lecture de fichiers, timeline controller, preview controller, file handler).
- `model/` — modèles métier (Source, Timeline, TimelineClip, Effects, etc.).

