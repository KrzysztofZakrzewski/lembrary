import streamlit as st
import streamlit as st
from ui.lnadingpage import render_landing_page
from src.embedings import get_qdrant_client, init_collection, search_books, print_top_result, get_embedding
from src.embedings import lem_books  # twoja lista książek

if "last_query" not in st.session_state:
    st.session_state["last_query"] = ""


from ui.lnadingpage import render_landing_page
# from src.embedings import *
client = get_qdrant_client(memory=True)
init_collection(client, lem_books)

query = render_landing_page()

# -----------------------------
# Inicjalizacja Qdrant w pamięci
# -----------------------------

# -----------------------------
# Landing page + input
# -----------------------------
# query = render_landing_page()

if query:
    results = search_books(client, query, top_k=3)

    # top wynik
    top_payload, top_score = results[0]
    # st.subheader("Top wynik:")
    # st.write(f"**Tytuł:** {top_payload['name']}")
    # st.write(f"**Score:** {top_score:.4f}")

    st.subheader("Wszystkie wyniki:")
    for payload, score in results:
        st.write(f"**Tytuł książki:** {payload['book']}")
        st.write(f"**Tytuł powieści:** {payload['name']}")
        st.write(payload.get("description", "brak opisu"))
        st.write(f"Score: {score:.4f}")
        st.write("---")

# opcjonalnie pokaż ostatnie wyszukiwanie
st.write(f"Ostatnie wyszukiwanie: {st.session_state['last_query']}")