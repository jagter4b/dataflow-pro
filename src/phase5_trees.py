from anytree import Node, RenderTree


# ── Binary Search Tree ────────────────────────────────────────────────────────

class BSTNode:
    def __init__(self, national_id, name):
        self.national_id = national_id
        self.name        = name
        self.left        = None
        self.right       = None


class DimensionIndex:
    def __init__(self):
        self.root = None

    def insert(self, national_id, name):
        if self.root is None:
            self.root = BSTNode(national_id, name)
        else:
            self._insert(self.root, national_id, name)

    def _insert(self, node, national_id, name):
        if national_id < node.national_id:
            if node.left is None:
                node.left = BSTNode(national_id, name)
            else:
                self._insert(node.left, national_id, name)
        elif national_id > node.national_id:
            if node.right is None:
                node.right = BSTNode(national_id, name)
            else:
                self._insert(node.right, national_id, name)
        else:
            print(f"[BST] ID {national_id} already exists, skipping.")

    def search(self, national_id):
        return self._search(self.root, national_id)

    def _search(self, node, national_id):
        if node is None:
            return None
        if national_id == node.national_id:
            return node
        elif national_id < node.national_id:
            return self._search(node.left, national_id)
        else:
            return self._search(node.right, national_id)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.national_id, node.name))
            self._inorder(node.right, result)


# ── N-ary Organizational Chart ────────────────────────────────────────────────

class OrgChartAnalyzer:
    def __init__(self):
        self.ceo     = Node("Omar (Global CEO)",          sales=0)
        self.vp_cairo = Node("Tarek (VP Cairo & Giza)",   sales=0,      parent=self.ceo)
        self.vp_alex  = Node("Salma (VP Alex & Delta)",   sales=0,      parent=self.ceo)

        Node("Aya (Maadi Branch Rep)",      parent=self.vp_cairo, sales=150000)
        Node("Mahmoud (Zayed Branch Rep)",  parent=self.vp_cairo, sales=270000)
        Node("Kareem (Smouha Branch Rep)",  parent=self.vp_alex,  sales=180000)
        Node("Nour (Mansoura Branch Rep)",  parent=self.vp_alex,  sales=120000)

    def display_chart(self):
        print("\n[Org Chart] NileMart Hierarchy:")
        for pre, _, node in RenderTree(self.ceo):
            print(f"{pre}{node.name}  (Direct Sales: {node.sales:,} EGP)")

    def roll_up_sales(self, node):
        total = node.sales
        for child in node.children:
            total += self.roll_up_sales(child)
        return total


# ── Phase 5 Runner ────────────────────────────────────────────────────────────

def run_phase5():
    print("\n" + "=" * 50)
    print("  PHASE 5: THE HIERARCHICAL MATRIX BUILDER")
    print("=" * 50)

    # --- Part 1: BST Dimension Index ---
    print("\n--- Part 1: Binary Search Tree (Customer Dimension Index) ---")
    bst = DimensionIndex()

    customers = [
        (29051997, "Ahmed Hassan"),
        (15031985, "Sara Mohamed"),
        (22081990, "Khaled Ali"),
        (30121978, "Mona Samir"),
        (10042003, "Omar Tarek"),
        (5072000,  "Nour Adel"),
        (18092010, "Youssef Karim"),
    ]

    for national_id, name in customers:
        bst.insert(national_id, name)
        print(f"[BST] Inserted → ID: {national_id}  Name: {name}")

    print("\n[BST] Inorder traversal (sorted by National ID):")
    for national_id, name in bst.inorder():
        print(f"  {national_id}  →  {name}")

    print("\n[BST] Searching for customers:")
    for target in [22081990, 99999999]:
        result = bst.search(target)
        if result:
            print(f"  Found  → ID: {result.national_id}  Name: {result.name}")
        else:
            print(f"  Not found → ID: {target}")

    # --- Part 2: N-ary Org Chart ---
    print("\n--- Part 2: N-ary Organizational Chart ---")
    org = OrgChartAnalyzer()
    org.display_chart()

    print("\n[Roll-Up] Calculating total sales per region:")
    cairo_total = org.roll_up_sales(org.vp_cairo)
    alex_total  = org.roll_up_sales(org.vp_alex)
    ceo_total   = org.roll_up_sales(org.ceo)

    print(f"  Tarek (VP Cairo & Giza)  → {cairo_total:,} EGP")
    print(f"  Salma (VP Alex & Delta)  → {alex_total:,} EGP")
    print(f"  Omar  (Global CEO)       → {ceo_total:,} EGP  (entire company)")


if __name__ == '__main__':
    run_phase5()