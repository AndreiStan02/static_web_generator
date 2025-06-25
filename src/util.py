import re, os, shutil

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode
from block import block_to_block_type, BlockType

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
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) < 2:
            new_nodes.append(node)
            continue

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
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
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

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
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
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
    text = text.replace("\n", "")
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

def format_block(text, block_type):
    if block_type == BlockType.HEADING:
        # Quita de 1 a 6 # al inicio + espacio
        return re.sub(r"^#{1,6}\s+", "", text.strip())

    elif block_type == BlockType.CODE:
        code = re.sub(r"^```|```$", "", text.strip())
        code = re.sub(r"^\s+", "", code, flags=re.MULTILINE)  # quita indentaciones por línea
        return code

    elif block_type == BlockType.QUOTE:
        # Quita > al inicio de cada línea
        return re.sub(r"^>\s?", "", text, flags=re.MULTILINE)

    elif block_type == BlockType.UNORDERED_LIST:
        # Quita - y espacio al inicio de cada línea
        return re.sub(r"^-\s+", "", text, flags=re.MULTILINE)

    elif block_type == BlockType.ORDERED_LIST:
        # Quita números secuenciales (1. , 2. , ...) al inicio
        return re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

    elif block_type == BlockType.PARAGRAPH:
        # Texto plano, se devuelve tal cual (opcional: strip)
        return " ".join(line.strip() for line in text.strip().splitlines())


    else:
        raise ValueError("no type")
            


def text_to_children(text, block_type):
    res = []
    aux_text = format_block(text, block_type)
    aux_text = re.sub(r"\s+", " ", aux_text.strip())  # Normalización aquí
    textnodes = text_to_textnodes(aux_text)
    for node in textnodes:
        res.append(text_node_to_html_node(node))
    return res

def markdown_to_html_node(markdown):
    res = []
    splited_markdown = markdown_to_blocks(markdown)
    for block in splited_markdown:
        block_type = block_to_block_type(block)
        children = text_to_children(block, block_type)
        if block_type == BlockType.PARAGRAPH:
            if not children or all(
                isinstance(child, LeafNode) and not child.value.strip()
                for child in children
            ):
                continue

            # En caso contrario, crea un <p> con los children
            html_node = ParentNode(tag="p", children=children)
            res.append(html_node)
        elif block_type == BlockType.QUOTE: 
            if len(children) != 0:
                html_node = ParentNode(tag="blockquote", children=children)
                res.append(html_node)
            else:
                html_node = LeafNode(tag="blockquote", value=block)
                res.append(html_node)
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            elements = []
            for line in lines:
                children = text_to_children(line[2:], BlockType.UNORDERED_LIST)
                if len(children) != 0:
                    elements.append(ParentNode(tag="li", children= children))
                else:
                    elements.append(ParentNode(tag="li", value=line[2:]))
            parentNode = ParentNode(tag="ul", children=elements)
            res.append(parentNode)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            elements = []
            for line in lines:
                children = text_to_children(line[2:], BlockType.UNORDERED_LIST)
                if len(children) != 0:
                    elements.append(ParentNode(tag="li", children= children))
                else:
                    elements.append(ParentNode(tag="li", value=line[2:]))
            parentNode = ParentNode(tag="ol", children=elements)
            res.append(parentNode)
        elif block_type == BlockType.CODE:
            html_node = LeafNode(tag="code", value=format_block(block, block_type))
            parentNode = ParentNode(tag="pre", children=[html_node])
            res.append(parentNode)
        elif block_type == BlockType.HEADING:
            hashes = re.match(r"#*", block).group()
            level = len(hashes)
            tag = f"h{level}"
            
            if len(children) != 0:
                html_node = ParentNode(tag=tag, children=children)
                res.append(html_node)
            else:
                html_node = LeafNode(tag=tag, value=block)
                res.append(html_node)
    return ParentNode(tag="div", children=res)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if re.match(r"^# ", line):
            return line[2:].strip()
    raise Exception("no header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file_from = open(from_path)
    file_template = open(template_path)
    markdown = file_from.read()
    template = file_template.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    print(page)
    with open(dest_path, 'w') as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    print(files)
    for file_name in files:
        if not os.path.isfile(os.path.join(dir_path_content, file_name)):
            new_dest = os.path.join(dest_dir_path, file_name)
            os.mkdir(new_dest)
            generate_pages_recursive(os.path.join(dir_path_content, file_name), template_path, new_dest)
        else:
            generate_page(os.path.join(dir_path_content, file_name), template_path, os.path.join(dest_dir_path, "index.html"))

