from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from markdown_blocks import markdown_to_html_node, extract_title
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    mkdn: str = open(from_path).read()
    temp: str = open(template_path).read()
    html: str = markdown_to_html_node(mkdn).to_html()
    title: str = extract_title(mkdn)
    new_temp: str = temp.replace("{{ Title  }}", title)
    new_temp = new_temp.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_temp)



def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)
    # main page
    generate_page("content/index.md", "template.html", "public/index.html")
    # glorfindel
    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    # majesty
    generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    # tom
    generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    # contact
    generate_page("content/contact/index.md", "template.html", "public/contact/index.html")

if __name__ == "__main__":
    main()