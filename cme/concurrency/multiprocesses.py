"""
Multiprocessing solution for concurrency problems. Allows the program to make
use of multiple CPUs.
"""


import multiprocessing
from typing import Any, Callable, Iterable, Mapping, Optional

# Just in case someone wants to package their game
multiprocessing.freeze_support()


def start_worker_process(
    *,
    target: Callable[[], None],
    name: Optional[str] = None,
    args: Iterable[Any] = (),
    kwargs: Mapping[str, Any] = {},
    daemon: Optional[bool] = None,
    callback: Optional[Callable[[], None]] = None,
) -> None:
    """
    Opens a worker process for heavy, blocking tasks. Enables usage of multiple
    CPUs. If this is not required `start_helper_thread` might be a better pick.
    You can specify a `callback` function to get notified when the process has
    finished.
    """
    def wrapper(*args: tuple[Any], **kwargs: Mapping[Any, Any]):
        target(*args, **kwargs)
        if callback:
            callback()
    process = multiprocessing.Process(
        target=wrapper,
        name=name,
        args=args,
        kwargs=kwargs,
        daemon=daemon,
    )
    process.start()
