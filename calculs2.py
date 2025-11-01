import numpy as np
import pandas as pd
import random
import io
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# --------------------------------------------------
# 1) IMC et Calories
# --------------------------------------------------

def calculer_imc(poids, taille_cm):
    taille_m = taille_cm / 100
    imc = round(poids / (taille_m ** 2), 1)
    if imc < 18.5:
        interpretation = 'Maigreur'
    elif imc < 25:
        interpretation = 'Poids normal'
    elif imc < 30:
        interpretation = 'Surpoids'
    else:
        interpretation = 'Obésité'
    return imc, interpretation


def calculer_calories(poids, taille_cm, age, sexe, niveau_sport, objectif):
    if sexe == 'Homme':
        bmr = (10 * poids) + (6.25 * taille_cm) - (5 * age) + 5
    else:
        bmr = (10 * poids) + (6.25 * taille_cm) - (5 * age) - 161

    # Doit correspondre aux valeurs envoyées par interface2.py
    facteur = {'Debutant': 1.2, 'Intermediaire': 1.4, 'Avance': 1.6}.get(niveau_sport, 1.3)
    tdee = bmr * facteur

    if objectif == 'Perte de poids':
        tdee *= 0.85
    elif objectif == 'Prise de masse':
        tdee *= 1.15

    return round(tdee)


# --------------------------------------------------
# 2) Programme Sportif sur 4 semaines (+ PDF)
# --------------------------------------------------

def generer_programme_sport(niveau, objectif):
    exercices = {
        'Haut du corps': [
            'Pompes', 'Tractions', 'Développé couché', 'Rowing haltères',
            'Développé militaire', 'Élévations latérales', 'Dips'
        ],
        'Bas du corps': [
            'Squats', 'Fentes', 'Soulevé de terre', 'Hip thrust',
            'Mollets debout', 'Leg press', 'Step-ups'
        ],
        'Cardio': [
            'Course à pied', 'Corde à sauter', 'Vélo', 'Rameur',
            'Marche rapide', 'Burpees', 'Montées de genoux'
        ],
        'Abdos': [
            'Gainage', 'Crunchs', 'Relevés de jambes', 'Planche latérale',
            'Russian twist', 'Mountain climbers'
        ],
        'Mobility/Stretch': [
            'Étirements complets', 'Yoga doux', 'Mobilité hanches',
            'Mobilité épaules', 'Respiration diaphragmatique'
        ],
        'Full body': [
            'Kettlebell swing', 'Thrusters', 'Burpees', 'Jumping jacks',
            'Bear crawl', 'Squat + pompe'
        ]
    }

    if niveau == 'Debutant':
        jours_actifs = 3
        series = 2
        reps = '10-12'
        repos = '90 sec'
        duree_base = 30
    elif niveau == 'Intermediaire':
        jours_actifs = 4
        series = 3
        reps = '10-15'
        repos = '75 sec'
        duree_base = 40
    else:  # Avance
        jours_actifs = 5
        series = 4
        reps = '12-15'
        repos = '60 sec'
        duree_base = 50

    if objectif == 'Perte de poids':
        focus = ['Full body', 'Cardio', 'Abdos', 'Mobility/Stretch', 'Bas du corps']
    elif objectif == 'Prise de masse':
        focus = ['Haut du corps', 'Bas du corps', 'Abdos', 'Full body', 'Mobility/Stretch']
    else:
        focus = ['Full body', 'Cardio', 'Bas du corps', 'Haut du corps', 'Mobility/Stretch']

    objectifs_hebdo = [
        'Semaine 1 : Stabiliser la technique et la régularité',
        'Semaine 2 : Augmenter légèrement le volume',
        'Semaine 3 : Progresser sur l’intensité',
        'Semaine 4 : Consolider et récupérer activement'
    ]

    lignes = []
    for semaine in range(1, 5):
        objectif_semaine = objectifs_hebdo[semaine - 1]
        jour = 1
        # jours actifs
        for j in range(jours_actifs):
            categorie = focus[(semaine + j) % len(focus)]
            exos = ', '.join(random.sample(exercices[categorie], k=min(2, len(exercices[categorie]))))
            duree = min(duree_base + 3 * semaine, 65)
            lignes.append({
                'Semaine': f'Semaine {semaine}',
                'Jour': f'Jour {jour}',
                'Type': categorie,
                'Exercices': exos,
                'Séries': series,
                'Répétitions': reps,
                'Repos': repos,
                'Durée (min)': duree,
                'Objectif de la semaine': objectif_semaine
            })
            jour += 1
        # repos actif
        while jour <= 7:
            lignes.append({
                'Semaine': f'Semaine {semaine}',
                'Jour': f'Jour {jour}',
                'Type': 'Repos actif',
                'Exercices': random.choice(exercices['Mobility/Stretch']),
                'Séries': '-',
                'Répétitions': '-',
                'Repos': '-',
                'Durée (min)': 15,
                'Objectif de la semaine': objectif_semaine
            })
            jour += 1

    return pd.DataFrame(lignes)


