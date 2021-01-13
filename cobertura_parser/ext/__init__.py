import typing
import pathlib
import xmltodict
from pydantic import BaseModel


class CoberLine(BaseModel):
    number: int
    hits: int
    branch: bool = False
    condition_coverage: str = None

    class Config:
        allow_population_by_field_name = True
        fields = {
            "number": {"alias": "@number"},
            "hits": {"alias": "@hits"},
            "branch": {"alias": "@branch"},
            "condition_coverage": {"alias": "@condition-coverage"},
        }


class CoberMethod(BaseModel):
    name: str
    signature: str
    line_rate: float
    branch_rate: float
    complexity: float = None

    # 3 types
    # - None
    # - Dict (only one element
    # - List (more than one
    lines: typing.Dict[str, typing.Union[CoberLine, typing.List[CoberLine]]] = None

    class Config:
        allow_population_by_field_name = True
        fields = {
            "name": {"alias": "@name"},
            "signature": {"alias": "@signature"},
            "line_rate": {"alias": "@line-rate"},
            "branch_rate": {"alias": "@branch-rate"},
            "complexity": {"alias": "@complexity"},
        }


class CoberKls(BaseModel):
    name: str
    filename: str
    line_rate: float
    branch_rate: float
    complexity: float = None

    methods: typing.Dict[
        str, typing.Union[CoberMethod, typing.List[CoberMethod]]
    ] = None

    class Config:
        allow_population_by_field_name = True
        fields = {
            "name": {"alias": "@name"},
            "filename": {"alias": "@filename"},
            "line_rate": {"alias": "@line-rate"},
            "branch_rate": {"alias": "@branch-rate"},
            "complexity": {"alias": "@complexity"},
        }


class CoberPackage(BaseModel):
    name: str
    line_rate: float
    branch_rate: float
    complexity: float = None
    classes: typing.Dict[str, typing.Union[CoberKls, typing.List[CoberKls]]] = None

    class Config:
        allow_population_by_field_name = True
        fields = {
            "name": {"alias": "@name"},
            "line_rate": {"alias": "@line-rate"},
            "branch_rate": {"alias": "@branch-rate"},
            "complexity": {"alias": "@complexity"},
        }


class CoberCoverage(BaseModel):
    sources: typing.Dict[str, typing.Union[str, typing.List[str]]] = None
    packages: typing.Dict[str, typing.Union[CoberPackage, typing.List[CoberPackage]]]

    # attrs
    line_rate: float
    branch_rate: float
    line_covered: int
    line_valid: int
    branches_covered: int
    branches_valid: int
    complexity: float = None
    version: int
    timestamp: int

    class Config:
        allow_population_by_field_name = True
        fields = {
            "line_rate": {"alias": "@line-rate"},
            "branch_rate": {"alias": "@branch-rate"},
            "line_covered": {"alias": "@lines-covered"},
            "line_valid": {"alias": "@lines-valid"},
            "branches_covered": {"alias": "@branches-covered"},
            "branches_valid": {"alias": "@branches-valid"},
            "complexity": {"alias": "@complexity"},
            "version": {"alias": "@version"},
            "timestamp": {"alias": "@timestamp"},
        }


class CoberStructure(BaseModel):
    coverage: CoberCoverage


class CoberturaLoader(object):
    @classmethod
    def from_file(cls, file_path: typing.Union[str, pathlib.Path]) -> dict:
        with open(file_path, encoding="utf-8") as f:
            return cls.from_str(f.read())

    @classmethod
    def from_str(cls, xml_content: str) -> dict:
        return xmltodict.parse(xml_content)


if __name__ == "__main__":
    r = CoberturaLoader.from_file("../../Cobertura.xml")
    import json

    sss = json.dumps(r)
    print(sss)
    print(r["coverage"]["packages"]["package"])
    print(CoberStructure(**r))
