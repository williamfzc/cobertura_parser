"""
these models have same structure as origin cobertura dtd
see http://cobertura.sourceforge.net/xml/coverage-04.dtd
"""
from pydantic import BaseModel
import typing

TYPE_ORIGIN_CONDITIONS = typing.Dict[
    str, typing.Union["CoberturaCondition", typing.List["CoberturaCondition"]]
]

TYPE_ORIGIN_LINES = typing.Optional[
    typing.Dict[str, typing.Union["CoberturaLine", typing.List["CoberturaLine"]]]
]
TYPE_ORIGIN_METHODS = typing.Optional[
    typing.Dict[str, typing.Union["CoberturaMethod", typing.List["CoberturaMethod"]]]
]
TYPE_ORIGIN_KLASSES = typing.Dict[
    str, typing.Union["CoberturaKlass", typing.List["CoberturaKlass"]]
]
TYPE_ORIGIN_PACKAGES = typing.Dict[
    str, typing.Union["CoberturaPackage", typing.List["CoberturaPackage"]]
]


class CoberturaCondition(BaseModel):
    number: int
    type: str
    coverage: str

    class Config:
        allow_population_by_field_name = True
        fields = {
            "number": {"alias": "@number"},
            "type": {"alias": "@type"},
            "coverage": {"alias": "@coverage"},
        }


class CoberturaLine(BaseModel):
    number: int
    hits: int
    # can not be `bool` because it can not be cast to xml format back
    branch: str
    condition_coverage: str = None

    conditions: TYPE_ORIGIN_CONDITIONS = None

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
    lines: TYPE_ORIGIN_LINES = dict()

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

    methods: TYPE_ORIGIN_METHODS = dict()
    lines: TYPE_ORIGIN_LINES = dict()

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
    classes: TYPE_ORIGIN_KLASSES = None

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
    packages: TYPE_ORIGIN_PACKAGES

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
