import os
import json

def extract_text_source_urls_from_json(directory):
    urls = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    try:
                        data = json.load(json_file)
                        if 'book_meta' in data and 'url_text_source' in data['book_meta']:
                            urls.append(data['book_meta']['url_text_source'])
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")
    return urls

if __name__ == "__main__":
    directory = "/home/mundus/abadawi696/libri-light-metadata-json/Libri-light/large"
    urls = extract_text_source_urls_from_json(directory)
    with open("text_urls.txt", "w") as f:
        for url in urls:
            f.write(url + "\n")
