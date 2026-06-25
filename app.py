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
from src.database.feedback_repository import (
    save_feedback
)
from src.database.analytics_repository import (
    save_query_analytics,
    get_analytics_stats
)
from src.database.error_repository import (
    log_error,
    get_recent_errors
)
import traceback

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

col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
with col1:
    st.write(f"Welcome, {st.session_state.username}!")
with col2:
    show_clear_chat()
with col3:
    if st.button("💾 Export"):
        if st.session_state.messages:
            # Create export content
            export_text = f"Medical Literature Assistant - Chat History\n"
            export_text += f"User: {st.session_state.username}\n"
            export_text += f"Export Date: {st.session_state.get('export_date', 'N/A')}\n"
            export_text += "=" * 50 + "\n\n"

            for idx, message in enumerate(reversed(st.session_state.messages), 1):
                export_text += f"--- Q&A {idx} ---\n"
                export_text += f"Question: {message['question']}\n"
                export_text += f"Answer: {message['answer']}\n"
                if message.get("confidence") is not None:
                    export_text += f"Confidence: {message['confidence']}\n"
                export_text += f"Sources: {len(message['sources'])} source(s)\n"
                for source in message['sources']:
                    page_info = f" | Page {source.get('page', 'N/A')}" if source.get('page') else ""
                    export_text += f"  - {source['pdf']} | Chunk {source['chunk']}{page_info}\n"
                export_text += "\n"

            st.download_button(
                label="Download TXT",
                data=export_text,
                file_name=f"chat_history_{st.session_state.username}_{st.session_state.get('export_date', 'export')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("No chat history to export.")
with col4:
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

            try:
                answer, sources, confidence, timing = ask_question(
                question,
                st.session_state.messages,
                st.session_state.user_id
            )

                # Fallback for None or failed answer
                if not answer or answer == "Gemini request failed." or answer == "The language model is temporarily unavailable. Please try again.":
                    answer = "I could not generate an answer from the retrieved context."
                    confidence = 0.0
                    timing = {"retrieval_time": 0, "generation_time": 0, "total_time": 0}

                # Save Conversation
                message = {
                    "question": question,
                    "answer": answer,
                    "sources": sources,
                    "confidence": confidence
                }
                st.session_state.messages.append(message)

                # Save to database
                try:
                    chat = save_chat(
                        st.session_state.user_id,
                        question,
                        answer,
                        sources,
                        confidence
                    )
                    # Store db_id for feedback
                    message["db_id"] = chat.id
                    
                    # Save query analytics
                    try:
                        save_query_analytics(
                            st.session_state.user_id,
                            question,
                            retrieval_time=timing.get("retrieval_time"),
                            generation_time=timing.get("generation_time"),
                            total_time=timing.get("total_time"),
                            confidence=confidence,
                            num_sources=len(sources)
                        )
                    except Exception as e:
                        print(f"Error saving analytics: {e}")
                except Exception as e:
                    st.error(f"Error saving chat to database: {e}")
                    log_error(st.session_state.user_id, "DatabaseError", str(e), traceback.format_exc())
            except Exception as e:
                st.error(f"An error occurred: {e}")
                log_error(st.session_state.user_id, "QueryError", str(e), traceback.format_exc())

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

            # Display confidence score if available
            if message.get("confidence") is not None:
                st.caption(
                    f"Confidence Score: {message['confidence']}"
                )

            # Feedback buttons
            col_like, col_dislike = st.columns([1, 1])
            with col_like:
                if st.button("👍", key=f"like_{message.get('id', id(message))}"):
                    try:
                        save_feedback(st.session_state.user_id, message.get('db_id'), True)
                        st.success("Thanks for your feedback!")
                    except Exception as e:
                        st.error(f"Error saving feedback: {e}")
            with col_dislike:
                if st.button("👎", key=f"dislike_{message.get('id', id(message))}"):
                    try:
                        save_feedback(st.session_state.user_id, message.get('db_id'), False)
                        st.success("Thanks for your feedback!")
                    except Exception as e:
                        st.error(f"Error saving feedback: {e}")

            st.subheader("Sources")

            for source in message["sources"]:

                # Build source label with page number if available
                page_info = f" | Page {source.get('page', 'N/A')}" if source.get('page') else ""
                source_label = f"{source['pdf']} | Chunk {source['chunk']}{page_info}"

                with st.expander(source_label):

                    st.write(
                        f"Reranker Score: {source['score']}"
                    )

                    # Show full chunk text if available
                    if source.get('text'):
                        st.text_area(
                            "Chunk Text",
                            source['text'],
                            height=200,
                            key=f"chunk_{source['chunk']}"
                        )
                    else:
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

# =========================
# Admin Dashboard
# =========================

st.divider()
st.header("📊 System Analytics")

try:
    stats = get_analytics_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Queries", stats["total_queries"])
    with col2:
        st.metric("Avg Retrieval Time", f"{stats['avg_retrieval_time']}s")
    with col3:
        st.metric("Avg Generation Time", f"{stats['avg_generation_time']}s")
    with col4:
        st.metric("Avg Confidence", stats["avg_confidence"])
    
    # Recent Errors
    st.subheader("Recent Errors")
    try:
        recent_errors = get_recent_errors(limit=5)
        if recent_errors:
            for error in recent_errors:
                with st.expander(f"{error.error_type} - {error.created_at.strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**Error:** {error.error_message}")
                    if error.stack_trace:
                        with st.expander("Stack Trace"):
                            st.code(error.stack_trace)
        else:
            st.info("No recent errors")
    except Exception as e:
        st.error(f"Error loading error logs: {e}")
except Exception as e:
    st.error(f"Error loading analytics: {e}")