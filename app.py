import streamlit as st
import os
from ui.lnadingpage import render_landing_page, render_foot
from src.vectorstore import (
    get_qdrant_client,
    init_collection,
    index_books,
    search_books
)

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

#=================
# UI
#=================
# Renders the landing page UI and returns the user's input query.
query = render_landing_page()

# Runs only if the user entered any text
if query:

    # Stores the current query in session state.
    st.session_state["last_query"] = query

    # Performs semantic search using vector similarity
    # and returns the top 3 most relevant results.
    results = search_books(client, query, top_k=3)

    # Checks if any results were returned.
    if results:
        # Retrieves the highest scoring result.
        top = results[0]
        # st.subheader("TOP MATCH:")
        # st.write(top.payload)
        st.write(f"Score: {top.score:.4f}")

    st.subheader("Wszystkie wyniki:")
    # Iterates through all returned results.
    for r in results:
        st.write(f"**Książka:** {r.payload['book']}")
        st.write(f"**Opowiadanie:** {r.payload['name']}")
        #show the image
        image_path = r.payload.get("image")

        if image_path and os.path.exists(image_path):
            st.image(image_path, width="stretch")

        
        st.write(r.payload.get("description", "brak opisu"))
        st.write(f"Score: {r.score:.4f}")
        st.write("---")
# Displays the last user query stored in session state.
st.write(f"Ostatnie wyszukiwanie: {st.session_state['last_query']}")




render_foot()

