import gzip
import io
import typing
import pathlib
import xmltodict

from cobertura_parser.models.builtin import CoberturaStructure
from cobertura_parser.ext.jacoco import jacoco2cobertura


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
        d = xmltodict.parse(
            gzip.GzipFile(fileobj=io.BytesIO(gzip.compress(xml_content.encode())))
        )
        if to_dict:
            return d
        return CoberturaStructure(**d)

    @classmethod
    def from_jacoco_file(
        cls, file_path: typing.Union[str, pathlib.Path], *args, **kwargs
    ):
        return cls.from_str(jacoco2cobertura(file_path), *args, **kwargs)
