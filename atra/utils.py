import datetime

# Simple timestamped logger
def log(message: str):
    """Prints a message with a UTC timestamp."""
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp} UTC] {message}")

# Example helper for formatting
def divider(label: str = ""):
    line = "=" * 40
    print(f"\n{line}\n{label}\n{line}\n")

if __name__ == "__main__":
    divider("Testing utils.py")
    log("Logger initialized successfully.")
