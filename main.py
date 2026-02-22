import argparse
import base64
import os
import sys

def create_file(base_path, current_level, i):
    # Create a file
    file_name = f"file_{current_level}_{i}.txt"
    file_path = os.path.join(base_path, file_name)
    
    # Generate some simple base64 content
    content = f"Level: {current_level}, Index: {i}".encode('utf-8')
    b64_content = base64.b64encode(content).decode('utf-8')
    
    with open(file_path, 'w') as f:
        f.write(b64_content)
        
    # Create a directory
    dir_name = f"dir_{current_level}_{i}"
    dir_path = os.path.join(base_path, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    
    return dir_path

def create_structure(base_path, depth, breadth, current_level=1):
    if depth == 0:
        return
        
    for i in range(breadth):
        dir_path = create_file(base_path, current_level, i)
        
        # Recurse into the new directory
        create_structure(dir_path, depth - 1, breadth, current_level + 1)

def main():
    parser = argparse.ArgumentParser(description="Test file tree structure generator")
    parser.add_argument('--depth', type=int, required=True, help='Depth of the recursive tree')
    parser.add_argument('--breadth', type=int, required=True, help='Number of files and folders at each level')
    parser.add_argument('--path', type=str, default='.', help='Base output path (defaults to current directory)')
    
    args = parser.parse_args()
    
    # Ensure the base path exists
    try:
        os.makedirs(args.path, exist_ok=True)
        print(f"Generating test structure at '{args.path}' (Depth: {args.depth}, Breadth: {args.breadth})...")
        create_structure(args.path, args.depth, args.breadth)
        print("Done!")
    except Exception as e:
        print(f"Error creating structure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()