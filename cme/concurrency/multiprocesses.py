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
    target: Callable[[], Any],
    name: Optional[str] = None,
    args: Iterable[Any] = (),
    kwargs: Mapping[str, Any] = {},
    daemon: Optional[bool] = None,
    callback: Optional[Callable[[], None]] = None,
) -> multiprocessing.Queue:  # type: ignore[type-arg]
    """
    Opens a worker process for heavy, blocking tasks. Enables usage of multiple
    CPUs. If this is not required `start_helper_thread` might be a better pick.
    You can specify a `callback` function to get notified when the process has
    finished. Be aware that you cannot change things over different processes.
    For that, use the multiprocessing.Queue object returned by this function,
    as it contains the target's return value.
    """
    def wrapper(
        queue: multiprocessing.Queue[Any],
        *args: tuple[Any],
        **kwargs: Mapping[Any, Any],
    ) -> None:
        output = target(*args, **kwargs)
        queue.put(output)
        if callback:
            callback()
    queue: multiprocessing.Queue[Any] = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=wrapper,
        name=name,
        args=(queue, *args),
        kwargs=kwargs,
        daemon=daemon,
    )
    process.start()
    return queue


def setup_worker_process(
    *,
    target: Callable[[], Any],
    name: Optional[str] = None,
    daemon: Optional[bool] = None,
) -> multiprocessing.Queue:  # type: ignore[type-arg]
    """
    Set up a permanent worker process processing on demand. This can be useful
    to avoid process create overhead. To use, simply store the queue returned
    by this function and .put() something in when required. This value should
    consist of a tuple with the first item being a `multiprocessing.Queue`
    object that will contain the target's return value. The remaining tuple
    content will be passed as positional arguments to `target`.

    :param target: A callable to be called on demand infinitely
    :type target: Callable[[], Any]
    :param name: The process name, defaults to None
    :type name: Optional[str], optional
    :param daemon: Wether the process is gonna be a daemon, defaults to None
    :type daemon: Optional[bool], optional
    :return: A queue to put arguments for `target` into, on demand
    :rtype: multiprocessing.Queue
    """
    def wrapper(queue: multiprocessing.Queue[Any]) -> None:
        while True:
            args = queue.get()
            out_queue = args[0]
            output = target(*args[1:])
            out_queue.put(output)
    queue: multiprocessing.Queue[Any] = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=wrapper,
        name=name,
        args=(queue,),
        daemon=daemon,
    )
    process.start()
    return queue
