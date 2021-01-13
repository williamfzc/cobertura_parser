def unused_dict_to_list(cb_dict: dict):
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
