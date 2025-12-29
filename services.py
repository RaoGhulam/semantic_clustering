from get_entities import get_entities
import os

# Load ontology file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ontology_file = os.path.join(BASE_DIR, "new_islam_ontology_tur.ttl")

def split_into_sentences(text):
    sentences = [line.strip() for line in text.split('\n') if line.strip()]
    return sentences

def get_sentences_from_files(files):
    sentences = []
    for file in files:
        # Read the file content as text (assuming UTF-8)
        text = file.read().decode('utf-8')
        # Split by newline and strip empty lines
        file_sentences = [line.strip() for line in text.split('\n') if line.strip()]
        sentences.extend(file_sentences)
        # Reset file pointer in case it needs to be read again
        file.seek(0)
    return sentences

def get_entities_from_sentences(sentences):
    all_entities = []
    
    for sent in sentences:
        entities_a = get_entities(sent, ontology_file)
        all_entities.append(entities_a)
    
    return all_entities
