import json
import os
from operator import itemgetter

# Path to your JSONL file
file_path = "/Users/badawi/Desktop/test-json/libriheavy_cuts_small.jsonl"

def extract_data_and_write_new_jsonl(file_path):
    # Read JSONL data into a list of dictionaries
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]

    # Ensure data is sorted by 'recording_id' and then by 'start' time
    data.sort(key=lambda x: (x['supervisions'][0]['recording_id'], x['start']))

    # Prepare simplified data
    simplified_data = []
    for item in data:
        recording_id = item['id']  # Extract the main ID
        texts = item['supervisions'][0]['custom']['texts'][0]  # Extract the first text from 'texts' array

        # Create a new simplified dict
        simplified_entry = {
            "id": recording_id,
            "texts": texts
        }
        simplified_data.append(simplified_entry)

    # Write the simplified data back to a new JSONL file
    dir_name, base_filename = os.path.split(file_path)
    new_file_path = os.path.join(dir_name, 'simplified-final-small_' + base_filename)
    with open(new_file_path, 'w') as file:
        for entry in simplified_data:
            json.dump(entry, file)
            file.write('\n')

    print(f"Simplified data saved to {new_file_path}")

# Run the function
extract_data_and_write_new_jsonl(file_path)
