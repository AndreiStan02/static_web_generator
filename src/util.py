from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type :
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b" ,value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i" ,value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code" ,value=text_node.text)
        case TextType.LINKS:
            return LeafNode(tag="a" ,value=text_node.text ,props={"href":text_node.url})
        case TextType.IMAGES:
            return LeafNode(tag="img" ,value="" ,props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Type needed")
                
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes