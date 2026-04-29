from datetime import datetime
from frame import Frame
from page_table import PageTable
from constants import PAGE_TABLE_LIMIT
class Node:
    def __init__(self, page):
        self.page = page
        self.prev = None
        self.next = None
class LRU:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_pages = set()
    def add(self, node):
        if node.page in self.current_pages: return 
        self.current_pages.add(node.page)
        node.next = node.prev = None # Clean stale pointers
        if not self.tail:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def remove(self, node):
        if not node or node.page not in self.current_pages: return
        self.current_pages.remove(node.page)
        if node.prev: node.prev.next = node.next
        else: self.head = node.next
        if node.next: node.next.prev = node.prev
        else: self.tail = node.prev
        node.next = node.prev = None # Prevent dangling references
    def move_to_end(self, node):
        if node == self.tail: return
        self.remove(node)
        self.add(node)

class MMU:
    def __init__(self, n):
        self.frames = [Frame(i) for i in range(n)]
        self.table = PageTable()
        self.lru = LRU()
        self.node_map = {}

    def _get_timestamp(self):
        return datetime.now()
    def _free(self):
        for f in self.frames:
            if f.page is None: return f
        return None
    def _victim(self):
        victim_node = self.lru.head
        if victim_node:
            self.lru.remove(victim_node)
        return victim_node
    def _cleanup(self):
        removed = []
        if len(self.table.entries) <= PAGE_TABLE_LIMIT:
            return removed 
        # Sort table by last access for housekeeping
        items = sorted(self.table.entries.items(), key=lambda x: x[1].last_access)
        while len(self.table.entries) > PAGE_TABLE_LIMIT:
            page, _ = items.pop(0)
            removed.append(page)
            if page in self.node_map:
                self.lru.remove(self.node_map[page])
                del self.node_map[page]
            self.table.unmap(page) 
        return removed
    def access(self, page):
        now = self._get_timestamp()
        e = self.table.get(page)
        if e and e.valid:
            if page in self.node_map:
                self.lru.move_to_end(self.node_map[page])
            e.access(now)
            return "HIT", self._cleanup()
        free = self._free()
        if not free:
            victim_node = self._victim()
            if victim_node:
                old_page = victim_node.page
                self.table.unmap(old_page) # Clears frame + removes entry
                if old_page in self.node_map:
                    del self.node_map[old_page]
                free = self._free() # Re-verify reclaimed frame
        if not free: free = self.frames[0] 
        free.page = page
        self.table.map(page, free, now)
        new_node = Node(page)
        self.lru.add(new_node)
        self.node_map[page] = new_node
        return "FAULT", self._cleanup()