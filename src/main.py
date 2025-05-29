from textnode import *
from htmlnode import *
import os, shutil, pathlib, sys
from block_markdown import *

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        lines = block.split("\n")
        for line in lines:
            if(line.startswith("# ")):
                return line[2:]
    raise Exception("Error: no h1 header")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    title = extract_title(markdown)  
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    result = template.replace("{{ Title }}", title, 1)
    result = result.replace("{{ Content }}", content, 1)
    result = result.replace('href="/',f'href="{basepath}')
    result = result.replace('src="/',f'src="{basepath}')
    with open(dest_path, "w") as file:
        file.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_list = os.listdir(dir_path_content)
    if not content_list:
        return
    
    for file in content_list:
        if (os.path.isfile(os.path.join(dir_path_content, file)) and file.endswith(".md")):
            html_file_path = file.replace(".md", ".html")
            pathlib.Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, html_file_path), basepath)
        elif(os.path.isfile(os.path.join(dir_path_content, file)) and file.endswith(".css")):
            pathlib.Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
            file_path = os.path.join(dir_path_content, file)
            file_dest = os.path.join(dest_dir_path, file)
            shutil.copy(file_path, file_dest)
        else:
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file), basepath)

def main():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
        os.mkdir("docs")
        docs_dir = "docs"
        source_dir = "static"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
   
    copy_files_recursive(source_dir, docs_dir)
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()