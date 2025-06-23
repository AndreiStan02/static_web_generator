from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None: raise ValueError("All leaf nodes must have a value")
        string = ""
        if self.tag is not None:
            string += f"<{self.tag}"
            string_props = self.props_to_html()
            if string_props:
                string += f' {string_props}'
            string += ">"
        
        string += self.value

        if self.tag is not None:
            string += f"</{self.tag}>"
        
        return string