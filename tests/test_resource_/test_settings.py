from typing import Any

import pytest

from cme import resource_


@pytest.fixture
def custom_settings_class() -> type:
    class CustomSettings(resource_.Settings):
        def apply(self) -> None:
            pass

        def update(self, *args: Any, **kwargs: Any) -> None:
            pass

        def _serialize(self) -> dict[Any, Any]:
            return {}

        @classmethod
        def _deserialize(cls, dictionary: dict[Any, Any]) -> "CustomSettings":
            return CustomSettings()

        @staticmethod
        def defaults() -> dict[Any, Any]:
            return {}

    return CustomSettings


def test_settings_interface() -> None:
    from cme import resource_
    with pytest.raises(TypeError):
        resource_.Settings()  # type: ignore
