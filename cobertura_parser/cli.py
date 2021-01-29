import fire

from cobertura_parser.loader import CoberturaLoader
from cobertura_parser.models.builtin import CoberturaStructure
from cobertura_parser.processor import CoberturaProcessor


class TerminalCli(object):
    def cov(self, from_file: str, to_file: str):
        structure: CoberturaStructure = CoberturaLoader.from_file(from_file)
        result = CoberturaProcessor.get_coverage(structure)
        result.lazy_calc()
        with open(to_file, "w") as f:
            f.write(
                result.json(
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
            )


def main():
    fire.Fire(TerminalCli)


if __name__ == "__main__":
    main()
