# 🏋️‍♂️ Digital Personal Trainer : Generative Coaching Engine

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![ReportLab](https://img.shields.io/badge/PDF_Engine-ReportLab-000000?style=for-the-badge)
![Plotly](https://img.shields.io/badge/Viz-Plotly_Interactive-3F4F75?style=for-the-badge)

> **Projet Application Web & Algorithmique**
> **Auteurs :** Tom Le Corre & Rishikaran Karunakaran

---

## 🚀 Vision du Projet & Complexité Technique

Ce projet dépasse le cadre d'une simple application de suivi sportif. Il s'agit d'un **Moteur Génératif** complet capable de construire, en temps réel, des programmes d'entraînement et de nutrition sur-mesure sur une période de 4 semaines.

L'objectif technique était de simuler l'intelligence d'un coach sportif à travers des algorithmes décisionnels basés sur des métriques physiologiques.

### 🔥 Les Défis Techniques Relevés
1.  **Architecture Modulaire (MVC-like) :** Nous avons implémenté une séparation stricte entre la logique métier (Backend) et l'interface utilisateur (Frontend) pour garantir la robustesse et la maintenabilité du code.
2.  **Moteur de Génération PDF (ReportLab) :** Le défi majeur a été de développer un pipeline d'export complexe. L'application ne se contente pas d'afficher des données ; elle **dessine programmatiquement** des fichiers binaires PDF (avec tableaux stylisés et mise en page dynamique) prêts à l'impression.
3.  **Algorithmique Métabolique :** Implémentation de formules physiologiques (BMR, TDEE) ajustées dynamiquement selon l'objectif (Sèche, Prise de masse) et le niveau sportif.
4.  **Projections Prédictives :** Modélisation mathématique de l'évolution du poids sur 4 semaines en fonction du déficit/surplus calorique calculé.

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
📂 1. Le Backend Logique : calculs2.py
C'est le "cerveau" de l'application. Ce fichier ne contient aucune interface graphique, uniquement des fonctions pures.

Calculs Physiologiques : Contient les fonctions calculer_imc et calculer_calories (Formule de Mifflin-St Jeor) pour déterminer le métabolisme de base et les besoins journaliers.

Générateurs de Plans : Algorithmes (generer_programme_sport, generer_plan_nutrition) qui construisent des Dataframes Pandas jour par jour en faisant varier l'intensité et les macros selon le profil utilisateur (Débutant/Avancé).

PDF Factory : Utilisation avancée de la librairie reportlab. Le code génère les fichiers PDF octet par octet (BytesIO), intégrant des tableaux complexes (TableStyle) et des mises en page structurées pour l'export.

📂 2. Le Frontend Interactif : interface2.py
C'est la couche de présentation gérée par Streamlit.

Collecte de Données : Formulaires dynamiques (Sliders, Selectbox) pour récupérer l'âge, le poids, le niveau, etc.

Orchestration : Appelle les fonctions du backend et transforme les données brutes en visualisations interactives.

Dataviz :

Plotly Express pour les diagrammes circulaires (Répartition Macros : Protéines/Glucides/Lipides).

Matplotlib pour tracer les courbes de projection de perte/gain de poids sur le mois à venir (prevision_poids).

📊 Fonctionnalités Clés
🔹 Planification Intelligente (4 Semaines)
L'algorithme génère un tableau complet jour par jour. Le volume d'entraînement est ajusté automatiquement (Ex: 3 séances/semaine pour un débutant vs 5 pour un expert).

🔹 Moteur Nutritionnel & Macros
Calcul automatique des macronutriments et suggestion d'aliments spécifiques. L'algorithme adapte les ratios selon l'objectif (Ex: Augmentation des protéines pour une prise de masse).

🔹 Export PDF Professionnel
L'utilisateur peut télécharger son programme. Ce n'est pas une simple capture d'écran, mais un document PDF natif généré par le code, incluant le branding et les tableaux formatés.

🛠️ Stack Technique & Algorithmes (SEO)
📚 Bibliothèques Principales
Frontend : streamlit (Interface réactive et déploiement).

Data Processing : pandas (Structure des plans hebdomadaires), numpy (Calculs de projection vectorielle).

Document Engineering : reportlab (Génération programmatique de PDF, gestion des Canvas et Platypus).

Visualisation : plotly (Graphiques interactifs), matplotlib (Courbes de tendance statiques).

🧮 Concepts Clés
Programmation Fonctionnelle : Code découpé en fonctions réutilisables.

Data Visualization : Représentation graphique des projections.

File Handling : Gestion des flux de données binaires (io.BytesIO) pour le téléchargement de fichiers générés en mémoire sans stockage disque.
