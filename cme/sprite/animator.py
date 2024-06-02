from typing import Any, Iterable, Union

from .sprite import Sprite


class Animator:
    """
    Animate a Sprite (or any other object) by changing float values over time,
    to a specified destination value.
    """
    def __init__(
        self,
        obj: Union[Sprite, Any],
        seconds: float,
        **kwargs: float,
    ) -> None:
        self._obj = obj
        self._seconds = self._remaining_seconds = seconds
        self._dest_attrs = kwargs
        self._original_attrs = self._cur_attrs(obj, kwargs)

    @staticmethod
    def _cur_attrs(obj: Any, attrs: Iterable[str]) -> dict[str, float]:
        return {k: getattr(obj, k) for k in attrs}

    def update(self, delta_time: float) -> None:
        self._remaining_seconds -= delta_time
        seconds_done = self._seconds - self._remaining_seconds
        percent_done = seconds_done / self._seconds
        for attr in self._dest_attrs:
            difference = self._dest_attrs[attr] - self._original_attrs[attr]
            setattr(
                self._obj,
                attr,
                self._original_attrs[attr] + difference * percent_done,
            )
