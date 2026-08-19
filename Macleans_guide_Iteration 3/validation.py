#validation.py

def is_non_empty(text: str) -> bool: 
    # Checks if input string is not empty or just whitespace.
    return bool(text and text.strip())

def validate_login_input(username: str, password: str) -> tuple[bool, str]:
    # Validates username and password inputs.
    if not is_non_empty(username):
        return False, "Username cannot be empty."
    if not is_non_empty(password):
        return False, "Password cannot be empty."
    return True, ""