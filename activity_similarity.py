from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Reference activities used for similarity matching
KNOWN_ACTIVITIES = {
    # Outdoor
    "morning run" : "outdoor",
    "evening run" : "outdoor",
    "walk the dog" : "outdoor",
    "dog walk" : "outdoor",
    "beach day" : "outdoor",
    "hike" : "outdoor",
    "jogging" : "outdoor",
    "5k training" : "outdoor",

    #Indoor
    "doctor appointment" : "indoor",
    "study at library" : "indoor",
    "movie night" : "indoor",
    "gym workout" : "indoor",

    #Errand
    "grocery shopping" : "errand",
    "bank visit" : "errand",
    "costco run" : "errand",
    "pharmacy pickup" : "errand",
    "medicine pickup" : "errand"
}

def classify_by_similarity(user_activity, threshold=0.20):
    activity_names = list(KNOWN_ACTIVITIES.keys())

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(activity_names + [user_activity])

    known_vectors = vectors[:-1]
    user_vector = vectors[-1]

    similarities = cosine_similarity(user_vector, known_vectors)[0]

    best_match_index = similarities.argmax()
    best_match = activity_names[best_match_index]
    best_score = similarities[best_match_index]
    #predicted_category = known_activities[best_match]

    if best_score < threshold:
        return {
        "category" : "unknown",
        "best_match" : None,
        "score" : best_score   
        }

    return {
        "category": KNOWN_ACTIVITIES[best_match], 
        "best_match" : best_match,
        "score" : best_score
    }

if __name__ == "__main__":
    activity = input("Enter an activity: ")

    result = classify_by_similarity(activity)

    print(f"Predicted category: {result["category"]}")
    print(f"Most similar known activity: {result["best_match"]}")
    print(f"Similarity score: {result["score"]:.2f}")