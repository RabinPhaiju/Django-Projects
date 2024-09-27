import os

def handle_uploaded_file(f):
    file_path = "uploaded_files/name.txt"
    
    # Ensure the directory exists, create it if necessary
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Open the file and write its contents
    with open(file_path, "ab+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
