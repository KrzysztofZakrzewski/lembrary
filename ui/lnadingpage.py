# ================
# IMPORTS
# ================
import streamlit as st
import os
# import base64

# ================
# INER IMPORTS
# ================
from ui.media import render_loop_video
from src.translation_ai import translate_text

# ================
# PATHS
# ================
video_path = "assets/main/1966_rakieta-778x1024-1©_by_Tomasz_Lem_movie.mp4"
image_path = "assets/main/1966_rakieta-778x1024-1©_by_Tomasz_Lem.jpg"

# ================
# WEB TEXT
# ================
intro_text = 'LemLibrary to projekt stworzony z pasji do twórczości Stanisława Lema. Jako fan jego książek, stworzyłem interaktywną „lemotekę”, która przy pomocy embeddingów i wyszukiwania semantycznego pomaga odkrywać dzieła Lema na podstawie tematów, pytań i zainteresowań użytkownika. ' \
'W bibliotece jest 20 tytółów, ale myslę że zaintresowani znajdą coś dla siebie.'

lem_bio = '''(1921–2006) był jednym z najwybitniejszych pisarzy science fiction XX wieku, eseistą, futurologiem i filozofem. Urodził się we Lwowie, a po II wojnie światowej związał swoje życie z Krakowem. Jego twórczość łączyła naukową wyobraźnię, przenikliwą satyrę oraz głęboką refleksję nad naturą człowieka, technologią i przyszłością cywilizacji.
    Lem jest autorem takich dzieł jak Solaris, Cyberiada, Bajki robotów, Dzienniki gwiazdowe czy Opowieści o pilocie Pirxie. Jego książki zostały przetłumaczone na ponad 40 języków, a łączny nakład przekroczył 45 milionów egzemplarzy, czyniąc go najczęściej tłumaczonym polskim pisarzem.
    Charakterystycznym elementem jego stylu był inteligentny humor, groteska, ironia oraz filozoficzna prowokacja. Lem wykorzystywał fantastykę naukową nie tylko do tworzenia wizji przyszłości, lecz przede wszystkim do krytycznego komentowania współczesnego świata, ludzkich słabości i ograniczeń poznania.
    Do dziś pozostaje jednym z najważniejszych i najbardziej oryginalnych twórców światowej literatury science fiction, a jego dzieła wciąż inspirują naukowców, filozofów, programistów i artystów na całym świecie.'''

subjects = 'Podaj jaki temat Cie interesuje'

# ================
# FUNCTIONS
# ================

# --- LANDING PAGE
# """
# Renders the landing page of the application.

# The function translates the page content into the user's selected language,
# displays a video or image of Stanisław Lem in the first column,
# and shows the translated biography in the second column.

# Returns the search query entered by the user.
# """
def render_landing_page()->str:
    lang = st.session_state.language

    translated_intro = translate_text(intro_text, lang)
    translated_bio = translate_text(lem_bio, lang)
    translated_subjects = translate_text(subjects, lang)

    st. header('LemLibrary')
    st.text(translated_intro)

    # 2 columns
    col1, col2 = st.columns([1, 2])  # proportion of columns: 1:2

    with col1:

        if os.path.exists(video_path):
            render_loop_video("assets/main/1966_rakieta-778x1024-1©_by_Tomasz_Lem_movie.mp4")
        else:

            st.image(image_path, width=300)
        st.text('1966_rakieta_©_by_Tomasz_Lem')

    with col2:
        st.header("Stanisław Lem")
        st.text(translated_bio)

    user_concepts = st.text_input(translated_subjects)
    return user_concepts

# --- RENDER FOOT
def render_foot():

    with st.expander("Credits"):
        st.write("Photo: 1966_rakieta_©_by_Tomasz_Lem")
        st.write('Taken from: https://instytutpolski.pl/minsk/pl/stanislaw-lem-zyciorys/')
        st.write('About author: https://krzysztofzakrzewski.github.io/portfolio/')
        st.write('linkedin: https://www.linkedin.com/in/krzysztof-zakrzewski-206554258/')
        st.write('github: https://github.com/KrzysztofZakrzewski')