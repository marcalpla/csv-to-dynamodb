import json
from decimal import Decimal


def convert_attribute(value, attr_type):
    if value is None or value == '':
        return None

    try:
        if attr_type == 'string':
            return str(value)
        elif attr_type == 'number':
            return Decimal(value) if '.' in value else int(value)
        elif attr_type == 'boolean':
            return value.lower() in ('true', '1', 'yes')
        elif attr_type == 'json':
            return json.loads(value, parse_float=Decimal)
        else:
            return value
    except Exception as e:
        raise ValueError(f"Error converting attribute: {value} "
                         f"to type {attr_type}. {str(e)}")