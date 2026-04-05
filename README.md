# DataFlow Pro — NileMart ETL Engine

A high-performance Python ETL (Extract, Transform, Load) engine built for NileMart Inc.
The engine cleans, sorts, and structures raw sales data before it reaches Power BI dashboards.
Every phase is built around a core Data Structures & Algorithms concept.

---

## The Problem

NileMart's Business Intelligence team in Smart Village was experiencing hours-long Power BI
dashboard refresh times. The root cause: raw transaction data being fed directly into Power BI
was messy, unindexed, and unstructured. DataFlow Pro solves this by processing the data
in the backend before it ever reaches the visualization layer.

---

## Project Structure

```
dataflow_pro/
├── data/
│   └── sales_data.csv          # 10,000 NileMart transaction records
├── docs/
│   └── PERFORMANCE_REPORT.md   # Answers all Big-O questions from PDF
├── tests/
│   └── test_all_phases.py      # Validates all code works
├── src/
│   ├── phase1_indexer.py       # Sorting & Searching
│   ├── phase2_tracker.py       # Linked Lists
│   ├── phase3_parser.py        # Stacks
│   ├── phase4_buffer.py        # Queues
│   ├── phase5_trees.py         # Trees & BST
│   └── main.py                 # CLI entry point
├── requirements.txt
└── logs.txt
├── README.md
└── validate_submissions.py
```

---

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
cd src
python main.py
```

Or run any phase individually:

```bash
python phase1_indexer.py
python phase2_tracker.py
python phase3_parser.py
python phase4_buffer.py
python phase5_trees.py
```

---

## Phases

---

### Phase 1 — The Query Optimizer (Sorting & Searching)

**DSA:** Bubble Sort, Insertion Sort, Selection Sort, Merge Sort, Quick Sort, Binary Search, Bisect

Benchmarks five sorting algorithms against Python's built-in Timsort on 10,000 transaction
records sorted by Total Revenue. Implements Linear Search vs Binary Search for fraud detection
on Order IDs, and uses Python's `bisect` module to instantly slice time-series data by date range.

**Output:**

```
==================================================
  SORT BENCHMARK  |  key: 'Total Revenue'  |  n=10,000
==================================================
  Bubble Sort     → 5.9377s
  Insertion Sort  → 2.4919s
  Selection Sort  → 3.1285s
  Merge Sort      → 0.0207s
  Quick Sort      → 0.0241s
  Timsort (built-in) → 0.0019s

==================================================
  SEARCH BENCHMARK  |  Target Order ID: 773452794
==================================================
  Linear Search (unsorted) → 0.000010s | Found: True
  Binary Search (sorted)   → 0.000010s | Found: True

  Order ID : 773452794
  Country  : Zambia
  Revenue  : 148,926.80
  Profit   : 64,139.16

[Bisect] 7/1/2015 → 9/30/2015 | 348 transactions found.
[Bisect] Total Q3 2015 Revenue: 455,808,486.12
```

**Why it matters:** Bubble Sort took 5.9s vs Timsort's 0.0019s on the same dataset.
For a dashboard refreshing hundreds of tables daily, this difference is the gap between
a usable product and an unusable one.

---

### Phase 2 — The Applied Steps Tracker (Linked Lists)

**DSA:** Singly Linked List, Doubly Linked List

Recreates Power Query's transformation tracking system. The Singly Linked List records
each ETL step. The Doubly Linked List upgrades this into a full Undo/Redo engine, allowing
analysts to navigate forward and backward through their transformation history in O(1) time.

**Output:**

```
--- Part 1: Singly Linked List ---
[Singly] Transformation History:
  1. Removed Nulls
  2. Changed Type: Order ID to Integer
  3. Renamed Column: 'Total Revenue' to 'Revenue'
  4. Filtered: Sales Channel = Online
[Singly] Removed step: 'Filtered: Sales Channel = Online'

--- Part 2: Doubly Linked List (Undo/Redo Engine) ---
[Tracker] Undo → removed 'Filtered: Region = Sub-Saharan Africa'
[Tracker] Undo → removed 'Renamed Column: Total Revenue to Revenue'

[Tracker] Full Step History (head → tail):
  1. Removed Nulls
  2. Changed Type: Order ID to Integer  ← current
  3. Renamed Column: 'Total Revenue' to 'Revenue'
  4. Filtered: Region = Sub-Saharan Africa

[Tracker] Redo → restored 'Renamed Column: Total Revenue to Revenue'
[Tracker] Applied step: 'Sorted by Total Profit Descending'

[Tracker] Reverse History (tail → head):
  5. Sorted by Total Profit Descending
  4. Renamed Column: 'Total Revenue' to 'Revenue'
  3. Changed Type: Order ID to Integer
  2. Removed Nulls
```

---

### Phase 3 — The DAX Formula Parser (Stacks)

**DSA:** Array Stack, Linked List Stack, Shunting-Yard Algorithm

Evaluates custom KPI formulas written by analysts. Implements two Stack representations.
Uses the Shunting-Yard algorithm to convert infix expressions into postfix notation and
evaluate them. Also validates parentheses matching in complex DAX formulas.

**Output:**

```
--- Postfix Expression Evaluator ---
  Postfix : 15000 5000 + 2 *
  Meaning : (15000 + 5000) * 2
  Result  : 40,000.00

  Postfix : 850000 340000 - 0.15 *
  Meaning : (Revenue - Cost) * Tax 15%
  Result  : 76,500.00

--- Parentheses Validator ---
  ✓ Valid   → CALCULATE(SUM([Revenue]), FILTER([Region], [Region] = "Africa"))
  ✓ Valid   → IF(([Revenue] - [Cost]) > 0, "Profit", "Loss")
  ✗ Invalid → SUMX(Sales, [Units Sold] * [Unit Price]
  ✗ Invalid → DIVIDE([Revenue], [Cost])) * 100

