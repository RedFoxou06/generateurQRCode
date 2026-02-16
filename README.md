# 📱 QR Code Generator

Utilitaire léger pour générer et sauvegarder des QR Codes instantanément — disponible en version **Desktop (.exe)** et désormais en **APK Android**.

---

## ✨ Fonctions

- **Auto-save** : Enregistrement direct dans `Téléchargements` avec nommage automatique via l'URL.
- **Aperçu** : Visualisation immédiate du QR Code généré.
- **Portabilité** : Exécutable `.exe` autonome — aucune installation requise.
- **📲 Version Android** : APK disponible — même logique, même rapidité, directement depuis ton téléphone.

---

## 🖥️ Version Desktop

### Installation & Utilisation

- **Utilisateurs** : Téléchargez et lancez directement le fichier `.exe`.
- **Développeurs** : Clonez le projet et lancez `main.py`.

```bash
# Dépendances
pip install qrcode Pillow
```

```bash
# Lancement
python main.py
```

### 📦 Build (.exe)

Pour recompiler le projet avec son icône :

```bash
python -m PyInstaller --noconsole --onefile --windowed --icon=logo.ico --add-data "logo.ico;." generateurQRCode.py
```

---

## 📲 Version Android (APK)

L'APK reprend exactement les mêmes fonctionnalités que la version desktop, natif sur Android — aucune installation via store, téléchargement direct du `.apk`.

> Télécharger l'APK

---

## 🛠️ Stack

| Version | Technologies                            |
|---------|-----------------------------------------|
| Desktop | Python, `qrcode`, `Pillow`, PyInstaller |
| Android | Ionic, Angular                          |

---

## 📄 Licence

Projet personnel — utilisation libre à des fins éducatives.