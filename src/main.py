import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phase1_indexer import run_phase1, load_data, benchmark_sorts, benchmark_search, extract_date_range
from phase2_tracker import run_phase2, AppliedStepsTracker
from phase3_parser  import run_phase3, DAXEvaluator
from phase4_buffer  import run_phase4, LiveIngestionQueue
from phase5_trees   import run_phase5, OrgChartAnalyzer


BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE, 'data', 'sales_data.csv')


def print_header():
    print("=" * 50)
    print("   DataFlow Pro — NileMart ETL Engine")
    print("   Powered by DSA | ITI Port Said")
    print("=" * 50)


def main_menu():
    print("\nMain Menu:")
    print("  1. Run Phase 1 — Query Optimizer    (Sorting & Searching)")
    print("  2. Run Phase 2 — Applied Steps      (Linked Lists)")
    print("  3. Run Phase 3 — DAX Formula Parser (Stacks)")
    print("  4. Run Phase 4 — Live Data Buffer   (Queues)")
    print("  5. Run Phase 5 — Hierarchical Matrix(Trees)")
    print("  6. Run All Phases")
    print("  7. Interactive Mode")
    print("  0. Exit")


def interactive_mode():
    print("\n" + "=" * 50)
    print("  INTERACTIVE MODE")
    print("=" * 50)

    tracker = AppliedStepsTracker()
    dax     = DAXEvaluator()
    buffer  = LiveIngestionQueue()
    org     = OrgChartAnalyzer()

    while True:
        print("\nInteractive Menu:")
        print("  1. Add ETL transformation step")
        print("  2. Undo last step")
        print("  3. Redo step")
        print("  4. Show step history")
        print("  5. Evaluate a postfix DAX expression")
        print("  6. Validate parentheses in a DAX formula")
        print("  7. Enqueue a live transaction")
        print("  8. Process transaction batch")
        print("  9. Show org chart & roll-up sales")
        print("  0. Back to main menu")

        choice = input("\nSelect: ").strip()

        if choice == '1':
            step = input("Enter transformation step: ").strip()
            tracker.add_step(step)
            tracker.print_history()

        elif choice == '2':
            tracker.undo()
            tracker.print_history()

        elif choice == '3':
            tracker.redo()
            tracker.print_history()

        elif choice == '4':
            tracker.print_history()

        elif choice == '5':
            print("Example: 15000 5000 + 2 *  means (15000 + 5000) * 2")
            expr   = input("Enter postfix expression: ").strip()
            result = dax.evaluate_postfix(expr)
            if result is not None:
                print(f"Result: {result:,.2f}")

        elif choice == '6':
            formula = input("Enter DAX formula: ").strip()
            valid   = dax.validate_parentheses(formula)
            print(f"  {'✓ Valid' if valid else '✗ Invalid'} parentheses")

        elif choice == '7':
            try:
                txn    = int(input("Transaction ID : ").strip())
                branch = input("Branch name    : ").strip()
                amt    = float(input("Amount (EGP)   : ").strip())
                buffer.enqueue_row({"txn": txn, "branch": branch, "amt_egp": amt})
                print(f"[Buffer] {buffer.size()} transaction(s) waiting.")
            except ValueError:
                print("Invalid input, please enter correct values.")

        elif choice == '8':
            try:
                n = int(input("Batch size: ").strip())
                buffer.process_batch(n)
                print(f"[Buffer] {buffer.size()} transaction(s) still waiting.")
            except ValueError:
                print("Invalid input.")

        elif choice == '9':
            org.display_chart()
            print(f"\n  Tarek (VP Cairo & Giza) → {org.roll_up_sales(org.vp_cairo):,} EGP")
            print(f"  Salma (VP Alex & Delta) → {org.roll_up_sales(org.vp_alex):,} EGP")
            print(f"  Omar  (Global CEO)      → {org.roll_up_sales(org.ceo):,} EGP")

        elif choice == '0':
            break

        else:
            print("Invalid choice, try again.")


def main():
    print_header()

    while True:
        main_menu()
        choice = input("\nSelect: ").strip()

        if choice == '1':
            run_phase1(CSV_PATH)

        elif choice == '2':
            run_phase2()

        elif choice == '3':
            run_phase3()

        elif choice == '4':
            run_phase4()

        elif choice == '5':
            run_phase5()

        elif choice == '6':
            run_phase1(CSV_PATH)
            run_phase2()
            run_phase3()
            run_phase4()
            run_phase5()

        elif choice == '7':
            interactive_mode()

        elif choice == '0':
            print("\nShutting down DataFlow Pro. Masalama! 👋")
            sys.exit()

        else:
            print("Invalid choice, try again.")


if __name__ == '__main__':
    main()
