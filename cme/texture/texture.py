from pathlib import Path
from typing import Iterable, Union
from arcade.hitbox import HitBoxAlgorithm, SimpleHitBoxAlgorithm
from arcade.texture import Texture, load_texture


def load_texture_series(
    dir: Union[Path, str],
    stem: str,
    range_: Iterable,
    hit_box_algorithm: HitBoxAlgorithm = SimpleHitBoxAlgorithm(),
) -> list[Texture]:
    """Load a series of textures following a name schema from a directory.

    Args:
        dir (Union[Path, str]): The directory containing the textures
        stem (str): The name schema of the textures. Should contain the
        number/unique identifier as `{i}` to be interpolated the the
        str.format() method. Example: `"player_idle_{i}.png"`.
        range_ (Iterable): Any iterable with interpolation values. Example:
        `range(1, 7)` or `["idle", "walking", "jumping"]`.
        hit_box_algorithm (Literal["None", "Simple", "Detailed"]): Hit box
        algorithm.

    Returns:
        list[Texture]: A list of loaded textures.
    """
    textures = []
    for i in range_:
        textures.append(load_texture(
            dir / stem.format(i=i),
            hit_box_algorithm=hit_box_algorithm,
        ))
    return textures
