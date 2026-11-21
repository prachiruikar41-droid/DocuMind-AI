import streamlit as st
import requests

from rag import extract_text_from_pdf, retrieve_relevant_chunks
from embeddings import split_text_into_chunks, get_embedding


st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="centered"
)

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1120, #111827, #172554);
    color: #f8fafc;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label, .stMarkdown {
    color: #cbd5e1;
}

div[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.65);
    border: 1px dashed #64748b;
    border-radius: 16px;
    padding: 15px;
}

div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #4338ca);
    color: white;
    border: none;
}

div[data-testid="stTextInput"] input {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}

div[data-testid="stExpander"] {
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid #334155;
    border-radius: 12px;
}

.answer-card {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 16px;
    margin-top: 15px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #334155;
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown("""
<div style="text-align:center; padding:10px 0 20px 0;">
    <div style="font-size:48px;">📚</div>
    <h1 style="font-size:42px; margin-bottom:0;">
        DocuMind AI
    </h1>
    <p style="font-size:17px; color:#94a3b8;">
        Intelligent PDF Assistant
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding-bottom:20px;">
    <p>Upload your document and ask questions.
    Get intelligent answers from your PDF using AI.</p>
</div>
""", unsafe_allow_html=True)


# ---------- AI ANSWER ----------
def generate_answer(question, context):

    prompt = f"""
    Answer the question using only the context below.
    If the answer is not in the context,
    say you cannot find it in the PDF.

    Context:
    {context}

    Question:
    {question}
    """

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:4b",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["message"]["content"]


# ---------- PDF UPLOAD ----------
st.markdown("### 📄 Upload your document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    key="pdf_upload"
)


# ---------- PROCESS PDF ----------
if uploaded_file:

    if st.button("⚡ Process PDF"):

        try:
            with st.spinner("Reading and processing your PDF..."):

                text = extract_text_from_pdf(uploaded_file)

                if not text.strip():
                    st.error("No readable text found in this PDF.")
                    st.stop()

                chunks = split_text_into_chunks(text)

                chunk_embeddings = []

                progress = st.progress(0)

                for i, chunk in enumerate(chunks):
                    chunk_embeddings.append(get_embedding(chunk))
                    progress.progress((i + 1) / len(chunks))

                st.session_state["chunks"] = chunks
                st.session_state["embeddings"] = chunk_embeddings
                st.session_state["pdf_name"] = uploaded_file.name

            st.success(
                f"PDF processed successfully! "
                f"{len(chunks)} chunks created."
            )

        except Exception as e:
            st.error(f"PDF processing failed: {e}")


# ---------- DOCUMENT STATUS ----------
if "chunks" in st.session_state:

    st.markdown("---")

    st.markdown("### ✅ Document ready")

    st.info(
        f"📄 {st.session_state.get('pdf_name', 'Uploaded PDF')}  \n"
        f"🔹 {len(st.session_state['chunks'])} text chunks processed"
    )


# ---------- QUESTION SECTION ----------
if "chunks" in st.session_state:

    st.markdown("---")

    st.markdown("### 💬 Ask your document")

    question = st.text_input(
        "Enter your question",
        placeholder="e.g. What are my technical skills?",
        key="question_input"
    )

    if st.button("🔍 Get Answer"):

        if not question.strip():

            st.warning("Please enter a question first.")

        else:

            try:
                with st.spinner("Finding answer..."):

                    relevant_chunks = retrieve_relevant_chunks(
                        question,
                        st.session_state["chunks"],
                        st.session_state["embeddings"],
                        get_embedding
                    )

                    context = "\n\n".join(relevant_chunks)

                    answer = generate_answer(question, context)

                st.markdown("---")
                st.markdown("### ✨ AI Generated Answer")

                st.markdown(
                    f"""
                    <div class="answer-card">
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                with st.expander("📖 View retrieved context"):

                    for chunk in relevant_chunks:
                        st.write(chunk)
                        st.divider()

            except Exception as e:
                st.error(f"Answer generation failed: {e}")


# ---------- RESET ----------
if "chunks" in st.session_state:

    if st.button("🗑️ Clear document"):

        for key in ["chunks", "embeddings", "pdf_name", "question_input"]:
            st.session_state.pop(key, None)

        st.rerun()


# ---------- FOOTER ----------
st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:15px 0;">
    <p style="color:#94a3b8; font-size:14px;">
        🤖 Powered by Local AI · Ollama
    </p>
    <p style="color:#64748b; font-size:12px;">
        DocuMind AI | PDF Intelligence Assistant
    </p>
</div>
""", unsafe_allow_html=True)
