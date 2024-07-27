from textnode import (TextNode, markdown_to_blocks, block_to_block_type, text_to_textnodes, text_node_to_html_node)
from htmlnode import (HTMLNode, ParentNode, LeafNode)


def block_type_to_tag(block_type, block):
    match(block_type):
        case ("heading"):
            heading_dict = {"# ": "h1", "## ": "h2", "### ": "h3", "#### ": "h4", "##### ": "h5", "###### ": "h6"}
            for header in heading_dict:
                if block.startswith(header):
                    return heading_dict[header], block.lstrip(header)
            raise Exception("Invalid Markdown: Wrong Header format")
        case ("code"):
            return "code", block.strip("```")
        case ("quote"):
            return "blockquote", block.replace(">", "").strip()
        case ("unordered_list"):
            if block.startswith("- "):
                return "ul", block.replace("- ", "")
            if block.startswith("* "):
                return "ul", block.replace("* ", "")
        case ("ordered_list"):
            split_block = block.split("\n")   
            for i in range(0, len(split_block)):
                split_block[i] = split_block[i].replace(f"{i+1}. ", "")
            new_block = "\n".join(split_block)
            return "ol", new_block
        case ("paragraph"):
            return "p", block
        case _:
            raise ValueError("Invalid block_type")
        
def markdown_to_html(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    Content_Node = ParentNode("div", [], None)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        block_tag, new_block = block_type_to_tag(block_type, block)
        if block_type == "unordered_list" or block_type == "ordered_list":
            new_block = new_block.split("\n")
            new_list = []
            for block_part in new_block:
                new_list.append(ParentNode("li", list(map(lambda x: text_node_to_html_node(x),(text_to_textnodes(block_part))))))
            leaf_nodes = new_list
        else:
            Text_nodes = text_to_textnodes(new_block)
            leaf_nodes = list(map(lambda x: text_node_to_html_node(x), Text_nodes))
        block_node = ParentNode(block_tag, leaf_nodes, None)
        Content_Node.children.append(block_node)
    return Content_Node