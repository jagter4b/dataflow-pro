class ArrayStack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)


#  Linked List Stack 

class StackNode:
    def __init__(self, value):
        self.value = value
        self.next  = None


class LinkedStack:
    def __init__(self):
        self.top  = None
        self._size = 0

    def push(self, item):
        node      = StackNode(item)
        node.next = self.top
        self.top  = node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        value    = self.top.value
        self.top = self.top.next
        self._size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.top.value

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size


#  DAX Evaluator 

class DAXEvaluator:

    def evaluate_postfix(self, expression):
        """
        Evaluates a postfix (Reverse Polish Notation) expression.
        Example: '15000 5000 + 2 *'  →  (15000 + 5000) * 2  →  40000
        Tokens are separated by spaces.
        """
        stack = ArrayStack()
        tokens = expression.strip().split()

        for token in tokens:
            if self._is_number(token):
                stack.push(float(token))
            elif token in ('+', '-', '*', '/'):
                if stack.size() < 2:
                    print("[DAX] Error: not enough operands.")
                    return None
                b = stack.pop()
                a = stack.pop()
                result = self._apply(a, b, token)
                stack.push(result)
            else:
                print(f"[DAX] Error: unknown token '{token}'")
                return None

        if stack.size() != 1:
            print("[DAX] Error: malformed expression.")
            return None

        return stack.pop()

    def validate_parentheses(self, expression):
        """
        Checks that every opening bracket has a matching closing bracket.
        Supports (), [], {}
        Analysts often write nested DAX like: CALCULATE(SUM([Revenue]), FILTER(...))
        """
        stack = LinkedStack()
        pairs = {')': '(', ']': '[', '}': '{'}

        for char in expression:
            if char in ('(', '[', '{'):
                stack.push(char)
            elif char in (')', ']', '}'):
                if stack.is_empty() or stack.pop() != pairs[char]:
                    return False

        return stack.is_empty()

    def infix_to_postfix(self, expression):
        """
        Converts a standard infix expression to postfix using the
        Shunting-Yard algorithm. Supports +, -, *, / and parentheses.
        Example: '( 15000 + 5000 ) * 2'  →  '15000 5000 + 2 *'
        Tokens must be space-separated.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        stack  = ArrayStack()
        output = []
        tokens = expression.strip().split()

        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in precedence:
                while (not stack.is_empty()
                       and stack.peek() in precedence
                       and precedence[stack.peek()] >= precedence[token]):
                    output.append(stack.pop())
                stack.push(token)
            elif token == '(':
                stack.push(token)
            elif token == ')':
                while not stack.is_empty() and stack.peek() != '(':
                    output.append(stack.pop())
                if stack.is_empty():
                    print("[DAX] Error: mismatched parentheses.")
                    return None
                stack.pop()
            else:
                print(f"[DAX] Error: unknown token '{token}'")
                return None

        while not stack.is_empty():
            top = stack.pop()
            if top in ('(', ')'):
                print("[DAX] Error: mismatched parentheses.")
                return None
            output.append(top)

        return ' '.join(output)

    def _is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _apply(self, a, b, operator):
        if operator == '+': return a + b
        if operator == '-': return a - b
        if operator == '*': return a * b
        if operator == '/':
            if b == 0:
                print("[DAX] Error: division by zero.")
                return 0
            return a / b


#  Phase 3 Runner 

def run_phase3():
    print("\n" + "=" * 50)
    print("  PHASE 3: THE DAX FORMULA PARSER")
    print("=" * 50)

    engine = DAXEvaluator()

    # --- Postfix Evaluation ---
    print("\n--- Postfix Expression Evaluator ---")
    expressions = [
        ("15000 5000 + 2 *",       "(15000 + 5000) * 2"),
        ("850000 340000 - 0.15 *", "(Revenue - Cost) * Tax 15%"),
        ("9 3 / 4 2 - *",          "(9 / 3) * (4 - 2)"),
    ]
    for postfix, description in expressions:
        result = engine.evaluate_postfix(postfix)
        print(f"  Postfix : {postfix}")
        print(f"  Meaning : {description}")
        print(f"  Result  : {result:,.2f}\n")

    # --- Parentheses Validator ---
    print("--- Parentheses Validator ---")
    formulas = [
        "CALCULATE(SUM([Revenue]), FILTER([Region], [Region] = \"Africa\"))",
        "IF(([Revenue] - [Cost]) > 0, \"Profit\", \"Loss\")",
        "SUMX(Sales, [Units Sold] * [Unit Price]",
        "DIVIDE([Revenue], [Cost])) * 100",
    ]
    for formula in formulas:
        valid = engine.validate_parentheses(formula)
        status = "✓ Valid" if valid else "✗ Invalid"
        print(f"  {status} → {formula}")

    #  Infix to Postfix Conversion 
    print("\n--- Infix to Postfix Converter (Shunting-Yard) ---")
    infix_expressions = [
        "( 15000 + 5000 ) * 2",
        "850000 - 340000 * 0.15",
        "( 9 / 3 ) * ( 4 - 2 )",
    ]
    for infix in infix_expressions:
        postfix = engine.infix_to_postfix(infix)
        result  = engine.evaluate_postfix(postfix)
        print(f"  Infix   : {infix}")
        print(f"  Postfix : {postfix}")
        print(f"  Result  : {result:,.2f}\n")


if __name__ == '__main__':
    run_phase3()