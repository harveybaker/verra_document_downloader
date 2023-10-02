import os
project_id="4321"
# directory_path = f"docs/{project_id}"

# # Check if the directory already exists
# if not os.path.exists(directory_path):
#     # If it doesn't exist, create the directory
#     os.makedirs(directory_path)
#     print(f"Directory '{directory_path}' created.")
# else:
#     print(f"Directory '{directory_path}' already exists.")

directory_path = f"docs/{project_id}/html"

# Check if the directory already exists
if not os.path.exists(directory_path):
    # If it doesn't exist, create the directory
    os.makedirs(directory_path)
    print(f"Directory '{directory_path}' created.")
else:
    print(f"Directory '{directory_path}' already exists.")