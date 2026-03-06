import streamlit as st
import os
from ui.lnadingpage import render_landing_page, render_foot
from src.vectorstore import (
    get_qdrant_client,
    init_collection,
    index_books,
    search_books
)

from src.translation_ai import translate_text, normalize_language, render_books

st.set_page_config(
    page_title="LemLibrary",
    page_icon="🪐",
)

#=================
# SESSION STATE 
#=================

# --- Query
if "last_query" not in st.session_state:
    st.session_state["last_query"] = ""

# --- Qdarant client
if "client" not in st.session_state:
    # Creates a Qdrant client for working with embedding collections.
    client = get_qdrant_client(memory=True)
    # Init collection
    init_collection(client)
    # Indexes books into the Qdrant collection by converting them into embeddings
    index_books(client)
    # Saves client in session_state
    st.session_state["client"] = client
else:
    # If Qdrat client exist leave it allone
    client = st.session_state["client"]

# --- Language
if "language" not in st.session_state:
    st.session_state.language = None

# take language from session_state in to variable
lang = st.session_state.language

# --- Render the semantic language selection
if st.session_state.language is None:

# If no language is set in session_state, display the language selection screen.
# The user can enter any language name which is normalized using the LLM.
# If the language is recognized, it is stored in session_state and the app reruns.
# Execution is stopped until a valid language is provided.
    st.markdown("## 🌍 ")
    st.markdown(
        """
        ᓂᕈᐊᕐᓗᒍ ᐅᖃᐅᓯᖅ

        Wybierz język
        
        Select language

        选择语言
        
        Seleccionar idioma
        
        भाषा चुने
        
        выберите язык
        
        sélectionner la langue 
        """
    )
    st.markdown("## ⬇️ ")
    user_lang_input = st.text_input(
        "."
    )
    if user_lang_input:
        normalized = normalize_language(user_lang_input)
        if normalized == "unknown":
            st.error("ᐅᖃᐅᓯᖅ ᐃᓕᑕᕆᔭᐅᓯᒪᙱᑦᑐᖅ. ᐆᑦᑐᑲᓐᓂᕆᑦ.")
        else:
            st.session_state.language = normalized
            st.rerun()
    st.stop()

#=================
# UI
#=================

# Renders the landing page UI and returns the user's input query.
query = render_landing_page()

if query:
    # saves the last query in sessionstate
    st.session_state["last_query"] = query
    # searches for books that match the embeddings
    top_books = search_books(client, query, top_k=3)
    # displays results (books)
    render_books(top_books)


# Runs only if the user entered any text
# if query:

#     lang = st.session_state.language
#     # Stores the current query in session state.
#     st.session_state["last_query"] = query

#     # Performs semantic search using vector similarity
#     # and returns the top 3 most relevant results.
#     results = search_books(client, query, top_k=2)

#     # Checks if any results were returned.
#     if results:
#         # Retrieves the highest scoring result.
#         top = results[0]
#         # st.subheader("TOP MATCH:")
#         # st.write(top.payload)
#         # st.write(f"Score: {top.score:.4f}")

#     # st.subheader(translate_text("Wszystkie wyniki:", lang))
#     # Iterates through all returned results.
#     for r in results:
#     #     st.write(f"**{translate_text('Książka:', lang)}** {translate_text(r.payload['book'], lang)}")
#     #     st.write(f"**{translate_text('Opowiadanie:', lang)}** {translate_text(r.payload['name'], lang)}")
#     #     #show the image
#         image_path = r.payload.get("image")


#     if image_path and os.path.exists(image_path):
#         st.image(image_path, width="stretch")

    
#     description = r.payload.get("description", "brak opisu")
#     st.write(translate_text(description, lang))
#     # st.write(f"Score: {r.score:.4f}")
#     st.write("---")

#     st.write("DEBUG results:", len(results))

# Displays the last user query stored in session state.
if "last_query" in st.session_state:
    lang = st.session_state.language

    translated_label = translate_text("Ostatnie wyszukiwanie:", lang)

    st.write(f"{translated_label} {st.session_state['last_query']}")

# RENDER FOOt WITH CREDITS
render_foot()

