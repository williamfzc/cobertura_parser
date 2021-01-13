from cobertura_parser.ext.loader import CoberturaLoader
from cobertura_parser.ext.models.builtin import CoberturaStructure
from cobertura_parser.ext.models.snapshot import CodeSnapshot
from cobertura_parser.ext.processor import CoberturaProcessor
import xmltodict


DATA_FILE = "../data/cobertura.xml"


def test_loader_roundtripping():
    with open(DATA_FILE) as f:
        before = f.read()
    after = xmltodict.unparse(CoberturaLoader.from_str(before))
    assert xmltodict.parse(before) == xmltodict.parse(after)


def test_loader_model_roundtripping():
    with open(DATA_FILE) as f:
        origin = f.read()
    before = CoberturaLoader.from_str(origin)
    after = CoberturaStructure(**before).dict(by_alias=True, exclude_defaults=True)
    assert xmltodict.unparse(before) == xmltodict.unparse(after)


def test_snapshot():
    r = CoberturaLoader.from_file("../data/cobertura.xml")
    s = CoberturaStructure(**r)
    assert isinstance(CoberturaProcessor.get_code_snapshot(s), CodeSnapshot)
