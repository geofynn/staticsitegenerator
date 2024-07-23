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
        self.assertEqual(new_nodes[0].text, "This is ")
    def test_two_italic(self):
        node = TextNode("This is *italic* right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*")
        self.assertEqual(new_nodes[1].text, "italic")
    def test_three_italic(self):
        node = TextNode("This is *italic* right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*")
        self.assertEqual(new_nodes[2].text, " right?")
    def test_four_italic(self):
        node = TextNode("*italic* This is right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*")
        self.assertEqual(new_nodes[0].text, "italic")
    def test_five_italic(self):
        node = TextNode("*italic* This is right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*")
        self.assertEqual(new_nodes[1].text, " This is right?")

    def test_one_code(self):
        node = TextNode("This is `code` right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`")
        self.assertEqual(new_nodes[0].text, "This is ")
    def test_two_code(self):
        node = TextNode("This is `code` right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`")
        self.assertEqual(new_nodes[1].text, "code")
    def test_three_code(self):
        node = TextNode("This is `code` right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`")
        self.assertEqual(new_nodes[2].text, " right?")
    
    def test_one_bold(self):
        node = TextNode("This is **code** right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes[0].text, "This is ")
    def test_two_bold(self):
        node = TextNode("This is **code** right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes[1].text, "code")
    def test_three_bold(self):
        node = TextNode("This is **code** right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes[2].text, " right?")
    def test_four_bold(self):
        node = TextNode("**code** This is right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes[0].text, "code")
    def test_five_bold(self):
        node = TextNode("**code** This is right?", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes[1].text, " This is right?")
    def test_six_bold(self):
        node = TextNode("This is right? **code**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes[0].text, "This is right? ")
    def test_seven_bold(self):
        node = TextNode("This is right? **code**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes[1].text, "code")
    def test_invalid(self):
        node = TextNode("This is right? **code", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertRaisesRegex(ValueError, "")


if __name__ == "__main__":
    unittest.main()