def exporter_programme_sport_pdf(df_sport):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph('Programme d\'entraînement – 4 semaines', styles['Title']), Spacer(1, 12)]

    for s in range(1, 5):
        story.append(Paragraph(f'Semaine {s}', styles['Heading2']))
        data = df_sport[df_sport['Semaine'] == f'Semaine {s}'][[
            'Jour', 'Type', 'Exercices', 'Séries', 'Répétitions', 'Repos', 'Durée (min)'
        ]]
        table_data = [list(data.columns)] + data.values.tolist()
        t = Table(table_data, colWidths=[50, 90, 190, 40, 60, 40, 60])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black)
        ]))
        story.append(t)
        if s < 4:
            story.append(PageBreak())

    pdf.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# --------------------------------------------------
# 3) Plan Nutritionnel sur 4 semaines (+ PDF)
# --------------------------------------------------

def generer_plan_nutrition(objectif, calories):
    base = {
        'Petit-déjeuner': {
            'Perte de poids': [
                ('Flocons d\'avoine + yaourt + fruits rouges', '50 g avoine, 150 g yaourt, 100 g fruits'),
                ('Omelette + pain complet', '2 oeufs, 1 tranche pain complet'),
                ('Smoothie protéiné + amandes', '250 ml smoothie, 15 g amandes')
            ],
            'Prise de masse': [
                ('Pancakes + beurre de cacahuète + banane', '2 pancakes, 1 càs beurre cacahuète, 1 banane'),
                ('Omelette + avoine au lait', '3 oeufs, 40 g avoine, 200 ml lait'),
                ('Porridge lait + fruits + noix', '60 g avoine, 250 ml lait, 15 g noix')
            ],
            'Remise en forme': [
                ('Muesli + lait + fruits', '40 g muesli, 200 ml lait, 100 g fruits'),
                ('Yaourt + granola + poire', '200 g yaourt, 30 g granola, 1 poire'),
                ('Toast avocat + oeuf', '1/2 avocat, 1 oeuf, 1-2 toasts complets')
            ],
        },
        'Déjeuner': {
            'Perte de poids': [
                ('Poulet + légumes vapeur + quinoa', '120 g poulet, 200 g légumes, 60 g quinoa'),
                ('Poisson blanc + riz + brocoli', '150 g poisson, 70 g riz, 150 g brocoli'),
                ('Dinde + patate douce + salade', '120 g dinde, 150 g patate douce, salade')
            ],
            'Prise de masse': [
                ('Boeuf + pâtes + légumes', '150 g boeuf, 90 g pâtes, 150 g légumes'),
                ('Saumon + riz complet + haricots verts', '150 g saumon, 90 g riz, 150 g HV'),
                ('Poulet + pommes de terre + salade', '150 g poulet, 250 g PDT, salade')
            ],
            'Remise en forme': [
                ('Dinde + riz + ratatouille', '120 g dinde, 80 g riz, 200 g ratatouille'),
                ('Cabillaud + quinoa + épinards', '150 g cabillaud, 70 g quinoa, 150 g épinards'),
                ('Wrap poulet + crudités', '1 wrap, 100 g poulet, crudités, sauce yaourt')
            ],
        },
        'Collation': {
            'Perte de poids': [
                ('Fromage blanc + fruits', '150-200 g fromage blanc, 100 g fruits'),
                ('Pomme + amandes', '1 pomme, 15 g amandes')
            ],
            'Prise de masse': [
                ('Shake protéiné + banane', '1 dose whey, 300 ml lait, 1 banane'),
                ('Pain complet + beurre cacahuète', '2 tranches, 1 càs beurre cacahuète')
            ],
            'Remise en forme': [
                ('Yaourt + fruits', '1 pot, 100 g fruits'),
                ('Oeuf dur + tomate', '1-2 oeufs, 1 tomate')
            ],
        },
        'Dîner': {
            'Perte de poids': [
                ('Omelette + salade + pain complet', '2 oeufs, salade, 1 tranche pain'),
                ('Poisson + légumes + quinoa', '140 g poisson, 200 g légumes, 60 g quinoa')
            ],
            'Prise de masse': [
                ('Poulet + riz + légumes', '150 g poulet, 90 g riz, 200 g légumes'),
                ('Boeuf + pâtes + sauce tomate', '150 g boeuf, 90 g pâtes, sauce maison')
            ],
            'Remise en forme': [
                ('Dinde + légumes rôtis + quinoa', '120 g dinde, 200 g légumes, 70 g quinoa'),
                ('Poisson + riz + salade', '140 g poisson, 80 g riz, salade')
            ],
        },
    }

    repartition = {'Petit-déjeuner': 0.25, 'Déjeuner': 0.35, 'Collation': 0.15, 'Dîner': 0.25}

    lignes = []
    dernier_choix = {repas: None for repas in base.keys()}

    for semaine in range(1, 5):
        for jour in range(1, 8):
            for repas, ratio in repartition.items():
                kcal = round(calories * ratio)
                choix_possibles = base[repas][objectif][:]
                if dernier_choix[repas] and len(choix_possibles) > 1:
                    choix_possibles = [c for c in choix_possibles if c[0] != dernier_choix[repas][0]]
                proposition, portions = random.choice(choix_possibles)
                dernier_choix[repas] = (proposition, portions)

                lignes.append({
                    'Semaine': f'Semaine {semaine}',
                    'Jour': f'Jour {jour}',
                    'Repas': repas,
                    'Proposition': proposition,
                    'Portions suggérées': portions,
                    'Calories estimées': kcal
                })

    return pd.DataFrame(lignes)


