import argparse
import base64
import os
import sys

def create_file(base_path, current_level, i, file_size_kb=1):
    # Create a file
    file_name = f"file_{current_level}_{i}.txt"
    file_path = os.path.join(base_path, file_name)
    
    b64_content = base64.b64encode(os.urandom(int(file_size_kb * 1024))).decode('utf-8')
    
    with open(file_path, 'w') as f:
        f.write(b64_content)

def create_structure(base_path, depth, breadth, file_size_kb=1, current_level=1):
    for i in range(breadth):
        # Delegate file creation to the helper
        create_file(base_path, current_level, i, file_size_kb)
        
        if depth > 0:
            # Handle directory creation directly in this generator function
            dir_name = f"dir_{current_level}_{i}"
            dir_path = os.path.join(base_path, dir_name)
            os.makedirs(dir_path, exist_ok=True)
                 
            # Recurse into the new directory
            create_structure(dir_path, depth - 1, breadth, file_size_kb, current_level + 1)

def main():
    parser = argparse.ArgumentParser(description="Test file tree structure generator")
    parser.add_argument('--depth', type=int, default=3,required=True, help='Depth of the recursive tree')
    parser.add_argument('--breadth', type=int, default=3, required=True, help='Number of files and folders at each level')
    parser.add_argument('--size', type=float, default=1.0, help='Size of generated files in KB (default: 1.0)')
    parser.add_argument('--path', type=str, default='.', help='Base output path (defaults to current directory)')
    
    args = parser.parse_args()
    
    # Ensure the base path exists
    try:
        os.makedirs(args.path, exist_ok=True)
        print(f"Generating test structure at '{args.path}' (Depth: {args.depth}, Breadth: {args.breadth}, Size: {args.size}KB)...")
        create_structure(args.path, args.depth, args.breadth, args.size)
        print("Done!")
    except Exception as e:
        print(f"Error creating structure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()