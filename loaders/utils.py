import os
import yaml
def createDirectoryIfNotPresnt(directory):
    if not os.path.exists(directory):
        print(f"{directory} not present and creating")
        os.mkdir(directory)
    else:
        print(f"{directory} present ")

def create_markdown_file(directory, filename, result):

    # Create directory if it does not exist
    os.makedirs(directory, exist_ok=True)

    # Combine directory and filename
    file_path = os.path.join(directory, filename)

    metadata = {
        "title": result.metadata.get("title"),
        "url": result.url,
        "description": result.metadata.get("description"),
        "depth": result.metadata.get("depth"),
        "parent_url": result.metadata.get("parent_url")
        }




    # Create file and write markdown content
    with open(file_path, "w", encoding="utf-8") as file:

        file.write("\n------\n")
        yaml.dump(metadata,file,default_flow_style=False)
        file.write("\n------\n")
        file.write(result.markdown)

    print("Markdown file created:", file_path)   
