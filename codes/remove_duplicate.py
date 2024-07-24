from nltk.tokenize import sent_tokenize
import json
import nltk

# Ensure the necessary NLTK resources are available
nltk.download('punkt')

def remove_duplicates(text, min_length=20):
    sentences = sent_tokenize(text)
    seen = set()
    duplicates = set()
    cleaned_sentences = []
    
    for sentence in sentences:
        if len(sentence) < min_length:
            # Add short sentences directly to the cleaned text without checking for duplicates
            cleaned_sentences.append(sentence)
        elif sentence in seen:
            duplicates.add(sentence)
        else:
            seen.add(sentence)
            cleaned_sentences.append(sentence)
    
    cleaned_text = ' '.join(cleaned_sentences)
    return cleaned_text, duplicates

def clean_json_data(file_path, output_path):
    # Load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Process the text to remove duplicates, report them, and replace specific phrases
    cleaned_data = {}
    all_duplicates = {}
    for key, value in data.items():
        # Replace the specific phrase
        modified_text = value.replace("please visit LibriVox.org.", "please visit LibriVox dot org.")
        # Remove duplicates
        cleaned_text, duplicates = remove_duplicates(modified_text)
        cleaned_data[key] = cleaned_text
        if duplicates:
            all_duplicates[key] = list(duplicates)
    
    # Save the cleaned data to a new JSON file
    with open(output_path, 'w') as file:
        json.dump(cleaned_data, file, indent=4)
    
    return all_duplicates

# Example usage
input_file_path = '/mundus/abadawi696/slibrilight/slibrilight-large/appended-json-large.json'
output_file_path = '/mundus/abadawi696/slibrilight/slibrilight-large/clean-appended-json-large.json'
duplicates_found = clean_json_data(input_file_path, output_file_path)
