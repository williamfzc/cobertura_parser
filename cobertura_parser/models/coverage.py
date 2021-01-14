import typing
from pydantic import validator
from cobertura_parser.models.builtin import (
    CoberturaMethodSlim,
    CoberturaKlassSlim,
    CoberturaPackageSlim,
    CoberturaStructureSlim,
    CoberturaStructure,
)


class CoverageKlass(CoberturaKlassSlim):
    @validator("methods")
    def remove_no_hit_methods(cls, methods: typing.List[CoberturaMethodSlim]):
        return [each for each in methods if each.is_hit()]


class CoveragePackage(CoberturaPackageSlim):
    classes: typing.List[CoverageKlass]

    @validator("classes")
    def remove_no_hit_classes(cls, classes: typing.List[CoverageKlass]):
        return [each for each in classes if each.is_hit()]


class Coverage(CoberturaStructureSlim):
    packages: typing.List[CoveragePackage]

    @validator("packages")
    def remove_no_hit_package(cls, packages: typing.List[CoveragePackage]):
        return [each for each in packages if each.is_hit()]

    @classmethod
    def from_slim(cls, slim_data: CoberturaStructureSlim) -> "Coverage":
        return cls(**slim_data.dict())

    @classmethod
    def from_normal(cls, data: CoberturaStructure) -> "Coverage":
        return cls.from_slim(data.slim())
