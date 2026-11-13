
import ast
import operator
from pathlib import Path

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


# -------------------------------
# TOOL 1: WEB SEARCH
# -------------------------------

search_engine = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """Search the internet for information about a given topic."""
    try:
        return search_engine.run(query)
    except Exception as e:
        return f"Web search error: {e}"


# -------------------------------
# TOOL 2: CALCULATOR
# -------------------------------

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions such as 25 * 4 or (100 + 50) / 3."""

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = calculate(node.left)
            right = calculate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large.")

            result = operations[type(node.op)](left, right)

            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
            return operations[type(node.op)](calculate(node.operand))

        raise ValueError("Unsupported mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = calculate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"


# -------------------------------
# TOOL 3: LOCAL FILE READER
# -------------------------------

@tool
def file_reader(file_path: str) -> str:
    """Read the contents of a local text, Markdown, CSV, or JSON file."""

    try:
        path = Path(file_path)

        if not path.is_file():
            return "Error: File not found."

        if path.suffix.lower() not in [".txt", ".md", ".csv", ".json"]:
            return "Error: Only TXT, MD, CSV, and JSON files are supported."

        if path.stat().st_size > 100_000:
            return "Error: File is too large. Maximum size is 100 KB."

        return path.read_text(encoding="utf-8")

    except Exception as e:
        return f"File reading error: {e}"


# -------------------------------
# ALL THREE AGENT TOOLS
# -------------------------------

tools = [web_search, calculator, file_reader]

print("AI Agent tools loaded successfully!")
