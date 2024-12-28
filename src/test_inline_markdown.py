import unittest
from inline_markdown import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    
#   ----- Split_node_delimiter Tests -------------------------------------------------------
    
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

#   ----- extract_markdown_images(text) Tests ----------------------------------------------------

    def test_single_image(self):
        text = "![alt text](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image.jpg")])
    
    def test_no_image(self):
        text = "Plain text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
    
    def test_multiple_images(self):
        text = "![cat](cat.jpg) ![dog](dog.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("cat", "cat.jpg"), ("dog", "dog.jpg")])
        
    def test_image_with_spaces(self):
        text = "![my cool cat](https://example.com/cool%20cat.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("my cool cat", "https://example.com/cool%20cat.jpg")])
    
    def test_mixed_content(self):
        text = "Some text ![image](img.jpg) more text ![another](pic.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "img.jpg"), ("another", "pic.png")])
        

#   ----- extract_markdown_links(text) Tests ------------------------------------------------

    def test_single_link(self):
        text = "[Boot.dev](https://boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Boot.dev", "https://boot.dev")])
    
    def test_no_links(self):
        text = "Plain text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_multiple_links(self):
        text = "Check out [Boot.dev](https://boot.dev) and [Python](https://python.org)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Boot.dev", "https://boot.dev"), ("Python", "https://python.org")])
        
    def test_ignore_images(self):
        text = "[link](https://boot.dev) ![image](pic.jpg)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://boot.dev")])
        
        
        

if __name__ == "__main__":
    unittest.main()