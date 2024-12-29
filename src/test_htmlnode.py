import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from converter import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    
#   ----- HTMLNode Tests ----------------------------------------------------------------------------

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        
        self.assertEqual(result, expected, f"Expected: {expected}, but got: {result}")
    
    def test_empty_props(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        expected = ""
        self.assertEqual(result, expected, f"Expected: {expected}, but got: {result}")
    
    def test_nested_children(self):
        child_node1 = HTMLNode(tag="span", value="child1")
        child_node2 = HTMLNode(tag="span", value="child2")
        parent_node = HTMLNode(tag="div", children=[child_node1, child_node2])
        
        self.assertEqual(len(parent_node.children), 2, "Expected two child nodes.")
        self.assertEqual(parent_node.children[0].value, "child1", "Expected first child node value to be 'child1'.")
        self.assertEqual(parent_node.children[1].value, "child2", "Expected second child node value to be 'child2'.")
    
    def test_missing_props(self):
        node = HTMLNode(tag="p", value="This is a paragraph.")
        result = node.props_to_html()
        expected = ''
        self.assertEqual(result, expected, "Expected an empty string when props is not set.")

#   ----- LeafNode Tests -------------------------------------------------------------------------

    def test_to_html_no_children(self): 
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self): 
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
#   ----- ParentNode Tests -----------------------------------------------------------------------
        
    def test_to_html_one_children(self): 
        parent = ParentNode("div", [LeafNode("p", "text")])
        self.assertEqual(parent.to_html(), "<div><p>text</p></div>")
    
    def test_to_html_nested_parent(self): 
        nestedParent = ParentNode("div", [
            ParentNode("p", [LeafNode("span", "text")])
        ])
        self.assertEqual(nestedParent.to_html(), "<div><p><span>text</span></p></div>")
    
    def test_to_html_with_props(self):
        parent = ParentNode("div", [LeafNode("p", "text")], {"class": "container"})
        self.assertEqual(parent.to_html(), "<div class=\"container\"><p>text</p></div>")
        
    def test_to_html_multiple_children(self):
        parent = ParentNode(
            "div",
            [
                LeafNode("p", "first"),
                LeafNode("p", "second"),
                LeafNode("p", "third")
            ]
        )
        self.assertEqual(parent.to_html(), "<div><p>first</p><p>second</p><p>third</p></div>")

#   ----- text_node_to_html_node Helper Function Tests -----------------------------------------

    def test_text_to_html(self):
        text_node = TextNode("text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "text")
    
    def test_bold_to_html(self):
        bold_text_node = TextNode("text", TextType.BOLD)
        html_node = text_node_to_html_node(bold_text_node)
        self.assertEqual(html_node.to_html(), "<b>text</b>")
        
    def test_italic_to_html(self):
        italic_text_node = TextNode("text", TextType.ITALIC)
        html_node = text_node_to_html_node(italic_text_node)
        self.assertEqual(html_node.to_html(), "<i>text</i>")
    
    def test_code_to_html(self):
        code_text_node = TextNode("text", TextType.CODE)
        html_node = text_node_to_html_node(code_text_node)
        self.assertEqual(html_node.to_html(), "<code>text</code>")
    
    def test_link_to_html(self):
        link_node = TextNode("Click here", TextType.LINK, "http://boot.dev")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.to_html(), "<a href=\"http://boot.dev\">Click here</a>")
    
    def test_image_to_html(self):
        image_node = TextNode("puppy.jpg", TextType.IMAGE, "A cute puppy")
        html_node = text_node_to_html_node(image_node)
        self.assertEqual(html_node.to_html(), "<img src=\"puppy.jpg\" alt=\"A cute puppy\"></img>") # ATTENTION! </img> is not HTML5 standard but this test needs it   
        





if __name__ == "__main__":
    unittest.main()