import unittest

from textnode import (
    TextNode,
     text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("this is a txt node", "italic", None)
        node2 = TextNode("this is a text node", "bold", "https://abc.com")
        self.assertNotEqual(node, node2)
    def test_eq_two(self):
        node = TextNode("Name", "italic", None)
        node2 = TextNode("Name", "italic", None)
        self.assertEqual(node, node2)
        

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_one_italic(self):
        node = TextNode("This is *italic* right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*")
        self.assertListEqual(new_nodes, [TextNode("This is ", text_type_text), TextNode("italic", text_type_italic), TextNode(" right?", text_type_text)])

    def test_one_code(self):
        node = TextNode("This is `code` right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`")
        self.assertListEqual(new_nodes, [TextNode("This is ", text_type_text), TextNode("code", text_type_code), TextNode(" right?", text_type_text)])
    
    
    def test_one_bold(self):
        node = TextNode("This is **bold** right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertListEqual(new_nodes, [TextNode("This is ", text_type_text), TextNode("bold", text_type_bold), TextNode(" right?", text_type_text)])
    
    
class Testextract_markdown_images(unittest.TestCase):
    def test_one(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image = extract_markdown_images(text)
        result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(image, result)
    def test_two(self):
        text = "This is text with no image"
        image = extract_markdown_images(text)
        result = []
        self.assertEqual(image, result)

class Testextract_markfown_links(unittest.TestCase):
    def test_one(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        image = extract_markdown_links(text)
        result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(image, result)

class Testsplit_nodes_image(unittest.TestCase):
    def test_one(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("This is text with a link ", text_type_text), TextNode("to boot dev", text_type_link, "https://www.boot.dev"), TextNode(" and ", text_type_text), TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev")])

class TestTexttoTextNodes(unittest.TestCase):
    def test_one(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = [
    TextNode("This is ", text_type_text),
    TextNode("text", text_type_bold),
    TextNode(" with an ", text_type_text),
    TextNode("italic", text_type_italic),
    TextNode(" word and a ", text_type_text),
    TextNode("code block", text_type_code),
    TextNode(" and an ", text_type_text),
    TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", text_type_text),
    TextNode("link", text_type_link, "https://boot.dev"),
]
        test = text_to_textnodes(text)
        self.assertListEqual(test, output)

class TestSplitBlocks(unittest.TestCase):
    def test_one(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        block_test = markdown_to_blocks(text)
        result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", """* This is the first list item in a list block
* This is a list item
* This is another list item"""]
        self.assertListEqual(block_test, result)
    def test_two(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

This is another Paragraphh with bad spellink!"""

        block_test = markdown_to_blocks(text)
        result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", """* This is the first list item in a list block
* This is a list item
* This is another list item""", "This is another Paragraphh with bad spellink!"]
        self.assertListEqual(block_test, result)
    def test_three(self):
        text = """# This is a heading

                  This is a paragraph of text. It has some **bold** and *italic* words inside of it.        

* This is the first list item in a list block
* This is a list item
* This is another list item

This is another Paragraphh with bad spellink!"""

        block_test = markdown_to_blocks(text)
        result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", """* This is the first list item in a list block\n* This is a list item\n* This is another list item""", "This is another Paragraphh with bad spellink!"]
        self.assertListEqual(block_test, result)

class TestBlockTypes(unittest.TestCase):
    def test_one(self):
        block = "### This is a header"
        block_test = block_to_block_type(block)
        result = "heading"
        self.assertEqual(block_test, result)
    def test_two(self):
        block = "```This is a code block```"
        block_test = block_to_block_type(block)
        result = "code"
        self.assertEqual(block_test, result)
    def test_three(self):
        block = ">This is a quote\n>This is second quoteline"
        block_test = block_to_block_type(block)
        result = "quote"
        self.assertEqual(block_test, result)
    def test_four(self):
        block = "* This is a unordered list\n* This is second listline"
        block_test = block_to_block_type(block)
        result = "unordered_list"
        self.assertEqual(block_test, result)
    def test_five(self):
        block = "- This is a quote\n- This is second quoteline"
        block_test = block_to_block_type(block)
        result = "unordered_list"
        self.assertEqual(block_test, result)
    def test_six(self):
        block = "1. This is a unordered list\n2. This is second listline"
        block_test = block_to_block_type(block)
        result = "ordered_list"
        self.assertEqual(block_test, result)
    def test_seven(self):
        block = "This is just a paragraph this is second listline"
        block_test = block_to_block_type(block)
        result = "paragraph"
        self.assertEqual(block_test, result)

if __name__ == "__main__":
    unittest.main()