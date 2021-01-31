from contextlib import contextmanager
import time


@contextmanager
def time_measure(name: str, enable: bool = None):
    start = time.time()
    yield
    if enable:
        print(f"name: {name}, cost: {time.time() - start}")


def unused_dict_to_list(cb_dict: dict) -> list:
    if not cb_dict:
        return []
    # by default, xml parser will create a dict, which only contains one element
    assert len(cb_dict) == 1
    ret = list(cb_dict.values())[0]
    if isinstance(ret, list):
        return ret
    return [
        ret,
    ]
