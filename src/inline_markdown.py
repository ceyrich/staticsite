from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    ret_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
        new_nodes = []
        node_texts = node.text.split(delimiter)
        if len(node_texts) % 2 == 0:
            raise Exception("Invalid markdown syntax, formatted section not closed")
        count = 0
        for text in node_texts:
            count += 1
            if text == "":
                continue
            if count & 1 != 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
            
        ret_nodes.extend(new_nodes)
    return ret_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    ret_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) <= 0:
            ret_nodes.append(node)
            continue
        for image in images:
            split_text = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_text[0] != "":
                ret_nodes.append(TextNode(split_text[0], TextType.TEXT))
            ret_nodes.append(
                TextNode(image[0], TextType.IMAGE, image[1]),
            )
            original_text = split_text[1]
        if original_text != "":
            ret_nodes.append(TextNode(original_text, TextType.TEXT))            
    return ret_nodes

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    ret_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) <= 0:
            ret_nodes.append(node)
            continue
        for link in links:
            split_text = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split_text[0] != "":
                ret_nodes.append(TextNode(split_text[0], TextType.TEXT))
            ret_nodes.append(
                TextNode(link[0], TextType.LINK, link[1]),
            )
            original_text = split_text[1]
        if original_text != "":
            ret_nodes.append(TextNode(original_text, TextType.TEXT))            
    return ret_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
