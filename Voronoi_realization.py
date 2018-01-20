import math
from data_structure import Point, Seg, Arc, Event, PriorityQueue

class Voronoi:
    def __init__(self, points):
        self.output = []  # Result, a list of segment
        self.arc = None  # parabola arcs
        self.event = PriorityQueue()  # circle events, old arc disappears
        self.points = PriorityQueue()  # site event, new arc appears
        # make an origin bounding box
        self.x0 = -0.0 # these value can be changed
        self.x1 = -0.0
        self.y0 = 0.0
        self.y1 = 0.0
        # insert points
        for ps in points:
            point = Point(ps[0], ps[1])
            self.points.push(point)
            # update bounding box
            if point.x < self.x0:
                self.x0 = point.x
            if point.y < self.y0:
                self.y0 = point.y
            if point.x > self.x1:
                self.x1 = point.x
            if point.y > self.y1:
                self.y1 = point.y
        # The follow can also be skipped
        dx = (self.x1 - self.x0 + 1) / 10.0
        dy = (self.y1 - self.y0 + 1) / 10.0
        self.x0 = self.x0 - dx
        self.x1 = self.x1 + dx
        self.y0 = self.y0 - dy
        self.y1 = self.y1 + dy

    # main process
    def process(self):
        # deal with points
        while not self.points.empty():
            if not self.event.empty() and (self.points.top().x >= self.event.top().x):
                self.circle_event()  # circle event
            else:
                self.site_event()  # site event
        # deal with remaining circle events
        while not self.event.empty():
            self.circle_event()
        # get segment and finish the edge
        self.finish_edge()

    def finish_edge(self):
        val = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        a = self.arc
        while a.next is not None:
            if a.s1 is not None:
                # find the intersected point and make it finished point of s1
                p = self.intersection(a.p, a.next.p, val * 3.0)
                a.s1.finish(p)
            a = a.next # until this is no arc

    def circle_event(self):
        # get event
        e = self.event.pop()
        if e.valid:
            # add an edge
            s = Seg(e.p)
            self.output.append(s)
            # remove the nearby parabola
            a = e.a
            if a.pre is not None:
                a.pre.next = a.next
                a.pre.s1 = s
            if a.next is not None:
                a.next.pre = a.pre
                a.next.s0 = s
            # finish the edge
            if a.s0 is not None:
                a.s0.finish(e.p)
            if a.s1 is not None:
                a.s1.finish(e.p)
            # recheck
            if a.pre is not None:
                self.check_cEvent(a.pre, e.x)
            if a.next is not None:
                self.check_cEvent(a.next, e.x)

        def site_event(self):
            # get new point from points
            p = self.points.pop()
            # add new arc
            self.addArc(p)

    def check_cEvent(self, a, x0):
        # find new circle event at arc a
        if (a.e is not None) and (a.e.x != self.x0):
            a.e.valid = False
        a.e = None
        if (a.pre is None) or (a.next is None):
            return
        visited, x, o = self.circle(a.pre.p, a.p, a.next.p)
        if visited and (x > self.x0):
            a.e = Event(x, o, a)
            self.event.push(a.e)

    def addArc(self, p):
        if self.arc is None:
            self.arc = Arc(p)
        else:
            # find the existing arc
            a = self.arc
            while a is not None:
                visited, z = self.intersect(p, a)
                if visited:
                    visited, zz = self.intersect(p, a.next)
                    if (a.next is not None) and (not visited):
                        a.next.pre = Arc(a.p, a, a.next)
                        a.next = a.next.pre
                    else:
                        a.next = Arc(a.p, a)
                    a.next.s1 = a.s1
                    # add p between a and a.next
                    a.next.pre = Arc(p, a, a.next)
                    a.next = a.next.pre
                    a = a.next  # a is new arc now
                    # create and connect the new line
                    seg = Seg(z)
                    self.output.append(seg)
                    a.pre.s1 = a.s0 = seg
                    seg = Seg(z)
                    self.output.append(seg)
                    a.next.s0 = a.s1 = seg
                    # check cir event of this new arc
                    self.check_cEvent(a, p.x)
                    self.check_cEvent(a.pre, p.x)
                    self.check_cEvent(a.next, p.x)
                    return
                a = a.next
            # if p never intersects an arc, append it to the list
            a = self.arc
            while a.next is not None:
                a = a.next
            a.next = Arc(p, a)
            # insert new seg
            x = self.x0
            y = (a.next.p.y + a.p.y) / 2.0
            start = Point(x, y)
            seg = Seg(start)
            a.s1 = a.next.s0 = seg
            self.output.append(seg)

    def circle(self, a, b, c):
        # check if bc is a "right turn" from ab
        if ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) > 0:
            return False, None, None
        # This method is learned from Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))
        if (G == 0):
            return False, None, None  # Points are co-linear
        # point o is the center of the circle
        ox = 1.0 * (D * E - B * F) / G
        oy = 1.0 * (A * F - C * E) / G
        x = ox + math.sqrt((a.x - ox) ** 2 + (a.y - oy) ** 2)  # o.x plus radius equals max x coord
        o = Point(ox, oy)  # the centre of a circle;
        return True, x, o

    def intersect(self, p, a):
        # check if the parabola of p intersect with a acr a
        # return a visited flag and a point
        if (a is None) or (a.p.x == p.x):
            return False, None
        o1 = 0.0
        o2 = 0.0
        if a.pre is not None:
            o1 = (self.intersection(a.pre.p, a.p, 1.0 * p.x)).y
        if a.next is not None:
            o2 = (self.intersection(a.p, a.next.p, 1.0 * p.x)).y
        # Find the intersection of point
        if ((a.pre is None) or (o1 <= p.y)) and ((a.next is None) or (o2 >= p.y)):
            py = p.y
            px = 1.0 * (a.p.x ** 2 + (a.p.y - py) ** 2 - p.x ** 2) / (2 * a.p.x - 2 * p.x)
            res = Point(px, py)
            return True, res
        return False, None

    def intersection(self, p0, p1, xval):
        # find the intersection of two parabolas
        p = p0
        if p0.x == p1.x:
            py = (p0.y + p1.y) / 2.0
        elif p1.x == xval:
            py = p1.y
        elif p0.x == xval:
            py = p0.y
            p = p1
        else:
            # use quadratic formula
            z0 = 2.0 * (p0.x - xval)
            z1 = 2.0 * (p1.x - xval)
            # calculate the result , cross point
            a = 1.0 / z0 - 1.0 / z1
            b = -2.0 * (p0.y / z0 - p1.y / z1)
            c = 1.0 * (p0.y ** 2 + p0.x ** 2 - xval ** 2) / z0 - 1.0 * (p1.y ** 2 + p1.x ** 2 - xval ** 2) / z1

            py = 1.0 * (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

        px = 1.0 * (p.x ** 2 + (p.y - py) ** 2 - xval ** 2) / (2 * p.x - 2 * xval)
        res = Point(px, py)
        return res

    def get_res(self):
        res = []
        for ans in self.output:
            p0 = ans.start
            p1 = ans.end
            res.append((p0.x, p0.y, p1.x, p1.y))
        return res

