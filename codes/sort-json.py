import json
from collections import defaultdict
import os

# Path to your JSONL file
file_path = "/mundus/abadawi696/slibrilight/slibrilight-medium/libriheavy_cuts_medium.jsonl"

def read_and_sort_jsonl(file_path):
    # Read JSONL data into a list of dictionaries
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]

    # Group data by 'recording_id' and sort each group by 'start' time
    grouped_data = defaultdict(list)
    for item in data:
        recording_id = item['supervisions'][0]['recording_id']  # Assumes 'recording_id' exists in the first item of 'supervisions'
        grouped_data[recording_id].append(item)

    # Sort each group by 'start' time
    for key in grouped_data:
        grouped_data[key] = sorted(grouped_data[key], key=lambda x: x['start'])

    # Flatten sorted groups into a single list
    sorted_data = [item for sublist in grouped_data.values() for item in sublist]

    # Write the sorted data back to a new JSONL file
    dir_name, base_filename = os.path.split(file_path)
    sorted_file_path = os.path.join(dir_name, 'sorted_' + base_filename)
    with open(sorted_file_path, 'w') as file:
        for entry in sorted_data:
            json.dump(entry, file)
            file.write('\n')

    print(f"Data sorted and saved to {sorted_file_path}")

# Run the function
read_and_sort_jsonl(file_path)
