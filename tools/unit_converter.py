import re

UNIT_ALIASES = {
    'meter': 'm', 'meters': 'm', 'metre': 'm', 'metres': 'm',
    'kilometer': 'km', 'kilometers': 'km', 'kilometre': 'km', 'kilometres': 'km',
    'centimeter': 'cm', 'centimeters': 'cm', 'centimetre': 'cm', 'centimetres': 'cm',
    'millimeter': 'mm', 'millimeters': 'mm', 'millimetre': 'mm', 'millimetres': 'mm',
    'mile': 'mi', 'miles': 'mi',
    'yard': 'yd', 'yards': 'yd',
    'foot': 'ft', 'feet': 'ft',
    'inch': 'in', 'inches': 'in',
    'kilogram': 'kg', 'kilograms': 'kg',
    'gram': 'g', 'grams': 'g',
    'milligram': 'mg', 'milligrams': 'mg',
    'pound': 'lb', 'pounds': 'lb', 'ounce': 'oz', 'ounces': 'oz',
    'liter': 'l', 'liters': 'l', 'litre': 'l', 'litres': 'l',
    'milliliter': 'ml', 'milliliters': 'ml', 'millilitre': 'ml', 'millilitres': 'ml',
    'celsius': 'c', '°c': 'c', 'centigrade': 'c',
    'fahrenheit': 'f', '°f': 'f',
    'kelvin': 'k', '°k': 'k',
    'meter/second': 'm/s', 'meters/second': 'm/s', 'metre/second': 'm/s',
    'kilometer/hour': 'km/h', 'kilometers/hour': 'km/h', 'kilometre/hour': 'km/h',
    'mile/hour': 'mph', 'miles/hour': 'mph',
    'kilometer per hour': 'km/h', 'miles per hour': 'mph',
}

UNIT_FACTORS = {
    'length': {
        'm': 1.0,
        'km': 1000.0,
        'cm': 0.01,
        'mm': 0.001,
        'mi': 1609.344,
        'yd': 0.9144,
        'ft': 0.3048,
        'in': 0.0254,
    },
    'mass': {
        'kg': 1.0,
        'g': 0.001,
        'mg': 0.000001,
        'lb': 0.45359237,
        'oz': 0.0283495231,
    },
    'volume': {
        'l': 1.0,
        'ml': 0.001,
        'm3': 1000.0,
    },
    'speed': {
        'm/s': 1.0,
        'km/h': 0.277777778,
        'mph': 0.44704,
    },
}

TEMPERATURE_UNITS = {'c', 'f', 'k'}

UNIT_PATTERN = r"(?:°?c|°?f|°?k|km/h|m/s|mph|km|m|cm|mm|mi|yd|ft|in|kg|g|mg|lb|oz|l|ml|m3)"


def _normalize_unit(unit: str) -> str:
    if not unit:
        return ''
    normalized = unit.strip().lower().replace('per', '/').replace(' ', '')
    return UNIT_ALIASES.get(normalized, normalized)


def _parse_input(arguments: dict):
    quantity = arguments.get('quantity')
    from_unit = arguments.get('from_unit') or arguments.get('from')
    to_unit = arguments.get('to_unit') or arguments.get('to')
    raw = arguments.get('input') or arguments.get('query')

    if quantity is not None and from_unit and to_unit:
        return quantity, from_unit, to_unit

    if raw and isinstance(raw, str):
        regex = re.compile(
            rf"(?P<value>-?[0-9]+(?:\.[0-9]+)?)\s*(?P<from>{UNIT_PATTERN})\s*(?:to|in|into)\s*(?P<to>{UNIT_PATTERN})",
            re.IGNORECASE,
        )
        match = regex.search(raw)
        if match:
            return match.group('value'), match.group('from'), match.group('to')

    return quantity, from_unit, to_unit


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return value

    celsius = value
    if from_unit == 'f':
        celsius = (value - 32) * 5.0 / 9.0
    elif from_unit == 'k':
        celsius = value - 273.15

    if to_unit == 'c':
        return celsius
    if to_unit == 'f':
        return celsius * 9.0 / 5.0 + 32
    if to_unit == 'k':
        return celsius + 273.15

    raise ValueError(f"Unsupported temperature target unit: {to_unit}")


def _find_unit_category(unit: str):
    for category, units in UNIT_FACTORS.items():
        if unit in units:
            return category
    if unit in TEMPERATURE_UNITS:
        return 'temperature'
    return None


def _convert_generic(quantity: float, from_unit: str, to_unit: str) -> float:
    category = _find_unit_category(from_unit)
    if category != _find_unit_category(to_unit):
        raise ValueError(f"Cannot convert '{from_unit}' to '{to_unit}'. Units are not in the same category.")

    if category == 'temperature':
        return _convert_temperature(quantity, from_unit, to_unit)

    from_factor = UNIT_FACTORS[category][from_unit]
    to_factor = UNIT_FACTORS[category][to_unit]
    return quantity * (from_factor / to_factor)


def convert(arguments: dict):
    quantity, from_unit, to_unit = _parse_input(arguments)
    if quantity is None or from_unit is None or to_unit is None:
        return {
            'error': 'Unit converter requires quantity, from_unit, and to_unit. Example: {"tool": "unit_converter", "quantity": 5, "from_unit": "km", "to_unit": "mi"}'
        }

    try:
        quantity = float(quantity)
    except Exception:
        return {'error': 'Quantity must be a number.'}

    from_unit = _normalize_unit(from_unit)
    to_unit = _normalize_unit(to_unit)

    if not from_unit or not to_unit:
        return {'error': 'Unable to recognize unit names.'}

    try:
        result = _convert_generic(quantity, from_unit, to_unit)
    except Exception as e:
        return {'error': str(e)}

    return f"{quantity} {from_unit} = {round(result, 6)} {to_unit}"


if __name__ == '__main__':
    print(convert({'quantity': 5, 'from_unit': 'km', 'to_unit': 'mi'}))
    print(convert({'input': 'Convert 32 F to C'}))
    print(convert({'input': '10 pounds in kg'}))
