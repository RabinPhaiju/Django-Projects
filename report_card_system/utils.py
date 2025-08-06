def is_int_parsable(value):
    """Check if a value can be parsed as an integer."""
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False

