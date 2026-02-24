import calendar
from pyVmomi import vim  # type: ignore
from typing import Any


def datetime_to_timestamp(inp):
    if inp is None:
        return inp
    return calendar.timegm(inp.timetuple())


def parse_custom_fields(custom_fields: vim.VirtualMachine.customValue,
                        custom_field_keys: dict[str, int]
                        ) -> list[dict[str, Any]]:
    custom_field_data = [{
        'name': name,
        'value': _get_field_value(custom_fields, key)
    }
        for name, key in custom_field_keys.items()
    ]
    return custom_field_data


def _get_field_value(custom_fields: vim.VirtualMachine.customValue,
                     key: int) -> str:
    try:
        key_field = [field for field in custom_fields if field.key == key][0]
        value = key_field.value
    except IndexError:
        return
    if value is None:
        return
    return str(value)
