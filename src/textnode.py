import re

from htmlnode import LeafNode
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"



class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, second_node):
        return (
            self.text_type == second_node.text_type
            and self.text == second_node.text
            and self.url == second_node.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case ("text"):
            return LeafNode(None, text_node.text)
        case ("bold"):
            return LeafNode("b", text_node.text)
        case ("italic"):
            return LeafNode("i", text_node.text)
        case ("code"):
            return LeafNode("code", text_node.text)
        case ("link"):
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case("image"):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter):
    delimiter_type_dict = {"*": text_type_italic, "**": text_type_bold, "`": text_type_code}
    split_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            split_nodes.append(node)
        else:
            split_string = node.text.split(delimiter)
            temp_nodes = []
            if len(split_string) % 2 == 0:
                raise ValueError("Invalid Markdown: delimiter not closed")
            for i in range(len(split_string)):
                if split_string[i] == "":
                    continue
                if i % 2 == 0:
                    temp_nodes.append(TextNode(split_string[i], text_type_text))
                else:
                    temp_nodes.append(TextNode(split_string[i], delimiter_type_dict[delimiter]))
            split_nodes.extend(temp_nodes)
    return split_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
     return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_tuple = extract_markdown_images(node.text)
        if link_tuple == []:
            new_nodes.append(node)
        else:
            temp_list = []
            split_node = []
            for link in link_tuple:
                if split_node == []:
                    split_node = node.text.split(f"![{link[0]}]({link[1]})", 1)
                else:
                    split_node = "".join(split_node).split(f"![{link[0]}]({link[1]})", 1)
                if len(split_node) != 2:
                    raise ValueError("Invalid Markdown: image section not closed")
                split_node = list(filter(None, split_node))
                temp_list.append(TextNode(split_node[0], text_type_text))
                temp_list.append(TextNode(link[0], text_type_image, link[1]))
                split_node.remove(split_node[0])
            new_nodes.extend(temp_list)
            if len(split_node) != 0:
                new_nodes.append(TextNode(split_node[0], text_type_text))
    return list(new_nodes)


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        link_tuple = extract_markdown_links(node.text)
        if link_tuple == []:
            new_nodes.append(node)
        else:
            temp_list = []
            split_node = []
            for link in link_tuple:
                if split_node == []:
                    split_node = node.text.split(f"[{link[0]}]({link[1]})", 1)
                else:
                    split_node = "".join(split_node).split(f"[{link[0]}]({link[1]})", 1)
                if len(split_node) != 2:
                    raise ValueError("Invalid Markdown: link section not closed")
                split_node = list(filter(None, split_node))
                temp_list.append(TextNode(split_node[0], text_type_text))
                temp_list.append(TextNode(link[0], text_type_link, link[1]))
                split_node.remove(split_node[0])
            new_nodes.extend(temp_list)
            if len(split_node) != 0:
                new_nodes.append(TextNode(split_node[0], text_type_text))
    return list(new_nodes)

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text, None)]
    #node_to_split = TextNode(text, text_type_text, None)
    nodes = split_nodes_delimiter(nodes, "**")
    nodes = split_nodes_delimiter(nodes, "*")
    nodes = split_nodes_delimiter(nodes, "`")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    split_string = markdown.split("\n\n")
    return list(map(lambda x: x.strip(), filter(None, split_string)))

def block_to_block_type(block):
    if (block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### ")):
        return "heading"
    elif block[0:3] == "```" and block[-3:] == "```":
        return "code"
    else:
        type_dict = {">": "quote", "* ": "unordered_list", "- ": "unordered_list"}
        split_block = block.split("\n")
        for block_type in type_dict:
            split_block_check = list(filter(lambda x: block_type in x[0:2], split_block))
            if len(split_block) == len(split_block_check):
                return type_dict[block_type]
        if split_block[0][0:3] == "1. ":
            for i in range(0, len(split_block)):
                if split_block[i][0:3] == f"{i+1}. ":
                    check = True
                else:
                    check = False
            if check:
                return "ordered_list"
            else:
                raise ValueError("Invalid Markdown: Not a correct ordered list")
        else:
            return "paragraph"

