# Lab 5: Static Code Analysis
## Issue Identification and Resolution

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak MD5 hashing algorithm | Security | 25 | The `ticket_code()` function used MD5 to generate ticket codes. MD5 is considered weak for security-sensitive hashing. | Replaced MD5 with SHA-256 to use a stronger hashing algorithm. The generated code remains predictable because it is derived from the show ID and seat number. |
| Insecure file permissions | Security | 55 | The program used `os.chmod("seats.json", 0o777)`, granting overly permissive access on Unix-like systems. | Removed the permission change so the program does not explicitly grant everyone read, write, and execute permissions. |
| Mutable default argument | Bug / Code Quality | 9 | The `reserve_seat()` function used `system_logs=[]`. Mutable default objects can be shared across function calls. | Changed the default to `None` and initialized a new list inside the function. |
| Broad exception handling | Bug / Code Quality | 19–22 | The `release_seat()` function used a bare `except`, potentially hiding unrelated errors. | Replaced the bare exception handler with specific exception handling. |
| File handling without context managers | Code Quality | 27–35 | Files were opened without context managers, making resource cleanup less reliable. | Used `with open(...)` and explicitly specified UTF-8 encoding. |
| Missing module and function docstrings | Code Quality | 1, 9, 18, 24, 27, 31, 37, 42 | The module and several functions lacked docstrings. | Added descriptive docstrings to explain the purpose of the module and functions. |
| Non-standard function naming | Style | 37 | `printSeatingSummary()` did not follow the standard snake_case naming convention. | Renamed the function to `print_seating_summary()` and updated its call. |
| String formatting | Style | 12, 15 | The original code used `%` formatting where f-strings were more appropriate. | Replaced the formatting expressions with f-strings. |
| Excessive line length | Style | 40 | A line exceeded the configured Pylint line-length limit. | Split the expression across multiple lines. |
| Missing file encoding | Code Quality | 28, 33 | File operations did not explicitly specify an encoding. | Added `encoding="utf-8"` to file operations. |
| Invalid seat reservations | Functional Bug | 9–15 | The program did not adequately validate seat numbers, allowing invalid values to be attempted. | Added checks for valid shows, integer seat numbers, and seat ranges. |
| Missing file-error handling | Reliability | 31–35 | Loading reservations could fail if the file was missing or contained invalid JSON. | Added handling for file-access errors and malformed JSON. |

## Summary

Pylint was used to identify code-quality problems, Bandit was used to identify security concerns, and Flake8 was used to identify style violations. The identified issues were reviewed and addressed to improve code quality, security, readability, and reliability while preserving the seat reservation functionality.

The final versions of the three tools' reports should be used to verify which findings were resolved.
