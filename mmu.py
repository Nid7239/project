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

        node.prev = node.next = None

    def move_to_end(self, node):
        self.remove(node)
        self.add(node)

    def pop(self):
        if not self.head:
            return None
        node = self.head
        self.remove(node)
        return node

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

    def _smart_victim(self):
        candidates = []
        curr = self.lru.head

        while curr:
            entry = self.table.get(curr.page)
            if entry and entry.valid:
                candidates.append((entry.reference, entry.last_access, curr))
            curr = curr.next

        if not candidates:
            return None

        candidates.sort(key=lambda x: (x[0], x[1]))
        victim = candidates[0][2]

        self.lru.remove(victim)
        return victim

    def cleanup(self):
        removed = []

        if len(self.table.entries) <= PAGE_TABLE_LIMIT:
            return removed

        items = sorted(
            self.table.entries.items(),
            key=lambda x: x[1].last_access
        )

# remove invalid entries
        i = 0
        while len(self.table.entries) > PAGE_TABLE_LIMIT and i < len(items):
            page, entry = items[i]

            if entry.valid == 0:
                removed.append(page)

                if page in self.map:
                    self.lru.remove(self.map[page])
                    del self.map[page]

                del self.table.entries[page]

            i += 1

   
        while len(self.table.entries) > PAGE_TABLE_LIMIT:
            node = self._smart_victim()
            if not node:
                break

            page = node.page
            removed.append(page)

            entry = self.table.get(page)

            if entry and entry.valid:
                node.frame.page = None

            if page in self.map:
                del self.map[page]

            del self.table.entries[page]

        return removed

    def access(self, page):
        e = self.table.get(page)

        # HIT
        if e and e.valid:
            node = self.map[page]
            self.lru.move_to_end(node)
            e.access()

            removed = []
            if len(self.table.entries) > PAGE_TABLE_LIMIT:
                removed = self.cleanup()

            return "HIT", removed

        # FAULT
        free = self._free()

        if free:
            free.page = page
            self.table.map(page, free)

            node = Node(page, free)
            self.lru.add(node)
            self.map[page] = node

            removed = []
            if len(self.table.entries) > PAGE_TABLE_LIMIT:
                removed = self.cleanup()

            return "FAULT", removed

        # Replacement
        victim = self._smart_victim()
        old_page = victim.page

        self.table.unmap(old_page)
        victim.frame.page = page
        self.table.map(page, victim.frame)

        if old_page in self.map:
            del self.map[old_page]

        node = Node(page, victim.frame)
        self.lru.add(node)
        self.map[page] = node

        removed = [old_page]
        if len(self.table.entries) > PAGE_TABLE_LIMIT:
            removed += self.cleanup()

        return "FAULT", removed