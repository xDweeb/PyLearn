# 🐍 PyLearn Desktop

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.5+-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Une application desktop moderne pour apprendre Python de manière interactive**

[Fonctionnalités](#-fonctionnalités) •
[Installation](#-installation) •
[Utilisation](#-utilisation) •
[Architecture](#-architecture) •
[Contribuer](#-contributeurs)

</div>

---

## 📖 Aperçu

**PyLearn Desktop** est une application d'apprentissage de Python conçue pour les débutants et les apprenants intermédiaires. Elle offre une expérience d'apprentissage structurée avec des modules progressifs, des leçons interactives et différents types d'exercices pour renforcer les connaissances.

L'application suit une approche pédagogique progressive où chaque concept doit être maîtrisé avant de passer au suivant, garantissant ainsi une compréhension solide des fondamentaux de Python.

---

## ✨ Fonctionnalités

### 📚 Système de Modules et Leçons
- **Modules thématiques** : Python Start, Variables, Strings, et plus encore
- **Leçons structurées** : Chaque module contient plusieurs leçons progressives
- **Déblocage progressif** : Les contenus se débloquent au fur et à mesure de la progression

### 📝 Types de Tâches Variés
| Type | Description |
|------|-------------|
| 📖 **Théorie** | Contenu éducatif avec explications et exemples de code |
| ❓ **Quiz** | Questions à choix multiples pour tester la compréhension |
| ⌨️ **Typing** | Exercices de frappe de code pour mémoriser la syntaxe |
| 💻 **Exercise** | Exercices de programmation avec validation automatique |

### 📊 Suivi de Progression
- **Barres de progression** sur les modules, leçons et tâches
- **Statistiques globales** : Visualisez votre avancement total
- **Système de déblocage** : Complétez les tâches pour débloquer la suite

### 🎨 Interface Utilisateur Moderne
- Design épuré et intuitif avec PySide6
- Navigation fluide entre les vues
- Feedback visuel immédiat sur les actions

---

## 🛠️ Technologies Utilisées

| Technologie | Utilisation |
|-------------|-------------|
| **Python 3.10+** | Langage de programmation principal |
| **PySide6** | Framework GUI (Qt for Python) |
| **SQLite** | Base de données embarquée |
| **PyInstaller** | Packaging en exécutable Windows |

---

## 🏗️ Architecture

PyLearn Desktop suit une architecture **MVC (Model-View-Controller)** :

```
PyLearn/
├── main.py                 # Point d'entrée de l'application
├── navigation_manager.py   # Gestion de la navigation entre vues
│
├── gui/                    # 🖼️ VIEWS - Interface utilisateur
│   ├── home_view.py        # Écran d'accueil
│   ├── modules_view.py     # Liste des modules
│   ├── lessons_view.py     # Liste des leçons
│   ├── tasks_view.py       # Liste et contenu des tâches
│   ├── quiz_view.py        # Interface quiz
│   ├── typing_view.py      # Interface typing
│   ├── exercise_view.py    # Interface exercice
│   └── statistics_view.py  # Page statistiques
│
├── controllers/            # 🎮 CONTROLLERS - Logique métier
│   ├── module_controller.py
│   ├── lesson_controller.py
│   ├── task_controller.py
│   └── progression_manager.py
│
├── database/               # 💾 MODEL - Accès aux données
│   ├── db.py               # Connexion à la base de données
│   └── init_db.py          # Initialisation et schéma
│
├── assets/                 # 📁 Ressources
│   ├── styles/
│   │   └── style.qss       # Feuille de style Qt
│   ├── icons/              # Icônes de l'application
│   └── pylearn.db          # Base de données SQLite
│
├── utils/                  # 🔧 Utilitaires
│   └── resource_path.py    # Gestion des chemins (PyInstaller)
│
├── build.py                # Script de build
├── pylearn.spec            # Configuration PyInstaller
└── requirements.txt        # Dépendances Python
```

### Flux de données

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│    Views    │ ←→  │  Controllers │ ←→  │   Database   │
│  (PySide6)  │     │   (Logic)    │     │   (SQLite)   │
└─────────────┘     └──────────────┘     └──────────────┘
       ↑                                        ↑
       │         Navigation Manager             │
       └────────────────────────────────────────┘
```

---

## 📸 Captures d'écran

<div align="center">

### Écran d'accueil
![Home Screen](assets/screenshots/home.png)
*Page d'accueil avec progression globale et aperçu des modules*

### Liste des Modules
![Modules](assets/screenshots/modules.png)
*Vue des modules avec barres de progression*

### Interface de Tâches
![Tasks](assets/screenshots/tasks.png)
*Sidebar de navigation et contenu de la tâche*

### Quiz Interactif
![Quiz](assets/screenshots/quiz.png)
*Questions à choix multiples avec feedback*

### Statistiques
![Statistics](assets/screenshots/statistics.png)
*Vue d'ensemble de la progression*

</div>

> 📝 **Note** : Les captures d'écran seront ajoutées prochainement.

---

## 📥 Installation

### Prérequis

- **Python 3.10** ou supérieur
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel, pour cloner le dépôt)

### Étapes d'installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/xDweeb/PyLearn.git
   cd PyLearn
   ```

2. **Créer un environnement virtuel** (recommandé)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Vérifier l'installation**
   ```bash
   python -c "import PySide6; print('PySide6 OK')"
   ```

---

## 🚀 Utilisation

### Lancer l'application

```bash
python main.py
```

### Navigation dans l'application

1. **Écran d'accueil** : Cliquez sur "Commencer l'apprentissage" pour voir les modules
2. **Modules** : Sélectionnez un module débloqué pour voir ses leçons
3. **Leçons** : Choisissez une leçon pour accéder aux tâches
4. **Tâches** : Complétez les tâches dans l'ordre pour débloquer la suite
5. **Statistiques** : Consultez votre progression globale

### Raccourcis

| Action | Description |
|--------|-------------|
| Bouton "Retour" | Revenir à la vue précédente |
| "Continuer" | Reprendre là où vous en étiez |
| "Statistiques" | Voir votre progression |

---

## 📦 Packaging en EXE

### Méthode 1 : Script automatisé (recommandé)

```bash
python build.py
```

Le script va :
- Vérifier les dépendances
- Nettoyer les builds précédents
- Créer l'exécutable dans `dist/PyLearnDesktop.exe`

### Méthode 2 : PyInstaller manuel

```bash
# Installer PyInstaller si nécessaire
pip install pyinstaller

# Builder avec le fichier spec
pyinstaller --clean --noconfirm pylearn.spec
```

### Résultat

```
dist/
└── PyLearnDesktop.exe    # Exécutable standalone (~50-100 MB)
```

### Notes importantes

- L'exécutable est **autonome** (ne nécessite pas Python installé)
- La base de données utilisateur est créée dans `%APPDATA%\PyLearnDesktop\`
- Pour ajouter une icône, placez `pylearn.ico` dans `assets/icons/`

---

## 🧪 Tests

```bash
# Lancer les tests (à venir)
python -m pytest tests/
```

---

## 🤝 Contributeurs

<div align="center">

| Contributeur | Rôle |
|--------------|------|
| **Taibi El Yakouti** | Développeur Principal |
| **Fatima Zahra** | Développeuse |
| **Sylla** | Développeur |

</div>

---

## 📄 License

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2025 PyLearn Desktop Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Fait avec ❤️ pour l'apprentissage de Python**

[⬆ Retour en haut](#-pylearn-desktop)

</div>
