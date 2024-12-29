from textnode import TextType, TextNode
from htmlnode import LeafNode
    
def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case (TextType.TEXT):
            return LeafNode(tag=None, value=text_node.text)
            
        case (TextType.BOLD):
            return LeafNode(tag="b", value=text_node.text)
            
        case (TextType.ITALIC):
            return LeafNode(tag="i", value=text_node.text)
            
        case (TextType.CODE):
            return LeafNode(tag="code", value=text_node.text)
        
        case (TextType.LINK):
            return LeafNode(tag="a", value=text_node.text, props={"href": f"{text_node.url}"})
            
        case (TextType.IMAGE):
            return LeafNode(tag="img", value="", props={"src": f"{text_node.text}",
                                                    "alt": f"{text_node.url}"})
        case _:
            raise Exception("Invalid Text Type")