def extract_file_paths(file_path):
    file_paths = set()
    with open(file_path, 'r') as file:
        for line in file:
            # Extract the full path up to the file name
            path = line.strip().split(': ')[0]
            file_paths.add(path)
    return file_paths

def compare_files(file1, file2):
    # Extract file paths from both files
    file_paths1 = extract_file_paths(file1)
    file_paths2 = extract_file_paths(file2)
    
    # Find file paths in file1 not in file2
    missing_files = file_paths1 - file_paths2
    return missing_files

def save_to_file(missing_files, output_file):
    # Save the missing file paths to a text file
    with open(output_file, 'w') as file:
        for file_path in sorted(missing_files):
            file.write(f"{file_path}\n")

# Replace 'path_to_txt1' and 'path_to_txt2' with your actual file paths
txt1 = '/mundus/abadawi696/slibrilight/slibrilight-medium/duration-medium-mundus.txt'
txt2 = '/mundus/abadawi696/slibrilight/slibrilight-medium/duration-medium-orignal.txt'

missing_in_txt2 = compare_files(txt1, txt2)
output_file_path = '/mundus/abadawi696/slibrilight/slibrilight-medium/missing_file_paths_medium.txt'  # Output file path
save_to_file(missing_in_txt2, output_file_path)

print(f"All paths of files in txt1 not in txt2 have been saved to {output_file_path}")
