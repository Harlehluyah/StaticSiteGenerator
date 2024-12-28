from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(list(map(lambda kv: f"{kv[0]}=\"{kv[1]}\"" ,self.props.items())))

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n)"

 
class LeafNode(HTMLNode): # techincally void_elements like img are self closing, dont need </img> at end but solution files have them so we follow
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid Tag: no value")
        if self.children is None:
            raise ValueError("Invalid Children: no children")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        return html + f"</{self.tag}>"
    
#   ----- Helper Functions --------------------------------------------------

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
        
        
        
            
        
            