import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from util import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    
    def test_text_type_text(self):
        """Test conversion of TEXT type to LeafNode"""
        text_node = TextNode("Simple text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(value="Simple text")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_text_type_bold(self):
        """Test conversion of BOLD type to LeafNode with b tag"""
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="b", value="Bold text")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_text_type_italic(self):
        """Test conversion of ITALIC type to LeafNode with i tag"""
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="i", value="Italic text")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_text_type_code(self):
        """Test conversion of CODE type to LeafNode with code tag"""
        text_node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="code", value="print('Hello')")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_text_type_links(self):
        """Test conversion of LINKS type to LeafNode with a tag and href"""
        text_node = TextNode("Click here", TextType.LINKS, "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="a", value="Click here", props={"href": "https://www.example.com"})
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_text_type_images(self):
        """Test conversion of IMAGES type to LeafNode with img tag"""
        text_node = TextNode("Alt text", TextType.IMAGES, "https://www.example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="img", value="", props={"src": "https://www.example.com/image.jpg", "alt": "Alt text"})
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_empty_text(self):
        """Test with empty text"""
        text_node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(value="")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
    
    def test_empty_bold_text(self):
        """Test with empty bold text"""
        text_node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="b", value="")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
    
    def test_link_with_empty_text(self):
        """Test link with empty text but valid URL"""
        text_node = TextNode("", TextType.LINKS, "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="a", value="", props={"href": "https://www.example.com"})
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_image_with_empty_alt(self):
        """Test image with empty alt text"""
        text_node = TextNode("", TextType.IMAGES, "https://www.example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="img", value="", props={"src": "https://www.example.com/image.jpg", "alt": ""})
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)
    
    def test_special_characters(self):
        """Test with special characters"""
        text_node = TextNode("Special chars: <>&\"'", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(value="Special chars: <>&\"'")
        self.assertEqual(html_node.value, expected.value)
    
    def test_unicode_characters(self):
        """Test with unicode characters"""
        text_node = TextNode("Unicode: 🚀 émojis ñ", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        expected = LeafNode(tag="b", value="Unicode: 🚀 émojis ñ")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
    
    def test_invalid_text_type_raises_exception(self):
        """Test that an invalid text type raises an exception"""
        # Asumiendo que existe un tipo inválido o None
        with self.assertRaises(Exception) as context:
            # Esto depende de cómo esté implementado TextType
            # Puedes crear un TextNode con un tipo que no existe
            text_node = TextNode("Invalid", None)  # o algún valor inválido
            text_node_to_html_node(text_node)
        
        self.assertEqual(str(context.exception), "Type needed")
    
    def test_return_type_is_leafnode(self):
        """Test that the function returns a LeafNode instance"""
        text_node = TextNode("Test", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
    
    def test_multiple_conversions_consistency(self):
        """Test that multiple conversions of the same node produce consistent results"""
        text_node = TextNode("Consistent test", TextType.ITALIC)
        html_node1 = text_node_to_html_node(text_node)
        html_node2 = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node1.tag, html_node2.tag)
        self.assertEqual(html_node1.value, html_node2.value)
        self.assertEqual(html_node1.props, html_node2.props)


if __name__ == "__main__":
    unittest.main()