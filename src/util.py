import re

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

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    res = re.findall(pattern, text)
    return res

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    res = re.findall(pattern, text)
    return res

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        split_nodes = []
        images = extract_markdown_images(old_node.text)
        current_text = old_node.text
        for image in images:
            sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
            current_text = sections[1]
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.IMAGES, image[1]))
        if current_text != "":
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        split_nodes = []
        links = extract_markdown_links(old_node.text)
        current_text = old_node.text
        for image in links:
            sections = current_text.split(f"[{image[0]}]({image[1]})", 1)
            current_text = sections[1]
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.LINKS, image[1]))
        if current_text != "":
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks



