# 🏋️‍♂️ Digital Personal Trainer : Coach Sportif Virtuel

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![ReportLab](https://img.shields.io/badge/PDF_Engine-ReportLab-000000?style=for-the-badge)

> **Projet Application Web & Algorithmique**


---

## 📋 Ce que fait le projet

Ce projet est une application web interactive qui agit comme un **coach sportif intelligent**. Elle permet à un utilisateur de générer instantanément un programme complet (Sport & Nutrition) sur 4 semaines, adapté à sa morphologie et ses objectifs.

Concrètement, l'application réalise les tâches suivantes :

1.  **Analyse Métabolique :** Elle calcule l'IMC, le Métabolisme de Base (BMR) et la Dépense Énergétique Journalière (TDEE) en fonction de l'âge, du poids, de la taille et du niveau d'activité.
2.  **Génération de Programme Sportif :** Elle crée un planning d'entraînement jour par jour sur 4 semaines. L'intensité et le nombre de séances s'adaptent automatiquement au niveau de l'utilisateur (Débutant, Intermédiaire, Avancé).
3.  **Planification Nutritionnelle :** Elle calcule les besoins en macronutriments (Protéines, Glucides, Lipides) selon l'objectif (Sèche, Prise de masse) et génère des menus types.
4.  **Visualisation Prédictive :** Elle projette l'évolution théorique du poids de l'utilisateur sur le mois à venir sous forme de graphique interactif.
5.  **Export PDF Dynamique :** Elle permet de télécharger le programme complet sous forme d'un fichier PDF propre et mis en page, généré directement par le code (pas de simple capture d'écran).

---

## 📂 Architecture : Qui fait quoi ?

Le code est séparé en deux fichiers principaux pour distinguer le calcul (Backend) de l'affichage (Frontend).

### 1. `interface2.py` (L'Interface Utilisateur)
C'est le fichier que l'on exécute pour lancer l'application. Il gère toute la partie visuelle avec **Streamlit**.
* **Formulaires :** Récupère les données utilisateur (Sliders pour le poids/taille, menus déroulants pour les objectifs).
* **Visualisation :** Affiche les graphiques :
    * Diagrammes circulaires (`Plotly`) pour la répartition des macros.
    * Courbes (`Matplotlib`) pour la prévision de perte/gain de poids.
* **Orchestration :** C'est lui qui "appelle" les fonctions de calcul et gère le bouton de téléchargement du PDF.

### 2. `calculs2.py` (Le Moteur de Calcul)
C'est le cerveau de l'application. Il ne contient aucune interface graphique.
* **Logique Mathématique :** Contient les formules physiologiques (Mifflin-St Jeor) pour calculer les calories et l'IMC.
* **Génération de Données :** Construit les tableaux de données (`Pandas Dataframes`) pour le planning sportif et nutritionnel en fonction des règles métiers (ex: Si "Prise de masse" -> Augmenter les protéines).
* **Moteur PDF :** Utilise la librairie `ReportLab` pour dessiner le fichier PDF final (tableaux, styles, couleurs) octet par octet.

---

## 🛠️ Stack Technique

* **Langage :** Python 3.9
* **Interface Web :** `Streamlit`
* **Manipulation de Données :** `Pandas`, `NumPy`
* **Génération PDF :** `ReportLab` (Platypus engine)
* **Graphiques :** `Plotly Express`, `Matplotlib`

---

## 🏗 Architecture Logicielle & Rôle des Fichiers

Le projet est structuré autour de deux noyaux distincts pour séparer le traitement des données de l'affichage.

```mermaid
graph LR
A[User Interface Streamlit] -->|Input Data| B(interface2.py)
B -->|Appel Fonctions| C{calculs2.py}
C -->|Calculs BMR & Plans| D[Dataframes Pandas]
C -->|Génération Binaire| E[PDF Engine]
D -->|Visualisation| F[Graphiques Plotly/Matplotlib]
E -->|Download| B
