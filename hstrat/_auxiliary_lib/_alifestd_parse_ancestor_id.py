import typing


def alifestd_parse_ancestor_id(ancestor_list_str: str) -> typing.Optional[int]:
    if ancestor_list_str.lower() in (
        "[]",
        "[none]",
    ):
        return None
    else:
        without_brackets_str = ancestor_list_str[1:-1]
        return int(without_brackets_str)
