import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank",})
        props_val =  " href=\"https://www.google.com\" target=\"_blank\""
        test_props = node.props_to_html()
        self.assertEqual(test_props, props_val)
        
class TestLeafNode(unittest.TestCase):
    def test_one(self):
        node = LeafNode(None, "HEllo world")
        self.assertEqual(node.to_html(), "HEllo world")
    def test_two(self):
        node = LeafNode("a", None)
        with self.assertRaisesRegex(ValueError, ''):
            node.to_html() 
    def test_three(self):
        node = LeafNode("a", "Paragraph", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Paragraph</a>")

class TestParentNode(unittest.TestCase):
    def test_ValErr_one(self):
        node = ParentNode(None,  [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),])
        with self.assertRaisesRegex(ValueError, ''):
            node.to_html()
    def test_ValErr_two(self):
        node = ParentNode("a", None)
        with self.assertRaisesRegex(ValueError, ''):
            node.to_html()
    def test_one(self):
        node = ParentNode("a", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),])
        self.assertEqual(node.to_html(), "<a><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>")

    def test_two(self):
        node = ParentNode("a", [
        LeafNode("b", "Bold text"),
        ParentNode("s", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),]),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),])
        self.assertEqual(node.to_html(), "<a><b>Bold text</b><s><b>Bold text</b>Normal text<i>italic text</i>Normal text</s>Normal text<i>italic text</i>Normal text</a>")
    def test_three(self):
        node = ParentNode("a", [
        LeafNode("b", "Bold text"),
        ParentNode("s", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),]),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),], {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\"><b>Bold text</b><s><b>Bold text</b>Normal text<i>italic text</i>Normal text</s>Normal text<i>italic text</i>Normal text</a>")

if __name__ == "__main__":
    unittest.main()