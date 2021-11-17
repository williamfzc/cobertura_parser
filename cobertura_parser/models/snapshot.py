import typing
from pydantic import BaseModel, validator
from cobertura_parser.models.builtin import (
    CoberturaMethod,
    CoberturaKlass,
    CoberturaPackage,
    CoberturaLine,
    CoberturaStructureSlim,
    CoberturaStructure,
)


class CodeSnapshotMethod(CoberturaMethod):
    _TYPE_LINE_FINAL = typing.Union[typing.List[int], typing.List[CoberturaLine]]
    lines: _TYPE_LINE_FINAL = None

    @validator("lines")
    def line2int(cls, lines: typing.List[CoberturaLine]):
        return [each.number for each in lines]


class CodeSnapshotKlass(CoberturaKlass):
    _TYPE_LINE_FINAL = typing.Union[typing.List[int], typing.List[CoberturaLine]]
    lines: _TYPE_LINE_FINAL = None
    methods: typing.List[CodeSnapshotMethod]

    @validator("lines")
    def line2int(cls, lines: typing.List[CoberturaLine]):
        return [each.number for each in lines]


class CodeSnapshotPackage(CoberturaPackage):
    classes: typing.List[CodeSnapshotKlass]


class CodeSnapshot(BaseModel):
    """snapshot does not need other attrs, so inherits from BaseModel"""

    sources: typing.Dict[str, typing.Union[str, typing.List[str]]] = None
    packages: typing.List[CodeSnapshotPackage]

    @classmethod
    def from_slim(cls, slim_data: CoberturaStructureSlim) -> "CodeSnapshot":
        return cls(**slim_data.dict())

    @classmethod
    def from_normal(cls, data: CoberturaStructure) -> "CodeSnapshot":
        return cls.from_slim(data.slim())


class CodeSnapshotExt(BaseModel):
    pass


class CodeSnapshotFat(BaseModel):
    data: CodeSnapshot
    extras: CodeSnapshotExt = dict()

    @classmethod
    def from_slim(cls, slim_data: CoberturaStructureSlim) -> "CodeSnapshotFat":
        # todo: extras will be auto calculated inside
        return cls(data=slim_data.dict())

    @classmethod
    def from_normal(cls, data: CoberturaStructure) -> "CodeSnapshotFat":
        return cls.from_slim(data.slim())
