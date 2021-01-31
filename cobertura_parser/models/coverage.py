import typing
from pydantic import validator
from cobertura_parser.models.builtin import (
    CoberturaMethodSlim,
    CoberturaKlassSlim,
    CoberturaPackageSlim,
    CoberturaStructureSlim,
    CoberturaStructure,
    CoberturaLineSlim,
)


class CoverageMethod(CoberturaMethodSlim):
    valid_lines: int = -1
    valid_branches: int = -1

    def lazy_calc(self):
        self.valid_lines = len(self.lines)
        self.valid_branches = len([each for each in self.lines if each.is_in_branch()])
        self.lines = [each for each in self.lines if each.is_hit()]


class CoverageKlass(CoberturaKlassSlim):
    methods: typing.List[CoverageMethod]

    @validator("methods")
    def remove_no_hit_methods(cls, methods: typing.List[CoverageMethod]):
        return [each for each in methods if each.is_hit()]

    def lazy_calc(self):
        for each in self.methods:
            each.lazy_calc()


class CoveragePackage(CoberturaPackageSlim):
    classes: typing.List[CoverageKlass]

    @validator("classes")
    def remove_no_hit_classes(cls, classes: typing.List[CoverageKlass]):
        return [each for each in classes if each.is_hit()]

    def lazy_calc(self):
        for each in self.classes:
            each.lazy_calc()


class Coverage(CoberturaStructureSlim):
    packages: typing.List[CoveragePackage] = None

    @validator("packages")
    def remove_no_hit_package(cls, packages: typing.List[CoveragePackage]):
        return [each for each in packages if each.is_hit()]

    @classmethod
    def from_slim(cls, slim_data: CoberturaStructureSlim) -> "Coverage":
        return cls(**slim_data.dict())

    @classmethod
    def from_normal(cls, data: CoberturaStructure) -> "Coverage":
        return cls.from_slim(data.slim())

    def lazy_calc(self):
        for each in self.packages:
            each.lazy_calc()
