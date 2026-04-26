from frame import Frame
from page_table import PageTable
from constants import PAGE_TABLE_LIMIT


class Node:
    def __init__(self, page, frame):
        self.page = page
        self.frame = frame
        self.prev = None
        self.next = None


class LRU:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, node):
        if not self.tail:
            self.head = self.tail = node
            return
        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    def remove(self, node):
        if not node:
            return
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def move_to_end(self, node):
        self.remove(node)
        self.add(node)


class MMU:
    def __init__(self, n):
        self.frames = [Frame(i) for i in range(n)]
        self.table = PageTable()
        self.lru = LRU()
        self.map = {}

    def _free(self):
        for f in self.frames:
            if f.page is None:
                return f
        return None

    def _victim(self):
        candidates = []
        curr = self.lru.head

        while curr:
            e = self.table.get(curr.page)
            if e and e.valid:
                candidates.append((e.reference, e.last_access, curr))
            curr = curr.next

        candidates.sort(key=lambda x: (x[0], x[1]))
        victim = candidates[0][2]
        self.lru.remove(victim)
        return victim

    def _cleanup(self):
        removed = []

        if len(self.table.entries) <= PAGE_TABLE_LIMIT:
            return removed

        items = sorted(
            self.table.entries.items(),
            key=lambda x: x[1].last_access
        )

        while len(self.table.entries) > PAGE_TABLE_LIMIT:
            page, entry = items.pop(0)
            removed.append(page)

            if page in self.map:
                self.lru.remove(self.map[page])
                del self.map[page]

            del self.table.entries[page]

        return removed

    def access(self, page):
        e = self.table.get(page)

        # HIT
        if e and e.valid:
            self.lru.move_to_end(self.map[page])
            e.access()
            return "HIT", self._cleanup()

        # FAULT
        free = self._free()

        if free:
            free.page = page
            self.table.map(page, free)

            node = Node(page, free)
            self.lru.add(node)
            self.map[page] = node

            return "FAULT", self._cleanup()

        # Replacement
        victim = self._victim()
        old_page = victim.page

        self.table.unmap(old_page)

        victim.frame.page = page
        self.table.map(page, victim.frame)

        if old_page in self.map:
            del self.map[old_page]

        node = Node(page, victim.frame)
        self.lru.add(node)
        self.map[page] = node

        return "FAULT", self._cleanup()