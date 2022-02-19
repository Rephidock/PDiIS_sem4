from __future__ import annotations
from typing import Callable
from queue import Queue


class MethodQueue:

    __methods: Queue[Callable]
    __params: Queue[tuple]

    def __init__(self):
        self.__methods = Queue()
        self.__params = Queue()
        pass

    def enqueue(self, method: Callable, *args) -> None:
        self.__methods.put(method)
        self.__params.put(args)

    def perform(self) -> None:
        while not self.__methods.empty():
            self.__methods.get()(*(self.__params.get()))
