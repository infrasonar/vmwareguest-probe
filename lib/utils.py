import calendar
from pyVmomi import vim
from typing import Any


def datetime_to_timestamp(inp):
    if inp is None:
        return inp
    return calendar.timegm(inp.timetuple())


def parse_custom_fields(custom_fields: list[vim.CustomFieldsManager.Value],
                        custom_field_keys: dict[str, int]
                        ) -> list[dict[str, Any]]:
    custom_fields_lk = {
        field.key: field.value
        for field in custom_fields
    }
    custom_field_data = [{
        'name': name,
        'value': _get_field_value(custom_fields_lk, key)
    }
        for name, key in custom_field_keys.items()
    ]
    return custom_field_data


def _get_field_value(fields: dict[int, vim.CustomFieldsManager.Value],
                     key: int) -> str:
    try:
        key_field = fields[key]
        value = key_field.value
    except KeyError:
        return f'<NO_INDEX_{key}>'
    if value is None:
        return '<NONE>'
    return str(value)
