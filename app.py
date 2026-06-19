import streamlit as st

from src.pipeline.rag_pipeline import (
    ask_question
)
import os
from src.ingestion.add_pdf import (
    add_pdf
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)
# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="Medical Literature Assistant",
    page_icon="🩺",
    layout="wide"
)

# =========================
# Session State
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Title
# =========================

st.title("🩺 Medical Literature Assistant")

question = st.text_input(
    "Ask a medical question:"
)

# =========================
# Search Button
# =========================

if st.button("Search"):

    if question:

        with st.spinner(
            "Searching medical literature..."
        ):

            answer, sources = ask_question(
            question,
            st.session_state.messages
        )

        # Save Conversation
        st.session_state.messages.append(
            {
                "question": question,
                "answer": answer,
                "sources": sources
            }
        )

# =========================
# Chat History
# =========================

if st.session_state.messages:

    st.header("Conversation")

    for message in reversed(
        st.session_state.messages
    ):

        with st.container():

            st.subheader("Question")

            st.write(
                message["question"]
            )

            st.subheader("Answer")

            st.write(
                message["answer"]
            )

            st.subheader("Sources")

            for source in message["sources"]:

                with st.expander(
                    f"{source['pdf']} | Chunk {source['chunk']}"
                ):

                    st.write(
                        f"Reranker Score: {source['score']}"
                    )

                    st.write(
                        source["preview"]
                    )

            st.divider()

if uploaded_file:

    save_path = os.path.join(
        "data/raw",
        uploaded_file.name
    )

    with open(
        save_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    with st.spinner(
        "Processing PDF..."
    ):

        add_pdf(
            save_path
        )

    st.success(
        f"{uploaded_file.name} added to knowledge base."
    )