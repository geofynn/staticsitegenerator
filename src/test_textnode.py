import unittest

from textnode import TextNode


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
        
if __name__ == "__main__":
    unittest.main()