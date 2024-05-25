from cme import texture


def test_exports() -> None:
    all_exports = [
        "BoundingHitBoxAlgorithm",
        "HitBox",
        "HitBoxAlgorithm",
        "PymunkHitBoxAlgorithm",
        "RotatableHitBox",
        "SimpleHitBoxAlgorithm",
        "algo_bounding_box",
        "algo_default",
        "algo_detailed",
        "algo_simple",
        "calculate_hit_box_points_detailed",
        "calculate_hit_box_points_simple",
        "load_texture",
        "load_texture_series",
        "load_textures",
        "Texture",
    ]
    for item in all_exports:
        assert hasattr(texture, item)
