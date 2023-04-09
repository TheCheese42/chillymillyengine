from cme import texture


def test_exports() -> None:
    all_exports = [
        "load_texture",
        "load_textures",
        "Texture",
    ]
    for item in all_exports:
        assert hasattr(texture, item)
