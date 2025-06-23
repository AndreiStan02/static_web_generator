class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        string = ' '.join(f'{k}="{v}"' for k, v in self.props.items())        
        return string
    
    def __repr__(self):
        return f"Tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"