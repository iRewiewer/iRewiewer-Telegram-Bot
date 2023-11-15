def TryParseInt(value: str) -> int:
    try:
        result = int(value)
        return result
    except ValueError:
        return None