--- Infix to Postfix Converter (Shunting-Yard) ---
  Infix   : ( 15000 + 5000 ) * 2
  Postfix : 15000 5000 + 2 *
  Result  : 40,000.00

  Infix   : 850000 - 340000 * 0.15
  Postfix : 850000 340000 0.15 * -
  Result  : 799,000.00

  Infix   : ( 9 / 3 ) * ( 4 - 2 )
  Postfix : 9 3 / 4 2 - *
  Result  : 6.00
```

---

### Phase 4 — The Live Data Buffer (Queues)

**DSA:** List-based Queue, Linked List Queue, collections.deque

Handles live streaming sales data during peak events like White Friday. Implements three
Queue versions to demonstrate the O(n) performance trap of list-based queues vs the O(1)
performance of deque-based queues.

**Output:**

```
--- Live Ingestion Queue (White Friday Simulation) ---
[Buffer] Enqueued: {'txn': 1045, 'branch': 'Maadi',    'amt_egp': 850}
[Buffer] Enqueued: {'txn': 1046, 'branch': 'Smouha',   'amt_egp': 3200}
[Buffer] Enqueued: {'txn': 1047, 'branch': 'Zayed',    'amt_egp': 1750}
[Buffer] Enqueued: {'txn': 1048, 'branch': 'Mansoura', 'amt_egp': 620}
[Buffer] Enqueued: {'txn': 1049, 'branch': 'Maadi',    'amt_egp': 4400}

[Buffer] 5 transactions waiting in queue.
[Buffer] Processed 3 transactions → pushing to Power BI...
[Buffer] 2 transactions still in queue.
[Buffer] Processed 2 transactions → pushing to Power BI...
[Buffer] 0 transactions still in queue.

--- Queue Performance Benchmark ---
  ListQueue   (n=10,000) → 0.1104s  [O(n) dequeue]
  LinkedQueue (n=10,000) → 0.0035s  [O(1) dequeue]
  deque       (n=10,000) → 0.0005s  [O(1) dequeue]
```

**Why it matters:** The list-based queue was 220x slower than deque on 10,000 rows.
During White Friday when thousands of transactions pour in per second, that difference
would crash the ingestion pipeline.

---

### Phase 5 — The Hierarchical Matrix Builder (Trees)

**DSA:** Binary Search Tree, N-ary Tree, Recursive Traversal

Models Parent-Child relationships for Power BI matrix visuals and drill-downs.
Builds a BST to index unique Customer IDs for fast lookups, and an N-ary organizational
tree using `anytree`. A recursive roll-up function aggregates sales from leaf nodes up
to any manager node.

**Output:**

```
--- Part 1: Binary Search Tree (Customer Dimension Index) ---
[BST] Inorder traversal (sorted by National ID):
  5072000   →  Nour Adel
  10042003  →  Omar Tarek
  15031985  →  Sara Mohamed
  18092010  →  Youssef Karim
  22081990  →  Khaled Ali
  29051997  →  Ahmed Hassan
  30121978  →  Mona Samir

[BST] Searching for customers:
  Found     → ID: 22081990  Name: Khaled Ali
  Not found → ID: 99999999

--- Part 2: N-ary Organizational Chart ---
Omar (Global CEO)  (Direct Sales: 0 EGP)
├── Tarek (VP Cairo & Giza)  (Direct Sales: 0 EGP)
│   ├── Aya (Maadi Branch Rep)  (Direct Sales: 150,000 EGP)
│   └── Mahmoud (Zayed Branch Rep)  (Direct Sales: 270,000 EGP)
└── Salma (VP Alex & Delta)  (Direct Sales: 0 EGP)
    ├── Kareem (Smouha Branch Rep)  (Direct Sales: 180,000 EGP)
    └── Nour (Mansoura Branch Rep)  (Direct Sales: 120,000 EGP)

[Roll-Up] Calculating total sales per region:
  Tarek (VP Cairo & Giza)  → 420,000 EGP
  Salma (VP Alex & Delta)  → 300,000 EGP
  Omar  (Global CEO)       → 720,000 EGP  (entire company)
```

---

## Big-O Performance Summary

| Operation | Algorithm | Complexity |
|---|---|---|
| Sorting (slow) | Bubble / Insertion / Selection Sort | O(n²) |
| Sorting (fast) | Merge Sort / Quick Sort | O(n log n) |
| Sorting (best) | Timsort built-in | O(n log n) optimized |
| Search unsorted | Linear Search | O(n) |
| Search sorted | Binary Search | O(log n) |
| Date range slice | Bisect | O(log n) |
| Linked List append | Singly (no tail) | O(n) |
| Undo / Redo | Doubly Linked List | O(1) |
| Stack push / pop | Array & Linked Stack | O(1) |
| Queue dequeue (bad) | List-based | O(n) |
| Queue dequeue (good) | deque / Linked List | O(1) |
| BST insert / search | Binary Search Tree | O(log n) avg |
| Sales roll-up | Recursive tree traversal | O(n) |

---

## Dependencies

- `anytree` — N-ary tree structure for the organizational chart (Phase 5)

---

## Dataset

`sales_data.csv` contains 10,000 sales transactions across global NileMart branches with
14 fields: Region, Country, Item Type, Sales Channel, Order Priority, Order Date, Order ID,
Ship Date, Units Sold, Unit Price, Unit Cost, Total Revenue, Total Cost, Total Profit.

---

*ITI Port Said | PowerBI46R2 | DSA Project | DataFlow Pro*
