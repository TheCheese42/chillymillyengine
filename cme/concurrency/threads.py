"""
Threaded solution for concurrency problems.
"""

import threading
from typing import Any, Callable, Iterable, Mapping, Optional


def start_helper_thread(
    *,
    target: Callable,
    name: Optional[str] = None,
    args: Iterable[Any] = (),
    kwargs: Optional[Mapping[str, Any]] = None,
    daemon: Optional[bool] = None,
    callback: Optional[Callable] = None,
) -> None:
    """
    Opens a helper thread for blocking tasks to not block the mainloop. If
    you experience lag in the mainloop please consider using `worker_process`
    to leverage a second CPU.
    You can specify a `callback` function to get notified when the thread has
    finished.
    """
    def wrapper(*args, **kwargs):
        target(*args, **kwargs)
        if callback:
            callback()

    thread = threading.Thread(
        target=wrapper,
        name=name,
        args=args,
        kwargs=kwargs,
        daemon=daemon,
    )
    thread.start()
