import time
from collections import deque


# ── List-based Queue (slow) ───────────────────────────────────────────────────

class ListQueue:
    def __init__(self):
        self.data = []

    def enqueue(self, row):
        self.data.append(row)

    def dequeue(self):
        if self.is_empty():
            print("[ListQueue] Queue is empty.")
            return None
        return self.data.pop(0)  # O(n) — shifts every element left

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)


# ── Linked List Queue (O(1) both ends) ───────────────────────────────────────

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, row):
        node = QueueNode(row)
        if self.tail:
            self.tail.next = node
        self.tail = node
        if self.head is None:
            self.head = node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            print("[LinkedQueue] Queue is empty.")
            return None
        value     = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return value

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size


# ── Deque-based Queue (production) ───────────────────────────────────────────

class LiveIngestionQueue:
    def __init__(self):
        self.buffer = deque()

    def enqueue_row(self, row):
        self.buffer.append(row)
        print(f"[Buffer] Enqueued: {row}")

    def process_batch(self, batch_size):
        processed = []
        for _ in range(batch_size):
            if not self.buffer:
                break
            processed.append(self.buffer.popleft())
        print(f"[Buffer] Processed {len(processed)} transactions → pushing to Power BI...")
        return processed

    def is_empty(self):
        return len(self.buffer) == 0

    def size(self):
        return len(self.buffer)


# ── Benchmark ─────────────────────────────────────────────────────────────────

def benchmark_queues(n=10000):
    print("\n--- Queue Performance Benchmark ---")
    sample_rows = [{"txn": i, "branch": "Maadi", "amt_egp": i * 10} for i in range(n)]

    # List Queue
    q = ListQueue()
    start = time.perf_counter()
    for row in sample_rows:
        q.enqueue(row)
    for _ in range(n):
        q.dequeue()
    print(f"  ListQueue   (n={n:,}) → {time.perf_counter() - start:.4f}s  [O(n) dequeue]")

    # Linked Queue
    q = LinkedQueue()
    start = time.perf_counter()
    for row in sample_rows:
        q.enqueue(row)
    for _ in range(n):
        q.dequeue()
    print(f"  LinkedQueue (n={n:,}) → {time.perf_counter() - start:.4f}s  [O(1) dequeue]")

    # Deque Queue
    q = deque()
    start = time.perf_counter()
    for row in sample_rows:
        q.append(row)
    for _ in range(n):
        q.popleft()
    print(f"  deque       (n={n:,}) → {time.perf_counter() - start:.4f}s  [O(1) dequeue]")


# ── Phase 4 Runner ────────────────────────────────────────────────────────────

def run_phase4():
    print("\n" + "=" * 50)
    print("  PHASE 4: THE LIVE DATA BUFFER")
    print("=" * 50)

    # --- Live Ingestion Demo ---
    print("\n--- Live Ingestion Queue (White Friday Simulation) ---")
    buffer = LiveIngestionQueue()

    buffer.enqueue_row({"txn": 1045, "branch": "Maadi",   "amt_egp": 850})
    buffer.enqueue_row({"txn": 1046, "branch": "Smouha",  "amt_egp": 3200})
    buffer.enqueue_row({"txn": 1047, "branch": "Zayed",   "amt_egp": 1750})
    buffer.enqueue_row({"txn": 1048, "branch": "Mansoura","amt_egp": 620})
    buffer.enqueue_row({"txn": 1049, "branch": "Maadi",   "amt_egp": 4400})

    print(f"\n[Buffer] {buffer.size()} transactions waiting in queue.")
    batch = buffer.process_batch(3)
    print(f"[Buffer] {buffer.size()} transactions still in queue.")
    batch = buffer.process_batch(10)
    print(f"[Buffer] {buffer.size()} transactions still in queue.")

    # --- Benchmark ---
    benchmark_queues(n=10000)


if __name__ == '__main__':
    run_phase4()