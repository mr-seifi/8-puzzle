import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def is_empty(self):
        return len(self._queue) == 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def remove(self):
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return heapq.heappop(self._queue)[-1]

    def __len__(self):
        return len(self._queue)