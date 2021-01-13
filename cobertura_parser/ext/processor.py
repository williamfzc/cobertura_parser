from cobertura_parser.ext.models.builtin import CoberturaStructure
from cobertura_parser.ext.models.snapshot import CodeSnapshot
from cobertura_parser.ext.models.coverage import Coverage


class CoberturaProcessor(object):
    """
    processing some loaded data
    static class too, and these API should not change origin data
    """

    @classmethod
    def get_code_snapshot(cls, data: CoberturaStructure) -> CodeSnapshot:
        return CodeSnapshot(**data.coverage.dict())

    @classmethod
    def get_coverage(cls, data: CoberturaStructure) -> Coverage:
        pass
