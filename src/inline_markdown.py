from textnode import TextNode, TextType

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

