from textnode import (TextNode, split_nodes_delimiter)
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

def main():
    nodes = TextNode("This is **bold bold bold** Text", "text")
    nodes2 = TextNode("**bold bold** Text", "text")
    
main()
