import heapq
import itertools

# Point
class Point:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

# Segment
class Seg:
    start = None
    end = None
    finished = False

    def __init__(self, p):
        self.start = p
        self.end = None
        self.finished = False

    def finish(self, p):
        if self.finished:
            return
        self.end = p
        self.finished = True


# tree structure
class Arc:
    p = None  # point
    pre = None  # two arcs
    next = None
    e = None  # event
    s0 = None  # two segments
    s1 = None  # pre and next

    def __init__(self, p, a=None, b=None):
        self.p = p
        self.pre = a
        self.next = b
        self.e = None
        self.s0 = None
        self.s1 = None

# circle event
class Event:
    x = 0.0
    p = None  # point
    a = None  # arc
    valid = True

    def __init__(self, x, p, a):
        self.x = x
        self.p = p
        self.a = a
        self.valid = True


class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.set = {}
        self.counter = itertools.count()

    def push(self, value):
        # if already exist
        if value in self.set:
            return
        count = next(self.counter)
        # use x as a determining key
        entry = [value.x, count, value]
        self.set[value] = entry
        heapq.heappush(self.pq, entry)

    def pop(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.set[item]
                return item
        raise KeyError('Cannot pop. It is empty ')

    def remove_entry(self, value):
        entry = self.set.pop(value)
        entry[-1] = 'Removed'

    def top(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.set[item]
                self.push(item)
                return item
        raise KeyError('Nothing here, it is empty')

    def empty(self):
        return not self.pq
