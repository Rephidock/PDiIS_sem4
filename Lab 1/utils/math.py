

def lerp(x1: float, x2: float, t: float) -> float:
    """Returns value linearly interpolated between x1 and x2"""
    return x1 + (x2-x1) * t


def lerp_clamped(x1: float, x2: float, t: float) -> float:
    """Returns value linearly interpolated between x1 and x2 bound between the 2 values"""
    return lerp(x1, x2, clamp(t, 0.0, 1.0))


def clamp(val: float, min_val: float, max_val: float) -> float:
    """Returns value clamped between boundaries (inclusive)"""
    return max(min(val, max_val), min_val)
