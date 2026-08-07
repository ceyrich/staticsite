import sys

from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from markdown_blocks import markdown_to_html_node, extract_title
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./docs"

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    mkdn: str = open(from_path).read()
    temp: str = open(template_path).read()
    html: str = markdown_to_html_node(mkdn).to_html()
    title: str = extract_title(mkdn)
    new_temp: str = temp.replace("{{ Title }}", title)
    new_temp = new_temp.replace("{{ Content }}", html)
    new_temp = new_temp.replace('href="/', f'href="{basepath}')
    new_temp = new_temp.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_temp)

def generate_page_recursive(from_path: str, template_path: str, dest_path: str, basepath: str):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for filename in os.listdir(from_path):
        f = os.path.join(from_path, filename)
        t = os.path.join(dest_path, filename.replace(".md", ".html"))
        if os.path.isfile(f):
            generate_page(f, template_path, t, basepath)
        else:
            generate_page_recursive(f, template_path, t, basepath)

    return

def main():
    basepath: str = "/"
    if len(sys.argv) > 1 and sys.argv[1] is not None:
        basepath = sys.argv[1]
    print(basepath)
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)
    generate_page_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()