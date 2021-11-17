from lcov_cobertura import LcovCobertura


def lcov2cobertura(data: str) -> str:
    converter = LcovCobertura(data)
    cobertura_xml = converter.convert()
    return cobertura_xml
