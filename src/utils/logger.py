import time


# Some lookup tables
status_color = {
    "PRINT": "\033[0m",
    "INFO": "\033[94m",
    "WARN": "\033[93m",
    "FAIL": "\033[91m"
}

text_format = {
    "NONE": "\033[0m",
    "BOLD": "\033[1m"
}


def log(text, status: str = "PRINT", custom_color: str = None, silent: bool = False) -> str:
    """Logs text to console with formatting and timestamp. Status can be 'print', 'info', 'warn', or 'fail'.
    Silent only returns a log string, it does not print it."""

    status_key = status.upper()
    if custom_color:
        color = custom_color
    elif status_key in status_color:
        color = status_color[status_key]
    else:
        color = text_format["NONE"]

    # Get time
    year, month, day, hour, minute, second = (str(i).zfill(2) for i in time.localtime()[:6])

    # Format strings
    date_string = f"[{year}/{month}/{day}, {hour}:{minute}:{second}]"
    status_string = f"{color}{text_format["BOLD"]}{status_key}:{text_format["NONE"]}"
    text_string = f"{color}{text}{text_format["NONE"]}"

    # Concatenate and print string
    print_string = f"{date_string} {status_string} {text_string}"
    if not silent:
        print(print_string)

    return print_string


def progress_bar():
    pass
