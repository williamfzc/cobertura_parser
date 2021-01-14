import typing
from cobertura_parser.models.builtin import (
    CoberturaStructure,
    CoberturaStructureSlim,
)
from cobertura_parser.models.snapshot import CodeSnapshot
from cobertura_parser.models.coverage import Coverage


class CoberturaProcessor(object):
    """
    processing some loaded data
    static class too, and these API should not change origin data
    """

    @classmethod
    def get_code_snapshot(
        cls, data: typing.Union[CoberturaStructure, CoberturaStructureSlim]
    ) -> CodeSnapshot:
        if isinstance(data, CoberturaStructure):
            return CodeSnapshot.from_normal(data)
        return CodeSnapshot.from_slim(data)

    @classmethod
    def get_coverage(
        cls, data: typing.Union[CoberturaStructure, CoberturaStructureSlim]
    ) -> Coverage:
        if isinstance(data, CoberturaStructure):
            return Coverage.from_normal(data)
        return Coverage.from_slim(data)
