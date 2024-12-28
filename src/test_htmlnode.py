import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
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
    
    def test_to_html_no_children(self): #leaf node
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self): # leaf node
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")





if __name__ == "__main__":
    unittest.main()