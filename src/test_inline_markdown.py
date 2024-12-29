import unittest
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes
    )

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
        
#   ----- split_node_image Tests ----------------------------------------------------------------

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

#   ----- split_node_link Tests -----------------------------------------------------------------
        
    def test_split_links(self):
        node = TextNode(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        TextType.TEXT,
    )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
            TextNode(" with text that follows", TextType.TEXT),
        ],
        new_nodes,
)
        
#   ----- text_to_textnodes Test ------------------------------------------------------------------

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
        

if __name__ == "__main__":
    unittest.main()