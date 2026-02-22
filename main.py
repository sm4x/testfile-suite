import argparse
import base64
import os
import sys

def create_file(base_path, current_level, i, file_size_kb=1):
    """
    Creates a single text file populated with randomized base64 encoded data.
    
    Args:
        base_path (str): The directory where the file should be created.
        current_level (int): The current depth level of the recursive generation (used for naming).
        i (int): The index of the file at the current level (used for naming).
        file_size_kb (float, optional): The target size of the file in kilobytes. Defaults to 1.
                                        Note: Base64 encoding inflates the size by ~33%, so 
                                        the random byte count is calculated before encoding.
    """

    # Construct the parameterized file name
    file_name = f"file_{current_level}_{i}.txt"
    file_path = os.path.join(base_path, file_name)
    
    # Calculate the required number of random bytes (1 KB = 1024 bytes)
    # The os.urandom function generates secure random bytes, which we then encode to base64.
    b64_content = base64.b64encode(os.urandom(int(file_size_kb * 1024))).decode('utf-8')
    
    # Write the base64 string to the target file
    with open(file_path, 'w') as f:
        f.write(b64_content)


def create_structure(base_path, depth, breadth, file_size_kb=1, current_level=1):
    """
    Recursively generates a hierarchical tree of directories and files.
    
    Args:
        base_path (str): The root directory for the current step of generation.
        depth (int): How many more levels deep the generator should traverse.
                     When depth hits 0, it stops creating deeper directories.
        breadth (int): The number of files and subdirectories to create at each level.
        file_size_kb (float, optional): Passed down to `create_file` to determine file size.
        current_level (int, optional): Tracks the current recursion depth for naming. Defaults to 1.
    """
    for i in range(breadth):
        # 1. File Generation
        # Regardless of whether we are at the bottom of the tree (depth=0) or not,
        # we always want to populate the *current* directory with files.
        create_file(base_path, current_level, i, file_size_kb)
        
        # 2. Directory Generation & Recursion
        # Only create subdirectories and recurse deeper if we haven't reached the target depth.
        if depth > 0:
            dir_name = f"dir_{current_level}_{i}"
            dir_path = os.path.join(base_path, dir_name)
            
            # Create the subdirectory (exist_ok prevents errors if the path already exists)
            os.makedirs(dir_path, exist_ok=True)
                 
            # Recursively call this function for the newly created subdirectory,
            # decrementing the depth counter and incrementing the level counter.
            create_structure(dir_path, depth - 1, breadth, file_size_kb, current_level + 1)

def main():
    """
    Entry point for the script. Handles command line argument parsing and initiates generation.
    """
    parser = argparse.ArgumentParser(description="Test file tree structure generator")
    
    # Define the expected command-line arguments
    parser.add_argument('--depth', type=int, default=3, required=True, 
                        help='Depth of the recursive tree (how many sub-folders deep it goes)')
    parser.add_argument('--breadth', type=int, default=3, required=True, 
                        help='Number of files and folders to create at each level of the tree')
    parser.add_argument('--size', type=float, default=1.0, 
                        help='Target size of each generated text file in KB (default: 1.0)')
    parser.add_argument('--path', type=str, default='.', 
                        help='Base output path for the root of the tree (defaults to current directory)')
    
    # Parse the arguments provided by the user
    args = parser.parse_args()
    
    try:
        # Ensure the specified root destination path exists before starting
        os.makedirs(args.path, exist_ok=True)
        
        print(f"Generating test structure at '{args.path}'...")
        print(f"Configuration -> Depth: {args.depth}, Breadth: {args.breadth}, File Size: {args.size}KB")
        
        # Begin the recursive structure generation
        create_structure(args.path, args.depth, args.breadth, args.size)
        
        print("Done! The test suite has been successfully created.")
        
    except Exception as e:
        # Catch any unexpected file system or generation errors
        print(f"Error creating structure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()