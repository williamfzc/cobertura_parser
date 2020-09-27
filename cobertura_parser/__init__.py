# MIT License
#
# Copyright (c) 2020 williamfzc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import xmltodict
import pathlib
import typing
from planter import Tree
from planter import Node
from planter import Compiler


class CoberturaParser(object):
    def __init__(self, content: str):
        self._raw = xmltodict.parse(content)

        # build tree
        c = Compiler()
        root = c.compile(self._raw)
        self.tree = Tree(root)

    @classmethod
    def from_file(cls, file_path: typing.Union[str, pathlib.Path]) -> "CoberturaParser":
        with open(file_path, encoding="utf-8") as f:
            return cls(f.read())

    @classmethod
    def from_str(cls, xml_content: str) -> "CoberturaParser":
        return cls(xml_content)

    def get_data(self) -> dict:
        return self._raw

    def get_package_nodes(self) -> typing.Iterable[Node]:
        return self.tree.get_nodes_by_name("package")

    def get_package_trees(self) -> typing.Iterable[Tree]:
        return [Tree(each) for each in self.get_package_nodes()]

    def get_class_nodes(self, package: Tree = None) -> typing.Iterable[Node]:
        tree = package or self.tree
        return tree.get_nodes_by_name("class")

    def get_class_trees(self, package: Tree = None) -> typing.Iterable[Tree]:
        return [Tree(each) for each in self.get_class_nodes(package)]

    def get_method_nodes(self, class_: Tree = None) -> typing.Iterable[Node]:
        tree = class_ or self.tree
        return tree.get_nodes_by_name("method")

    def get_method_trees(self, class_: Tree = None) -> typing.Iterable[Tree]:
        return [Tree(each) for each in self.get_method_nodes(class_)]

    def get_packages(self):
        return [self.get_node_attrs(each) for each in self.get_package_nodes()]

    def get_classes(self, package: Tree = None):
        return [self.get_node_attrs(each) for each in self.get_class_nodes(package)]

    def get_methods(self, class_: Tree = None):
        return [self.get_node_attrs(each) for each in self.get_method_nodes(class_)]

    @staticmethod
    def get_node_attrs(node: Node) -> dict:
        return {k[1:]: v for k, v in node.__dict__.items() if k.startswith("@")}

    @staticmethod
    def get_node_attr(node: Node, name: str):
        return getattr(node, f"@{name}")
