from cme import font


def test_exports_load_font() -> None:
    assert hasattr(font, "load_font") and callable(font.load_font)
