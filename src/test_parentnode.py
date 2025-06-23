import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_single_child(self):
        child_node = LeafNode("p", "Hello")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html() ,"<div><p>Hello</p></div>")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First")
        child2 = LeafNode("p", "Second")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><p>First</p><p>Second</p></div>")

    def test_to_html_with_props(self):
        child = LeafNode("span", "Test")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><span>Test</span></div>')

    def test_to_html_nested_with_props(self):
        grandchild = LeafNode("em", "deep")
        child = ParentNode("p", [grandchild], {"style": "color:red;"})
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), '<section><p style="color:red;"><em>deep</em></p></section>')

    def test_to_html_raises_error_without_tag(self):
        try:
            ParentNode(None, [LeafNode("p", "text")]).to_html()
        except ValueError as e:
            self.assertEqual(str(e), "Need tag.")

    def test_to_html_raises_error_without_children(self):
        try:
            ParentNode("div", None).to_html()
        except ValueError as e:
            self.assertEqual(str(e), "Need children")

if __name__ == "__main__":
    unittest.main()