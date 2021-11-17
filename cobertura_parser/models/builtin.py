"""
these models have same structure as origin cobertura dtd
see http://cobertura.sourceforge.net/xml/coverage-04.dtd
"""
from pydantic import BaseModel
import typing
from cobertura_parser.utils import unused_dict_to_list

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

    def is_hit(self) -> bool:
        return bool(self.hits)

    def is_in_branch(self) -> bool:
        # todo: is it correct??
        return self.branch == "true"


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

    def get_line_list(self) -> typing.List[CoberturaLine]:
        return unused_dict_to_list(self.lines)


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

    def get_method_list(self) -> typing.List[CoberturaMethod]:
        return unused_dict_to_list(self.methods)

    def get_line_list(self) -> typing.List[CoberturaLine]:
        return unused_dict_to_list(self.lines)


class CoberturaPackage(BaseModel):
    name: str
    line_rate: float
    branch_rate: float
    complexity: float = None
    classes: TYPE_ORIGIN_KLASSES = dict()

    class Config:
        allow_population_by_field_name = True
        fields = {
            "name": {"alias": "@name"},
            "line_rate": {"alias": "@line-rate"},
            "branch_rate": {"alias": "@branch-rate"},
            "complexity": {"alias": "@complexity"},
        }

    def get_class_list(self) -> typing.List[CoberturaKlass]:
        return unused_dict_to_list(self.classes)


class CoberturaCoverage(BaseModel):
    sources: typing.Dict[str, typing.Union[str, typing.List[str]]] = None
    packages: TYPE_ORIGIN_PACKAGES = None

    # attrs
    line_rate: float
    branch_rate: float
    line_covered: int = None
    line_valid: int = None
    branches_covered: int = None
    branches_valid: int = None
    complexity: float = None
    version: float = -1.0
    timestamp: float = -1.0

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

    def get_package_list(self) -> typing.List[CoberturaPackage]:
        return unused_dict_to_list(self.packages)

    def slim(self) -> "CoberturaStructureSlim":
        data = CoberturaCoverage(**self.dict())
        for each_pkg in data.get_package_list():
            for each_kls in each_pkg.get_class_list():
                for each_method in each_kls.get_method_list():
                    each_method.lines = each_method.get_line_list()
                each_kls.methods = each_kls.get_method_list()
                each_kls.lines = each_kls.get_line_list()
            each_pkg.classes = each_pkg.get_class_list()
        data.packages = data.get_package_list()
        return CoberturaStructureSlim(**data.dict())


class CoberturaLineSlim(CoberturaLine):
    pass


class CoberturaMethodSlim(CoberturaMethod):
    lines: typing.List[CoberturaLine] = None

    def get_line_list(self) -> typing.List[CoberturaLine]:
        raise NotImplementedError

    def is_hit(self) -> bool:
        return any((each.is_hit() for each in self.lines))


class CoberturaKlassSlim(CoberturaKlass):
    methods: typing.List[CoberturaMethodSlim] = None
    lines: typing.List[CoberturaLineSlim] = None

    def get_method_list(self) -> typing.List[CoberturaMethod]:
        raise NotImplementedError

    def get_line_list(self) -> typing.List[CoberturaLine]:
        raise NotImplementedError

    def is_hit(self) -> bool:
        return any((each.is_hit() for each in self.methods))


class CoberturaPackageSlim(CoberturaPackage):
    classes: typing.List[CoberturaKlassSlim] = None

    def get_class_list(self) -> typing.List[CoberturaKlass]:
        raise NotImplementedError

    def is_hit(self) -> bool:
        return any((each.is_hit() for each in self.classes))


class CoberturaStructureSlim(CoberturaCoverage):
    packages: typing.List[CoberturaPackageSlim] = None

    def get_package_list(self) -> typing.List[CoberturaPackage]:
        raise NotImplementedError


class CoberturaStructure(BaseModel):
    coverage: CoberturaCoverage

    def to_origin(self) -> dict:
        return self.dict(by_alias=True, exclude_defaults=True)

    def slim(self) -> CoberturaStructureSlim:
        return self.coverage.slim()
