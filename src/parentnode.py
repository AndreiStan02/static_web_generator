from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None: raise ValueError("Need tag.")
        if self.children == None: raise ValueError("Need children")

        string = f"<{self.tag}"
        string_props = self.props_to_html()
        if string_props:
            string += f' {string_props}'
        string += ">"

        string += "".join(child.to_html() for child in self.children)

        string += f"</{self.tag}>"

        return string