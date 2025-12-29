from flask import Flask, render_template, request, jsonify
from services import split_into_sentences, get_sentences_from_files, get_entities_from_sentences
from clustering import cluster_sentences

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text')
    files = request.files.getlist('files')

    # Initialize sentences list
    sentences = []

    if text and files:
        # Both provided, raise error or choose priority
        raise ValueError("Please provide either text or files, not both.")
    elif text:
        # Process text input
        sentences = split_into_sentences(text)
    elif files:
        # Process uploaded files
        sentences = get_sentences_from_files(files)
    else:
        # Neither text nor files provided
        sentences = []

    entities_per_sentence = get_entities_from_sentences(sentences)
    result, number_of_clusters = cluster_sentences(sentences, entities_per_sentence)
    print(number_of_clusters)
    result_fixed = {int(k): v for k, v in result.items()}
    
    return jsonify(result_fixed)

if __name__ == '__main__':
    app.run(debug=True)
