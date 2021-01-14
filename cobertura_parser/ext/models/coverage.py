import typing
from pydantic import validator
from cobertura_parser.ext.models.builtin import (
    CoberturaMethod,
    CoberturaKlass,
    CoberturaPackage,
    CoberturaCoverage,
)


class CoverageKlass(CoberturaKlass):
    @validator("methods")
    def remove_no_hit_methods(
        cls,
        methods: typing.Dict[
            str, typing.Union[CoberturaMethod, typing.List[CoberturaMethod]]
        ],
    ):
        method_key = "method"
        if not methods:
            return {method_key: []}
        methods = methods[method_key]
        if isinstance(methods, CoberturaMethod):
            methods = [methods]
        return {method_key: [each for each in methods if each.is_hit()]}


class CoveragePackage(CoberturaPackage):
    classes: typing.Dict[
        str, typing.Union[CoverageKlass, typing.List[CoverageKlass]]
    ] = None


class Coverage(CoberturaCoverage):
    sources: typing.Dict[str, typing.Union[str, typing.List[str]]] = None
    packages: typing.Dict[
        str, typing.Union[CoveragePackage, typing.List[CoveragePackage]]
    ]
