# Release v1.0.6

## Improvements & Fixes

- Resolved all merge conflicts, especially for Python bytecode and database files.
- Cleaned up `.gitignore` to prevent tracking of `.pyc`, `__pycache__/`, and `.db` files.
- Merged and updated `requirements.txt` with the latest compatible package versions and added `twilio` for WhatsApp notifications.
- Fixed and refactored `test_user_features.py` to remove merge markers and ensure test logic is correct.
- General codebase cleanup and improved test reliability.

---

**Note:**
- Please ensure your Python environment matches the required versions in `requirements.txt`.
- If you encounter issues running tests, check your Python interpreter and virtual environment setup.
