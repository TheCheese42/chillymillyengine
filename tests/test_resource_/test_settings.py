from typing import Any

import pytest


@pytest.fixture
def custom_settings_class(initialize_cme: None) -> type:
    from cme import resource_

    class CustomSettings(resource_.Settings):
        def apply(self) -> None:
            return super().apply()

        def update(self, *args: Any, **kwargs: Any) -> None:
            return super().update(*args, **kwargs)

        def _serialize(self) -> dict[Any, Any]:
            return {}

        @classmethod
        def _deserialize(cls, dictionary: dict[Any, Any]) -> "CustomSettings":
            return CustomSettings()

        @staticmethod
        def defaults() -> dict[Any, Any]:
            return {}

    return CustomSettings


def test_custom_settings_class_constant(
    initialize_cme: None, custom_settings_class: type
) -> None:
    from cme import resource_
    assert resource_.get_settings() is None
    resource_.register_custom_settings_class(custom_settings_class)
    assert resource_.get_settings() is custom_settings_class


def test_settings_interface(initialize_cme: None) -> None:
    from cme import resource_
    with pytest.raises(TypeError):
        resource_.Settings()  # type: ignore
