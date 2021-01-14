from cobertura_parser.ext.loader import CoberturaLoader
from cobertura_parser.ext.models.builtin import CoberturaStructure
import pathlib


DATA_FILE = pathlib.Path(__file__).parent.parent / "data" / "cobertura.xml"


def test_builtin_model_api_hit():
    d = CoberturaLoader.from_file(DATA_FILE)
    s = d.slim()
    some_kls_not_hit = False
    for each in s.packages:
        assert each.is_hit()
        for each_kls in each.classes:
            if not each_kls.is_hit():
                some_kls_not_hit = True
    assert some_kls_not_hit
