from flask import Flask, render_template, request
import spacy
import random

# Initialize the Flask app
app = Flask(__name__)

# Load the spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Function to extract concepts
def extract_concepts(text):
    doc = nlp(text)
    concepts = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    return list(set(concepts))  # Remove duplicates

# Function to generate questions
def generate_question(concept, text):
    templates = [
        f"What is the role of {concept} in the text?",
        f"How does {concept} contribute to the process described?",
        f"Which statement best describes {concept}?",
        f"In the context of the passage, explain {concept}.",
        f"Why is {concept} important?"
    ]
    question = random.choice(templates)
    sentences = [sent.text for sent in nlp(text).sents if concept in sent.text]
    correct_answer = sentences[0] if sentences else f"{concept} is important."
    distractors = [c for c in extract_concepts(text) if c != concept]
    distractors = random.sample(distractors, min(3, len(distractors)))
    options = distractors + [correct_answer]
    random.shuffle(options)
    return question, options, correct_answer

# Home route for input form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    input_text = request.form['text']
    concepts = extract_concepts(input_text)
    quiz = []
    for concept in concepts:
        question, options, answer = generate_question(concept, input_text)
        quiz.append({'question': question, 'options': options, 'answer': answer})
    return render_template('quiz.html', quiz=quiz)

if __name__ == '__main__':
    app.run(debug=True)
