from dotenv import dotenv_values
from openai import OpenAI
import os

env = dotenv_values(".env")

def get_openai_client():
    return OpenAI(api_key=env["OPENAI_API_KEY"])


from openai import OpenAI
import streamlit as st

client = get_openai_client()

def translate_text(text: str, target_language: str) -> str:

    if target_language.lower() in ["polish", "polski", "pl"]:
        return text

    cache_key = f"{target_language}:{text}"

    if "translation_cache" not in st.session_state:
        st.session_state.translation_cache = {}

    if cache_key in st.session_state.translation_cache:
        return st.session_state.translation_cache[cache_key]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional literary translator."
            },
            {
                "role": "user",
                "content": f"""
                Translate the following Polish text into fluent, natural {target_language}.
                Preserve tone, meaning and formatting.

                Text:
                {text}
                """
            }
        ],
        temperature=0.3
    )

    translated = response.choices[0].message.content.strip()

    st.session_state.translation_cache[cache_key] = translated

    return translated


def normalize_language(user_input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You normalize language names."
            },
            {
                "role": "user",
                "content": f"""
                The user wrote this language name: {user_input}.
                Return the correct English name of this language.
                If it does not exist, return 'unknown'.
                Return only the language name.
                """
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()



# def render_books(books: list):

#     lang = st.session_state.language

#     for book in books:

#         translated_title = translate_text(book["name"], lang)
#         translated_description = translate_text(book["description"], lang)
#         translated_genre = translate_text(book["genere"], lang)

#         st.subheader(translated_title)
#         st.markdown(translated_description)
#         st.markdown(f"**Genre:** {translated_genre}")
#         st.markdown("---")


def render_books(results):

    lang = st.session_state.language

    st.subheader(translate_text("Wszystkie wyniki:", lang))

    for r in results:

        st.write(f"**{translate_text('Książka:', lang)}** {translate_text(r.payload['book'], lang)}")
        st.write(f"**{translate_text('Opowiadanie:', lang)}** {translate_text(r.payload['name'], lang)}")

        image_path = r.payload.get("image")

        if image_path and os.path.exists(image_path):
            st.image(image_path, width="stretch")

        description = r.payload.get("description", "brak opisu")
        st.write(translate_text(description, lang))

        st.write(f"Score: {r.score:.4f}")
        st.write("---")