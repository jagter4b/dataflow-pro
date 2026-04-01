class SinglyNode:
    def __init__(self, step):
        self.step = step
        self.next = None
 
 
class SinglyStepsTracker:
    def __init__(self):
        self.head = None
        self.size = 0
 
    def add_step(self, step):
        new_node = SinglyNode(step)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
        print(f"[Singly] Added step: '{step}'")
 
    def print_history(self):
        print("\n[Singly] Transformation History:")
        if self.head is None:
            print("  No steps recorded.")
            return
        current = self.head
        step_num = 1
        while current:
            print(f"  {step_num}. {current.step}")
            current = current.next
            step_num += 1
 
    def remove_last(self):
        if self.head is None:
            print("[Singly] Nothing to remove.")
            return
        if self.head.next is None:
            print(f"[Singly] Removed step: '{self.head.step}'")
            self.head = None
            self.size -= 1
            return
        current = self.head
        while current.next.next:
            current = current.next
        print(f"[Singly] Removed step: '{current.next.step}'")
        current.next = None
        self.size -= 1
 
 
#  Doubly Linked List 
 
class DoublyNode:
    def __init__(self, step):
        self.step = step
        self.prev = None
        self.next = None
 
 
class AppliedStepsTracker:
    def __init__(self):
        self.head    = None
        self.tail    = None
        self.current = None
        self.size    = 0
 
    def add_step(self, step):
        new_node = DoublyNode(step)
 
        # If we added a step after undoing, discard the future steps
        if self.current and self.current.next:
            self.current.next = None
            self.tail = self.current
 
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
 
        self.current = self.tail
        self.size += 1
        print(f"[Tracker] Applied step: '{step}'")
 
    def undo(self):
        if self.current is None:
            print("[Tracker] Nothing to undo.")
            return
        print(f"[Tracker] Undo → removed '{self.current.step}'")
        self.current = self.current.prev
 
    def redo(self):
        if self.current is None and self.head:
            self.current = self.head
        elif self.current and self.current.next:
            self.current = self.current.next
        else:
            print("[Tracker] Nothing to redo.")
            return
        print(f"[Tracker] Redo → restored '{self.current.step}'")
 
    def print_history(self):
        print("\n[Tracker] Full Step History (head → tail):")
        if self.head is None:
            print("  No steps recorded.")
            return
        current = self.head
        step_num = 1
        while current:
            marker = " ← current" if current is self.current else ""
            print(f"  {step_num}. {current.step}{marker}")
            current = current.next
            step_num += 1
 
    def print_reverse(self):
        print("\n[Tracker] Reverse History (tail → head):")
        if self.tail is None:
            print("  No steps recorded.")
            return
        current = self.tail
        step_num = self.size
        while current:
            print(f"  {step_num}. {current.step}")
            current = current.prev
            step_num -= 1
 
 
#  Phase 2 Runner 
 
def run_phase2():
    print("\n" + "=" * 50)
    print("  PHASE 2: THE APPLIED STEPS TRACKER")
    print("=" * 50)
 
    # --- Part 1: Singly Linked List ---
    print("\n--- Part 1: Singly Linked List ---")
    singly = SinglyStepsTracker()
    singly.add_step("Removed Nulls")
    singly.add_step("Changed Type: Order ID to Integer")
    singly.add_step("Renamed Column: 'Total Revenue' to 'Revenue'")
    singly.add_step("Filtered: Sales Channel = Online")
    singly.print_history()
    singly.remove_last()
    singly.print_history()
 
    #  Part 2: Doubly Linked List with Undo/Redo 
    print("\n--- Part 2: Doubly Linked List (Undo/Redo Engine) ---")
    tracker = AppliedStepsTracker()
    tracker.add_step("Removed Nulls")
    tracker.add_step("Changed Type: Order ID to Integer")
    tracker.add_step("Renamed Column: 'Total Revenue' to 'Revenue'")
    tracker.add_step("Filtered: Region = Sub-Saharan Africa")
    tracker.print_history()
 
    print()
    tracker.undo()
    tracker.undo()
    tracker.print_history()
 
    print()
    tracker.redo()
    tracker.print_history()
 
    print()
    tracker.add_step("Sorted by Total Profit Descending")
    tracker.print_history()
 
    print()
    tracker.print_reverse()
 
 
if __name__ == '__main__':
    run_phase2()