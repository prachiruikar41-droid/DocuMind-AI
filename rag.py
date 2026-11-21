
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    return text


def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (norm1 * norm2)


def retrieve_relevant_chunks(question, chunks, chunk_embeddings, get_embedding):
    question_embedding = get_embedding(question)

    scores = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(question_embedding, embedding)
        scores.append((score, chunk))

    scores.sort(key=lambda item: item[0], reverse=True)

    return [chunk for score, chunk in scores[:3]]