def exporter_plan_pdf(df_plan):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph('Plan nutritionnel – 4 semaines', styles['Title']), Spacer(1, 12)]

    for s in range(1, 5):
        story.append(Paragraph(f'Semaine {s}', styles['Heading2']))
        sem_df = df_plan[df_plan['Semaine'] == f'Semaine {s}']
        for j in range(1, 8):
            story.append(Paragraph(f'Jour {j}', styles['Heading3']))
            data = sem_df[sem_df['Jour'] == f'Jour {j}'][['Repas', 'Proposition', 'Portions suggérées', 'Calories estimées']]
            table_data = [list(data.columns)] + data.values.tolist()
            t = Table(table_data, colWidths=[90, 200, 110, 70])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
        if s < 4:
            story.append(PageBreak())

    pdf.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# --------------------------------------------------
# 4) Macros et Aliments associés
# --------------------------------------------------

def get_macros_info(objectif):
    if objectif == 'Perte de poids':
        macros = {'Protéines': 0.35, 'Glucides': 0.30, 'Lipides': 0.25, 'Fibres': 0.10}
        aliments = {
            'Protéines': ['Poulet', 'Poisson blanc', 'Tofu', 'Oeufs', 'Yaourt nature', 'Lentilles'],
            'Glucides': ['Quinoa', 'Riz complet', 'Patate douce', 'Flocons d\'avoine', 'Pomme'],
            'Lipides': ['Avocat', 'Noix', 'Huile d\'olive', 'Saumon', 'Graines de chia'],
            'Fibres': ['Légumes verts', 'Fruits rouges', 'Haricots', 'Avoine']
        }

    elif objectif == 'Prise de masse':
        macros = {'Protéines': 0.30, 'Glucides': 0.50, 'Lipides': 0.15, 'Micronutriments': 0.05}
        aliments = {
            'Protéines': ['Poulet', 'Saumon', 'Oeufs entiers', 'Lentilles', 'Fromage blanc'],
            'Glucides': ['Riz basmati', 'Pâtes complètes', 'Pain complet', 'Flocons d\'avoine', 'Fruits secs'],
            'Lipides': ['Huile d\'olive', 'Beurre de cacahuète', 'Noix de cajou', 'Avocat'],
            'Micronutriments': ['Banane', 'Brocoli', 'Poivron rouge', 'Amandes', 'Épinards']
        }

    else:
        macros = {'Protéines': 0.30, 'Glucides': 0.40, 'Lipides': 0.20, 'Hydratation': 0.10}
        aliments = {
            'Protéines': ['Poisson', 'Oeufs', 'Légumineuses', 'Fromage blanc'],
            'Glucides': ['Pain complet', 'Pâtes', 'Fruits', 'Céréales'],
            'Lipides': ['Huile d\'olive', 'Amandes', 'Avocat', 'Saumon'],
            'Hydratation': ['Eau', 'Thé vert', 'Smoothie maison', 'Infusion']
        }

    return dict(macros), dict(aliments)


# --------------------------------------------------
# 5) Prévision du poids sur 4 semaines
# --------------------------------------------------

def prevision_poids(poids, objectif, niveau_selectionne):
    semaines = np.arange(1, 5)

    if objectif == 'Perte de poids':
        base = -0.45
    elif objectif == 'Prise de masse':
        base = 0.35
    else:
        base = 0.0

    # Doit correspondre aux valeurs envoyées par interface2.py
    mults = {'Debutant': 0.75, 'Intermediaire': 1.00, 'Avance': 1.35}
    fig, ax = plt.subplots(figsize=(7, 4))

    for niv, m in mults.items():
        p = poids
        courbe = []
        for _ in semaines:
            p += base * m
            courbe.append(round(p, 2))

        style = '-' if niv == niveau_selectionne else '--'
        width = 2.8 if niv == niveau_selectionne else 1.6
        alpha = 1.0 if niv == niveau_selectionne else 0.7
        ax.plot(semaines, courbe, style,
                linewidth=width, alpha=alpha, label=niv, marker='o')

    ax.set_title('Évolution prévisionnelle du poids sur 4 semaines')
    ax.set_xlabel('Semaines')
    ax.set_ylabel('Poids (kg)')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(title='Niveau sportif')
    ax.set_facecolor('#F7F7F7')

    return fig
