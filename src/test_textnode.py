import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_none_url(self):
        node = TextNode("None url node", TextType.ITALIC, None)
        node2 = TextNode("None url node", TextType.ITALIC, None)
        self.assertEqual(node, node2)
        
    def test_same_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)
        
    def test_same_text_diff_type(self):
        node = TextNode("Italic text node", TextType.ITALIC)
        node2 = TextNode("Bold text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
