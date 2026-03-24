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
    items = []
    for name, key in custom_field_keys.items():
        value = _get_field_value(custom_fields_lk, key)
        if value is not None:
            items.append({
                'name': name,
                'value': value,
            })
    return items


def _get_field_value(fields: dict[int, Any],
                     key: int) -> str | None:
    try:
        value = fields[key]
    except KeyError:
        return None  # f'<NO_INDEX_{key}>'
    if value is None:
        return '<NONE>'
    return str(value)
