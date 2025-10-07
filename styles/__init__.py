"""
Chargeur de styles pour Pydeo
"""


import os


def get_styles():
    """Charge et retourne le fichier QSS principal"""
    styles_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(styles_dir, 'main.qss')
    
    try:
        with open(qss_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Fichier de styles non trouvé: {qss_path}")
        return ""
    except Exception as e:
        print(f"Erreur lors du chargement des styles: {e}")
        return ""


