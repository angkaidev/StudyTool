def prompt(message: str) -> str:
    return input(f"\u001b[38;5;$11m{message}\u001b[0m")

def correct(message: str) -> str:
    return f"\u001b[38;5;$2m{message}\u001b[0m"

def incorrect(message: str) -> str:
    return f"\u001b[38;5;$1m{message}\u001b[0m"