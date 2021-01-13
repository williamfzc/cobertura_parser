from cobertura_parser.ext.loader import CoberturaLoader
from cobertura_parser.ext.model import CoberturaStructure


def test_loader():
    r = CoberturaLoader.from_file("../data/cobertura.xml")
    import json

    sss = json.dumps(r)
    print(sss)
    print(r["coverage"]["packages"]["package"])
    print(CoberturaStructure(**r))
