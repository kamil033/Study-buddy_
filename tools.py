"""
tools.py — Tool functions for the AWS Cloud Assistant
Tools must NEVER raise exceptions — always return strings.
"""
from datetime import datetime


def get_current_datetime() -> str:
    """Returns the current date and time as a formatted string."""
    try:
        now = datetime.now()
        return f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"
    except Exception as e:
        return f"Error retrieving date/time: {str(e)}"


def calculator(expression: str) -> str:
    """
    Evaluates a safe arithmetic expression.
    Returns result as string or an error message.
    """
    try:
        # Allow only safe characters for arithmetic
        allowed = set("0123456789+-*/().^ %")
        cleaned = expression.replace("**", "^")
        if not all(c in allowed or c.isspace() for c in expression):
            return "Error: Only arithmetic expressions are supported."
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {expression} = {result}"
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error in calculation: {str(e)}"
