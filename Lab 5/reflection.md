# Lab 5: Static Code Analysis
## Reflection

### 1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing the program. It helps identify potential bugs, security vulnerabilities, coding-standard violations, and maintainability problems. It is important because developers can detect and fix many issues early, before they cause problems during execution or deployment.

### 2. What are the differences between Pylint, Bandit, and Flake8?

Pylint focuses on overall Python code quality, including naming conventions, documentation, potential programming errors, and code structure. Bandit focuses on identifying common security vulnerabilities and unsafe coding practices. Flake8 checks Python code for style violations, whitespace issues, and other formatting problems.

Using all three tools provides a broader review than using only one because they focus on different aspects of code quality.

### 3. What issues were identified and how were they fixed?

The analysis identified issues including a mutable default argument, broad exception handling, missing docstrings, non-standard function naming, unsafe file permissions, and the use of MD5 for ticket-code generation. File handling and seat validation also required improvement.

The fixes included using `None` for the mutable default argument, catching specific exceptions, adding docstrings, following snake_case naming conventions, replacing MD5 with SHA-256, removing the overly permissive file-permission change, using context managers, and validating seat numbers.

These changes improved the program's readability, reliability, and security. The final analysis reports were used to check whether the tool-detected issues had been resolved.

### 4. What are the limitations of static code analysis?

Static code analysis cannot detect every possible runtime error or guarantee that a program behaves correctly for every input. Some findings may require human judgment to determine whether they represent genuine problems. Static analysis also cannot fully replace functional testing.

For this reason, the program was also executed and tested with valid and invalid seat inputs. Combining static analysis with testing provides greater confidence in the correctness and maintainability of the code.
