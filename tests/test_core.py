import pathlib
from cobertura_parser import CoberturaParser


cobertura_xml = pathlib.Path(__file__).parent / "data" / "cobertura.xml"

with open(cobertura_xml) as f:
    cobertura_content = f.read()


def test_read():
    c = CoberturaParser.from_file(cobertura_xml)
    assert isinstance(c, CoberturaParser)
    assert c._raw


def test_get_data():
    c = CoberturaParser.from_str(cobertura_content)
    assert c.get_data()


def test_tree_package():
    c = CoberturaParser.from_str(cobertura_content)
    for each in c.get_package_trees():
        assert each.root.__dict__


def test_tree_class():
    c = CoberturaParser.from_str(cobertura_content)
    for each in c.get_class_trees():
        assert each.root.__dict__


def test_tree_method():
    c = CoberturaParser.from_str(cobertura_content)
    for each in c.get_class_trees():
        assert each.root.__dict__


def test_tree():
    c = CoberturaParser.from_str(cobertura_content)
    assert c.tree
    packages = c.get_package_trees()
    for each_package in packages:
        for each_classes in c.get_class_trees(each_package):
            for each_methods in c.get_method_trees(each_classes):
                assert each_methods.root.__dict__
                assert each_methods.root


def test_get_node_info():
    c = CoberturaParser.from_str(cobertura_content)
    assert c.tree
    packages = c.get_package_trees()
    for each_package in packages:
        name = c.get_node_attr(each_package.root, "name")
        assert name is not None
