import typing
import pathlib
import xmltodict

from cobertura_parser.ext.models.builtin import CoberturaStructure


class CoberturaLoader(object):
    """
    load data from outside
    static class which will not save anything because data can be huge
    """

    @classmethod
    def from_file(
        cls, file_path: typing.Union[str, pathlib.Path], *args, **kwargs
    ) -> typing.Union[CoberturaStructure, dict]:
        with open(file_path, encoding="utf-8") as f:
            return cls.from_str(f.read(), *args, **kwargs)

    @classmethod
    def from_str(
        cls, xml_content: str, to_dict: bool = None
    ) -> typing.Union[CoberturaStructure, dict]:
        d = xmltodict.parse(xml_content)
        if to_dict:
            return d
        return CoberturaStructure(**d)
