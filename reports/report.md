# 📄 Code Review Report


## sample_code\bad_code.py
- **High** | Logic Risk | Line: 5
  - Issue: Possible division by zero.
  - Fix: Add a guard condition before division, e.g. `if len(nums) == 0: return 0`.
- **High** | Type Risk | Line: None
  - Issue: Possible string and integer concatenation.
  - Fix: Use f-strings: `print(f'Average is {avg}')`
- **Medium** | Best Practice | Line: None
  - Issue: Missing `if __name__ == '__main__'` guard.
  - Fix: Wrap executable code inside `if __name__ == '__main__':`.
- **Medium** | Resource Management | Line: None
  - Issue: File opened without using `with` statement.
  - Fix: Use `with open(path, 'r') as f:` so the file is closed automatically.
- **Low** | Portability Issue | Line: None
  - Issue: Hardcoded file path detected. Consider using os.path.
  - Fix: Use `os.path.join()` instead of hardcoded paths.
