import json
from collections import defaultdict

file_path = "/mundus/abadawi696/slibrilight/slibrilight-medium/sorted_libriheavy_cuts_medium.jsonl"

# Initialize a dictionary to hold concatenated texts keyed by the unique audio name
audio_texts_first_element = defaultdict(set)  # Using set to prevent duplicates

# Open the JSONL file and process each line
with open(file_path, 'r') as file:
    for line in file:
        data = json.loads(line)
        
        # Parse the 'id' to extract the unique audio file identifier
        audio_id = data['id'].split('/')[2]
        
        # Extract the first element of texts from the custom field within supervisions
        for supervision in data['supervisions']:
            if 'custom' in supervision and 'texts' in supervision['custom'] and len(supervision['custom']['texts']) > 0:
                # Add only the first element of texts, using set to avoid duplicates
                audio_texts_first_element[audio_id].add(supervision['custom']['texts'][0])

# Convert sets of texts into single strings for each unique identifier
concatenated_texts_first_element = {k: ' '.join(v) for k, v in audio_texts_first_element.items()}

# Define the path for the output JSON file
output_file_path = '/mundus/abadawi696/slibrilight/slibrilight-medium/sorted-text.jsonl'

# Save the concatenated texts to a JSON file
with open(output_file_path, 'w') as json_file:
    json.dump(concatenated_texts_first_element, json_file, ensure_ascii=False, indent=4)

print(f"Results saved to {output_file_path}")
