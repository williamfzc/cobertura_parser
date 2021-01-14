from cobertura_parser.ext.loader import CoberturaLoader
from cobertura_parser.ext.models.builtin import (
    CoberturaStructure,
    CoberturaCoverage,
    CoberturaStructureSlim,
)
from cobertura_parser.ext.models.snapshot import CodeSnapshot
from cobertura_parser.ext.processor import CoberturaProcessor
import xmltodict
import pathlib


DATA_FILE = pathlib.Path(__file__).parent.parent / "data" / "cobertura.xml"


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
    r = CoberturaLoader.from_file(DATA_FILE)
    s = CoberturaStructure(**r)
    assert isinstance(CoberturaProcessor.get_code_snapshot(s), CodeSnapshot)


def test_coverage():
    def _all_method_hit(c: CoberturaCoverage):
        for each_pkg in c.get_package_list():
            for each_kls in each_pkg.get_class_list():
                for each_method in each_kls.get_method_list():
                    if not each_method.is_hit():
                        return False
        return True

    r = CoberturaLoader.from_file(DATA_FILE)
    before = CoberturaStructure(**r)
    assert not _all_method_hit(before.coverage)
    after = CoberturaProcessor.get_coverage(before)
    assert _all_method_hit(after)


def test_slim():
    r = CoberturaLoader.from_file(DATA_FILE)
    s = CoberturaStructure(**r)
    slim = s.slim()
    sub_slim = s.coverage.slim()
    assert isinstance(slim, CoberturaStructureSlim)
    assert slim.json() == sub_slim.json()
