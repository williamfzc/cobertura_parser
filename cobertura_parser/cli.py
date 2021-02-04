import fire

from cobertura_parser.loader import CoberturaLoader
from cobertura_parser.models.builtin import CoberturaStructure
from cobertura_parser.processor import CoberturaProcessor
from cobertura_parser.utils import time_measure
from cobertura_parser.ext.jacoco import jacoco2cobertura


class TerminalCli(object):
    def _cov(self, structure: CoberturaStructure) -> str:
        result = CoberturaProcessor.get_coverage(structure)
        result.lazy_calc()
        return result.json(
            exclude={
                "sources": ...,
                "line_rate": ...,
                "branch_rate": ...,
                "line_covered": ...,
                "line_valid": ...,
                "branches_covered": ...,
                "branches_valid": ...,
                "complexity": ...,
                "version": ...,
                "packages": {
                    "__all__": {
                        "classes": {
                            "__all__": {
                                "methods": {
                                    "__all__": {
                                        "branch_rate",
                                        "line_rate",
                                        "complexity",
                                    }
                                },
                                "branch_rate": ...,
                                "line_rate": ...,
                                "complexity": ...,
                                "lines": ...,
                            }
                        },
                        "branch_rate": ...,
                        "line_rate": ...,
                        "complexity": ...,
                    }
                },
            }
        )

    def cov(self, from_file: str, to_file: str, dev: bool = None):
        with time_measure("cov", dev):
            structure: CoberturaStructure = CoberturaLoader.from_file(from_file)
            with open(to_file, "w") as f:
                f.write(self._cov(structure))

    def cov_from_jacoco(self, from_file: str, to_file: str, dev: bool = None):
        with time_measure("cov_from_jacoco", dev):
            structure: CoberturaStructure = CoberturaLoader.from_jacoco_file(from_file)
            with open(to_file, "w") as f:
                f.write(self._cov(structure))

    def xml_from_jacoco(self, from_file: str, to_file: str, dev: bool = None):
        with time_measure("xml_from_jacoco", dev):
            with open(to_file, "w") as f:
                f.write(jacoco2cobertura(from_file))


def main():
    fire.Fire(TerminalCli)


if __name__ == "__main__":
    main()
