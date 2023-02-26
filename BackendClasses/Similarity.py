from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.metrics.pairwise import cosine_similarity

def Similarity(participants: list[str], desc: str):
    # Create the Document Term Matrix
    vectorizer = TfidfVectorizer()
    cleaned_participants = []
    
    for participant in participants:
        cleaned_participants.append(re.sub(r'[^\w\s]', '', participant.lower()))

    data = vectorizer.fit_transform(cleaned_participants)

    description = vectorizer.transform([desc.lower()])
    similarities = cosine_similarity(data, description)

    return [similarity[0] for similarity in similarities]