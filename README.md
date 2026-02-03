# 📱 QR Code Generator

Utilitaire léger pour générer et sauvegarder des QR Codes instantanément.

## ✨ Fonctions
- **Auto-save** : Enregistrement direct dans `Téléchargements`.
- **Aperçu** : Visualisation immédiate du QR Code généré.
- **Naming** : Nommage automatique via l'URL.

## 🚀 Installation & Utilisation
- **Utilisateurs** : Téléchargez et lancez directement le fichier `.exe`.
- **Développeurs** : Clonez/Pullez le projet et lancez `main.py` (nécessite `qrcode` et `Pillow`).

## 📦 Build (.exe)
Pour re-compiler le projet avec son icône :
```bash
python -m PyInstaller --noconsole --onefile --windowed --icon=logo.ico --add-data "logo.ico;." generateurQRCode.py
