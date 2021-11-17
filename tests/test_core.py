from cobertura_parser.loader import CoberturaLoader
from cobertura_parser.models.builtin import (
    CoberturaStructure,
    CoberturaStructureSlim,
)
from cobertura_parser.models.snapshot import CodeSnapshot
from cobertura_parser.processor import CoberturaProcessor
import xmltodict
import pathlib


DATA_FILE = pathlib.Path(__file__).parent / "data" / "cobertura.xml"


def test_loader_roundtripping():
    with open(DATA_FILE) as f:
        before = f.read()
    after = xmltodict.unparse(CoberturaLoader.from_str(before, to_dict=True))
    assert xmltodict.parse(before) == xmltodict.parse(after)


def test_loader_model_roundtripping():
    with open(DATA_FILE) as f:
        origin = f.read()
    before = CoberturaLoader.from_str(origin, to_dict=True)
    after = CoberturaStructure(**before).to_origin()
    assert xmltodict.unparse(before) == xmltodict.unparse(after)


def test_snapshot():
    r = CoberturaLoader.from_file(DATA_FILE)
    snapshot = CoberturaProcessor.get_code_snapshot(r)
    assert isinstance(snapshot, CodeSnapshot)


def test_coverage():
    def _all_method_hit(c: CoberturaStructureSlim):
        for each_pkg in c.packages:
            for each_kls in each_pkg.classes:
                for each_method in each_kls.methods:
                    if not each_method.is_hit():
                        return False
        return True

    r = CoberturaLoader.from_file(DATA_FILE)
    before = r.slim()
    assert not _all_method_hit(before)
    after = CoberturaProcessor.get_coverage(before)
    assert _all_method_hit(after)


def test_slim():
    r = CoberturaLoader.from_file(DATA_FILE)
    slim = r.slim()
    sub_slim = r.coverage.slim()
    assert isinstance(slim, CoberturaStructureSlim)
    assert slim.json() == sub_slim.json()
