import typing
from pydantic import BaseModel, validator
from cobertura_parser.ext.models.builtin import (
    CoberturaMethod,
    CoberturaKlass,
    CoberturaPackage,
    CoberturaLine,
    TYPE_ORIGIN_LINES,
)


class CodeSnapshotMethod(CoberturaMethod):
    _TYPE_LINE_FINAL = typing.Union[typing.List[int], TYPE_ORIGIN_LINES]
    lines: _TYPE_LINE_FINAL = None

    @validator("lines")
    def line2int(cls, lines: TYPE_ORIGIN_LINES = None):
        if not lines:
            return []
        # `lines` dict will only have one element
        lines = lines["line"]
        if isinstance(lines, CoberturaLine):
            return [lines.number]
        return [each.number for each in lines]


class CodeSnapshotKlass(CoberturaKlass):
    methods: typing.Dict[
        str, typing.Union[CodeSnapshotMethod, typing.List[CodeSnapshotMethod]]
    ] = None


class CodeSnapshotPackage(CoberturaPackage):
    classes: typing.Dict[
        str, typing.Union[CodeSnapshotKlass, typing.List[CodeSnapshotKlass]]
    ] = None


class CodeSnapshot(BaseModel):
    sources: typing.Dict[str, typing.Union[str, typing.List[str]]] = None
    packages: typing.Dict[
        str, typing.Union[CodeSnapshotPackage, typing.List[CodeSnapshotPackage]]
    ]
