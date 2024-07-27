import unittest
from htmlnode import (HTMLNode, ParentNode, LeafNode)
from markdown_to_html import markdown_to_html

class Testmarkdown_to_html(unittest.TestCase):
    def test_one(self):
        markdown_text = """### This is a heading

>This is a block_quote
>Second blockquote line
>Third Block Quote Line"""
        markdown_result = ParentNode("div", [ParentNode("h3", [LeafNode(None, "This is a heading")]), ParentNode("blockquote", [LeafNode(None, """This is a block_quote
Second blockquote line
Third Block Quote Line""")])])
        self.assertEqual(markdown_to_html(markdown_text).to_html(), markdown_result.to_html())
    def test_two(self):
        markdown_text = """### This is a heading

```This is a block_quote
Second blockquote line
Third Block Quote Line```"""
        markdown_result = ParentNode("div", [ParentNode("h3", [LeafNode(None, "This is a heading")]), ParentNode("code", [LeafNode(None, """This is a block_quote
Second blockquote line
Third Block Quote Line""")])])
        self.assertEqual(markdown_to_html(markdown_text).to_html(), markdown_result.to_html())
    def test_three(self):
        markdown_text = """### This is a heading

This is a block_quote
Second blockquote line
Third Block Quote Line"""
        markdown_result = ParentNode("div", [ParentNode("h3", [LeafNode(None, "This is a heading")]), ParentNode("p", [LeafNode(None, """This is a block_quote
Second blockquote line
Third Block Quote Line""")])])
        self.assertEqual(markdown_to_html(markdown_text).to_html(), markdown_result.to_html())
    def test_four(self):
        markdown_text = """### This is a heading

- Item 1
- Item 2
- Item 3"""
        markdown_result = ParentNode("div", [ParentNode("h3", [LeafNode(None, "This is a heading")]), ParentNode("ul", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2"), LeafNode("li", "Item 3")])])
        self.assertEqual(markdown_to_html(markdown_text).to_html(), markdown_result.to_html())
    def test_five(self):
        markdown_text = """### This is a heading

1. Item 1
2. Item 2
3. Item 3"""
        markdown_result = ParentNode("div", [ParentNode("h3", [LeafNode(None, "This is a heading")]), ParentNode("ol", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2"), LeafNode("li", "Item 3")])])
        self.assertEqual(markdown_to_html(markdown_text).to_html(), markdown_result.to_html())

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )
    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )