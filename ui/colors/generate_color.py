from ui.colors.color_utils import random_primary, reduce_color_lightness


def random_light() -> str:
    return random_primary(200).as_hex()


def random_dark(shade: int = 200, reduce: float = 0.95) -> str:
    assert (reduce <= 1)
    color = random_primary(shade)
    return reduce_color_lightness(color, reduce).as_hex()
