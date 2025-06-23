import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        tag = "p"
        value = "the value"
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode(tag= tag, value=value, props=props)
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')
    
    def test_noteq(self):
        tag = "p"
        value = "the value"
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode(tag= tag, value=value, props=props)
        self.assertNotEqual(node.props_to_html(), 'href="https://www.google.com"')
    
    def test_eq2(self):
        props = {
            "href": "https://www.google.com",
        }

        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com"')


if __name__ == "__main__":
    unittest.main()