import streamlit as st
import plotly.express as px
from calculs2 import (
    calculer_imc,
    calculer_calories,
    generer_programme_sport,
    exporter_programme_sport_pdf,
    generer_plan_nutrition,
    exporter_plan_pdf,
    get_macros_info,
    prevision_poids
)
import base64

st.set_page_config(page_title='Coach Sportif', layout='wide')
st.title('Coach Sportif – Ton programme personnalisé')


# --------------------------------------------------
# 1) Saisie des informations
# --------------------------------------------------

st.sidebar.header('Tes informations')
age = st.sidebar.number_input('Âge', min_value=10, max_value=99, value=25)
poids = st.sidebar.number_input('Poids (kg)', min_value=40, max_value=150, value=70)
taille = st.sidebar.number_input('Taille (cm)', min_value=140, max_value=210, value=170)
sexe = st.sidebar.radio('Sexe', ('Homme', 'Femme'), horizontal=True)
objectif = st.sidebar.selectbox('Objectif', ('Perte de poids', 'Prise de masse', 'Remise en forme'))
niveau = st.sidebar.selectbox('Niveau sportif', ('Debutant', 'Intermediaire', 'Avance'))

st.sidebar.write('---')

if st.sidebar.button('Générer mon programme'):
    st.session_state['programme_genere'] = True

# --------------------------------------------------
# 2) Calcul et affichage de l'IMC
# --------------------------------------------------

if st.session_state.get('programme_genere', False):
    imc, interpretation = calculer_imc(poids, taille)
    st.header('1️⃣ Ton IMC')
    st.write(f'Ton IMC est **{imc}** → **{interpretation}**')
    st.markdown("""
    **L'IMC (Indice de Masse Corporelle)** permet d'évaluer la corpulence à partir du poids et de la taille.  
    - Moins de 18,5 : insuffisance pondérale  
    - Entre 18,5 et 25 : poids normal  
    - Entre 25 et 30 : surpoids  
    - Plus de 30 : obésité  
    """)

    # Calcul des besoins caloriques
    calories = calculer_calories(poids, taille, age, sexe, niveau, objectif)
    st.write(f'Apport calorique conseillé : **{calories} kcal / jour**')

    st.write('---')

    # --------------------------------------------------
    # 3) Programme d'entraînement
    # --------------------------------------------------
    st.header('2️⃣ Programme d\'entraînement sur 4 semaines')

    df_sport = generer_programme_sport(niveau, objectif)
    st.dataframe(df_sport, use_container_width=True)

    # Bouton de téléchargement PDF
    pdf_sport = exporter_programme_sport_pdf(df_sport)
    st.download_button(
        label='Télécharger le programme sportif (PDF)',
        data=pdf_sport,
        file_name='programme_sportif.pdf',
        mime='application/pdf'
    )

    st.write('---')

    # --------------------------------------------------
    # 4) Programme nutritionnel
    # --------------------------------------------------
    st.header('3️⃣ Plan nutritionnel sur 4 semaines')

    df_plan = generer_plan_nutrition(objectif, calories)
    st.dataframe(df_plan, use_container_width=True)

    pdf_plan = exporter_plan_pdf(df_plan)
    st.download_button(
        label='Télécharger le plan nutritionnel (PDF)',
        data=pdf_plan,
        file_name='plan_nutritionnel.pdf',
        mime='application/pdf'
    )

    st.write('---')

    # --------------------------------------------------
    # 5) Macros + Aliments associés
    # --------------------------------------------------
    st.header('4️⃣ Répartition des macronutriments')

    macros, aliments = get_macros_info(objectif)
    fig_pie = px.pie(
        names=list(macros.keys()),
        values=list(macros.values()),
        title=f'Répartition des nutriments pour ton objectif : {objectif}',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader('Aliments conseillés pour chaque catégorie')
    for macro, liste in aliments.items():
        st.markdown(f'**{macro} :** {", ".join(liste)}')

    st.write('---')

    # --------------------------------------------------
    # 6) Prévision du poids sur 4 semaines
    # --------------------------------------------------
    st.header('5️⃣ Prévision de ton poids sur 4 semaines')
    fig = prevision_poids(poids, objectif, niveau)
    st.pyplot(fig)

    st.success('✅ Ton programme complet est prêt ! Tu peux le télécharger ci-dessus.')
