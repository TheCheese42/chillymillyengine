# FAQ

## AttributeError: module 'config' has no attribute 'app_name'

You didn't properly initialized the engine. Run the `init_cme()` function as described in the README.

## How do I add Textures to an AnimatedSprite based sprite?

Load the Textures via `texture.load_texture` and add them using the sprite's `add_texture()` method with the corresponding state (e.g. 'walking', 'idling', etc.) like this:

```py
idling_texture = load_texture("path/to/texture.png")

sprite.add_texture(idling_texture, "idling")
```

If you are in the need of different textures for different facing directions or similar, you can give a tuple containing those as the first argument to `.add_texture()`. The index of the textures determines the facing directory wich can be set with the sprites `facing` property. We recommend using the `enums.Facing` enum for common facing directions.
