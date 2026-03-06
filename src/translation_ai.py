# ================
# IMPORTS
# ================
from dotenv import dotenv_values
from openai import OpenAI
import streamlit as st
import os

# READ .env
env = dotenv_values(".env")

# ================
# FUNCTIONS
# ================

# TAKE OPEN AI KEY
def get_openai_client():
    return OpenAI(api_key=env["OPENAI_API_KEY"])

# CRATING OpenAI CLIENT
client = get_openai_client()

# --- NORMALIZE LANGUAGE
def normalize_language(user_input: str) -> str:
    """
    Normalizes a language name provided by the user.

    The function sends the user input to an OpenAI model which returns
    the correct English name of the language. If the language cannot
    be recognized, the model returns "unknown".
    """
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

# TRANSLATE TEXT OF PAGE
def translate_text(text: str, target_language: str) -> str:
    '''Translates a given text into the user's selected language using an OpenAI model.

    If the target language is Polish, the original text is returned without translation.
    The function uses a translation cache stored in Streamlit session_state to avoid
    repeated API calls for the same text and language combination.

    Each translation is identified by a unique cache key composed of the language
    and the original text. The model is queried with low temperature to produce
    consistent translations. Leading and trailing whitespace is removed before
    returning the translated result.'''

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

# RENDER BOOKS WITH TRANSLATION
def render_books(results):
    """
    Renders book search results in the Streamlit interface.

    The function iterates through results returned by the vector search
    and displays book information including title, story name,
    description and similarity score.

    All visible text is translated into the language selected by the user.
    If an image path exists, the corresponding book image is also displayed.
    """
    lang = st.session_state.language

    st.subheader(translate_text("Wszystkie wyniki:", lang))

    for r in results:

        st.write(f"**{translate_text('Książka:', lang)}** {translate_text(r.payload['book'], lang)}")
        st.write(f"**{translate_text('Tytuł:', lang)}** {translate_text(r.payload['name'], lang)}")
        st.write(f"**{translate_text('Rok:', lang)}** {r.payload['year']}")
        # st.write(f"**{translate_text('rok:', lang)}** {r.payload['year']}")
        # st.write(f"**Year: {r.payload['year']})**")
        image_path = r.payload.get("image")

        if image_path and os.path.exists(image_path):
            st.image(image_path, width="stretch")

        description = r.payload.get("description", "brak opisu")
        st.write(translate_text(description, lang))

        # st.write(f"Score: {r.score:.4f}")
        st.write("---")