class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        str = ""
        for property in self.props:
            str += (f" {property}=\"{self.props[property]}\"")
        return str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.value = value

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, None, props)
        self.children = children
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        elif self.children is None:
            raise ValueError("Invalid HTML: needs children")
        else:
            html_string = ""
            for child in self.children:
                html_string += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"