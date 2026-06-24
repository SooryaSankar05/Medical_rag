import streamlit as st

from src.pipeline.rag_pipeline import (
    ask_question
)
import os
from src.ingestion.add_pdf import (
    add_pdf
)
from src.database.user_repository import (
    create_user,
    verify_user_credentials,
    get_user_by_username
)
from src.database.chat_repository import (
    save_chat,
    load_chat,
    clear_chat
)
from src.database.document_repository import (
    save_document,
    get_documents_by_user,
    delete_document
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

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

# =========================
# Authentication Functions
# =========================

def show_login_page():
    st.title("🩺 Medical Literature Assistant")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            if verify_user_credentials(username, password):
                user = get_user_by_username(username)
                st.session_state.user_id = user.id
                st.session_state.username = user.username
                st.session_state.auth_page = "authenticated"
                
                # Load chat history from database
                st.session_state.messages = load_chat(user.id)
                
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
        else:
            st.error("Please enter both username and password")

    if st.button("Create an account"):
        st.session_state.auth_page = "signup"
        st.rerun()


def show_signup_page():
    st.title("🩺 Medical Literature Assistant")
    st.subheader("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if username and password and confirm_password:
            if password != confirm_password:
                st.error("Passwords do not match")
            else:
                try:
                    create_user(username, password)
                    st.success("Account created successfully! Please login.")
                    st.session_state.auth_page = "login"
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error("Error creating account. Please try again.")
        else:
            st.error("Please fill in all fields")

    if st.button("Back to Login"):
        st.session_state.auth_page = "login"
        st.rerun()


def show_logout():
    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.auth_page = "login"
        st.session_state.messages = []
        st.rerun()


def show_clear_chat():
    if st.button("Clear Chat History"):
        try:
            clear_chat(st.session_state.user_id)
            st.session_state.messages = []
            st.success("Chat history cleared!")
            st.rerun()
        except Exception as e:
            st.error("Error clearing chat history")


# =========================
# Authentication Flow
# =========================

if not st.session_state.user_id:
    if st.session_state.auth_page == "login":
        show_login_page()
    elif st.session_state.auth_page == "signup":
        show_signup_page()
    st.stop()

# =========================
# Main App (Authenticated)
# =========================

st.title("🩺 Medical Literature Assistant")

col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    st.write(f"Welcome, {st.session_state.username}!")
with col2:
    show_clear_chat()
with col3:
    show_logout()

st.divider()

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
            st.session_state.messages,
            st.session_state.user_id
        )

        # Fallback for None or failed answer
        if not answer or answer == "Gemini request failed." or answer == "The language model is temporarily unavailable. Please try again.":
            answer = "I could not generate an answer from the retrieved context."

        # Save Conversation
        message = {
            "question": question,
            "answer": answer,
            "sources": sources
        }
        st.session_state.messages.append(message)

        # Save to database
        try:
            save_chat(
                st.session_state.user_id,
                question,
                answer,
                sources
            )
        except Exception as e:
            st.error(f"Error saving chat to database: {e}")

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

# =========================
# PDF Upload
# =========================

st.header("Upload PDF")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    save_path = os.path.join(
        "data/raw",
        uploaded_file.name
    )

    # Check if document already exists for this user
    existing_docs = get_documents_by_user(st.session_state.user_id)
    doc_exists = any(doc.filename == uploaded_file.name for doc in existing_docs)

    if not doc_exists:
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

            print("[INGESTION] Processing new PDF upload")
            add_pdf(
                save_path,
                st.session_state.user_id
            )

        # Save document metadata to database
        try:
            save_document(
                st.session_state.user_id,
                uploaded_file.name,
                save_path
            )
        except ValueError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Error saving document metadata: {e}")
            st.stop()

        st.success(
            f"{uploaded_file.name} added to knowledge base."
        )
    else:
        st.info(f"Document '{uploaded_file.name}' already uploaded.")

# =========================
# Document Listing
# =========================

st.header("Your Documents")

documents = get_documents_by_user(st.session_state.user_id)

if documents:
    for doc in documents:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{doc.filename}**")
                st.caption(f"Uploaded: {doc.uploaded_at.strftime('%Y-%m-%d %H:%M')}")
            with col2:
                if st.button("Delete", key=f"delete_{doc.id}"):
                    try:
                        delete_document(doc.id, st.session_state.user_id)
                        st.success("Document deleted!")
                        st.rerun()
                    except PermissionError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Error deleting document: {e}")
            st.divider()
else:
    st.write("No documents uploaded yet.")