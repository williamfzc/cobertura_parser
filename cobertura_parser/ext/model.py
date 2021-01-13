from pydantic import BaseModel
import typing


class CoberturaLine(BaseModel):
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


class CoberturaMethod(BaseModel):
    name: str
    signature: str
    line_rate: float
    branch_rate: float
    complexity: float = None

    # 3 types
    # - None
    # - Dict (only one element
    # - List (more than one
    lines: typing.Dict[str, typing.Union[CoberturaLine, typing.List[CoberturaLine]]] = None

    class Config:
        allow_population_by_field_name = True
        fields = {
            "name": {"alias": "@name"},
            "signature": {"alias": "@signature"},
            "line_rate": {"alias": "@line-rate"},
            "branch_rate": {"alias": "@branch-rate"},
            "complexity": {"alias": "@complexity"},
        }


class CoberturaKlass(BaseModel):
    name: str
    filename: str
    line_rate: float
    branch_rate: float
    complexity: float = None

    methods: typing.Dict[
        str, typing.Union[CoberturaMethod, typing.List[CoberturaMethod]]
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


class CoberturaPackage(BaseModel):
    name: str
    line_rate: float
    branch_rate: float
    complexity: float = None
    classes: typing.Dict[str, typing.Union[CoberturaKlass, typing.List[CoberturaKlass]]] = None

    class Config:
        allow_population_by_field_name = True
        fields = {
            "name": {"alias": "@name"},
            "line_rate": {"alias": "@line-rate"},
            "branch_rate": {"alias": "@branch-rate"},
            "complexity": {"alias": "@complexity"},
        }


class CoberturaCoverage(BaseModel):
    sources: typing.Dict[str, typing.Union[str, typing.List[str]]] = None
    packages: typing.Dict[str, typing.Union[CoberturaPackage, typing.List[CoberturaPackage]]]

    # attrs
    line_rate: float
    branch_rate: float
    line_covered: int = None
    line_valid: int = None
    branches_covered: int = None
    branches_valid: int = None
    complexity: float = None
    version: float
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


class CoberturaStructure(BaseModel):
    coverage: CoberturaCoverage
