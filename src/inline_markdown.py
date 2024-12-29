from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
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
    description_images_tuple_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)    

    return description_images_tuple_list

def extract_markdown_links(text):
    description_link_tuple_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return description_link_tuple_list



def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
    
    
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
        
def markdown_to_blocks(markdown):

    block_list = markdown.split("\n\n")
    formatted_block_list = []
    
    for block in block_list:
        if block != "":
            lines = block.strip().split("\n")
            trimmed_lines = [line.strip() for line in lines]
            formatted_block = "\n".join(trimmed_lines)
            formatted_block_list.append(formatted_block)
    
    return formatted_block_list

def block_to_block_type(block):
    
    if re.match(r"^#{1,6} ", block):
        return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    lines = block.split("\n")
    
    quote_checker = []
    unordered_list_checker = []
    ordered_list_checker = []
     
    for line in lines:
        line.strip()
        if line.startswith(">"):
            quote_checker.append(True)
        else:
            quote_checker.append(False)
    
    for line in lines:
        line.strip()
        if line.startswith("-") or line.startswith("*"):
            unordered_list_checker.append(True)
        else:
            unordered_list_checker.append(False)
        
    for i in range(len(lines)):
        if lines[i].strip().startswith(f"{i+1}. "):
            ordered_list_checker.append(True)
        else:
            ordered_list_checker.append(False)
    
    if all(quote_checker):
        return "quote"
    elif all(unordered_list_checker):
        return "unordered_list"
    elif all(ordered_list_checker):
        return "ordered_list"
    
    return "paragraph"
        
    
    
         