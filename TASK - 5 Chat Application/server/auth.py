# server/auth.py

from database import add_user, verify_user

def handle_register(username, password):
    try:
        success = add_user(username, password)
        return "REGISTERED" if success else "USERNAME_TAKEN"
    except Exception as e:
        print(f"[AUTH ERROR - REGISTER] {e}")
        return "ERROR"

def handle_login(username, password):
    try:
        valid = verify_user(username, password)
        return "LOGIN_SUCCESS" if valid else "LOGIN_FAILED"
    except Exception as e:
        print(f"[AUTH ERROR - LOGIN] {e}")
        return "ERROR"
