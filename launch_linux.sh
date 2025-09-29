#!/bin/bash
# Configuration de l'environnement
VENV_DIR="venv"
PYTHON_EXEC="python3"  # Configurable selon vos besoins

# Création de l'environnement virtuel (réutilisable)
if [ ! -d "$VENV_DIR" ]; then
    echo "🔹 Création de l'environnement virtuel..."
    "$PYTHON_EXEC" -m venv "$VENV_DIR"
    
    # Installation des dépendances
    if [ -f requirements.txt ]; then
        echo "📦 Installation des dépendances depuis requirements.txt..."
        "$VENV_DIR/bin/pip" install -r requirements.txt
    else
        echo "⚠️  Aucun requirements.txt trouvé. Installation de PySide6 par défaut..."
        "$VENV_DIR/bin/pip" install PySide6
    fi
fi

# Détermination dynamique des chemins (indépendant de la version Python)
SITE_PACKAGES="$("$VENV_DIR/bin/python" -c \
    "from sysconfig import get_paths; print(get_paths()['purelib'])")"

# Configuration Qt spécifique
QT_PLUGINS_DIR="$SITE_PACKAGES/PySide6/Qt/plugins"
QT_LIB_DIR="$SITE_PACKAGES/PySide6/Qt/lib"

# Vérification de l'existence des chemins Qt
if [ ! -d "$QT_PLUGINS_DIR" ]; then
    echo "❌ Erreur : Répertoire des plugins Qt non trouvé ($QT_PLUGINS_DIR)" >&2
    echo "Assurez-vous que PySide6 est correctement installé." >&2
    exit 1
fi

# Configuration des variables d'environnement
export QT_DEBUG_PLUGINS=1
export QT_PLUGIN_PATH="$QT_PLUGINS_DIR"
export LD_LIBRARY_PATH="$QT_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

# Affichage des informations de débogage
echo -e "\n⚙️  Configuration de l'environnement :"
echo "   QT_PLUGIN_PATH = $QT_PLUGIN_PATH"
echo "   LD_LIBRARY_PATH = $LD_LIBRARY_PATH"
echo "   Python utilisé : $("$VENV_DIR/bin/python" --version 2>&1)"

# Exécution de l'application
echo -e "\n🚀 Démarrage de l'application..."
exec "$VENV_DIR/bin/python" main.py # A remplacer par main
"""
python -m venv venv
source venv/bin/activate

export QT_DEBUG_PLUGINS=1
export QT_PLUGIN_PATH=$VIRTUAL_ENV/lib/python3.13/site-packages/PySide6/Qt/plugins
export LD_LIBRARY_PATH=$VIRTUAL_ENV/lib/python3.13/site-packages/PySide6/Qt/lib:$LD_LIBRARY_PATH

python main.py
desactivate
"""
