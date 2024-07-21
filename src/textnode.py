text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case ("text_type_text"):
            return LeafNode()



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




