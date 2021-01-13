import typing
import pathlib
import xmltodict


class CoberturaLoader(object):
    @classmethod
    def from_file(cls, file_path: typing.Union[str, pathlib.Path]) -> dict:
        with open(file_path, encoding="utf-8") as f:
            return cls.from_str(f.read())

    @classmethod
    def from_str(cls, xml_content: str) -> dict:
        return xmltodict.parse(xml_content)
