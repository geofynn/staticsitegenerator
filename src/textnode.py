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
        if self.text == second_node.text and self.text_type == second_node.text_type and self.url == second_node.url:
            return True
        return False
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
            if delimiter in node.text:
                split_string = node.text.split(delimiter)
                split_string = list(filter(None, split_string))
                if len(split_string) == 3:
                    split_nodes.extend([TextNode(split_string[0], text_type_text), TextNode(split_string[1], delimiter_type_dict[delimiter]), TextNode(split_string[2], text_type_text)])
                elif len(split_string) == 2:
                    if delimiter in node.text[:2]:
                        split_nodes.extend([TextNode(split_string[0], delimiter_type_dict[delimiter]), TextNode(split_string[1], text_type_text)],)
                    elif delimiter in node.text[:-2]:
                        split_nodes.extend([TextNode(split_string[0], text_type_text), TextNode(split_string[1], delimiter_type_dict[delimiter])],)
                    else:
                        raise Exception("Delimiter not at start or end")
                elif len(split_string) > 3:
                    raise Exception("Multinested not testet yet")
            else:
                raise Exception("Delimiter is not in Text")
    return split_nodes







