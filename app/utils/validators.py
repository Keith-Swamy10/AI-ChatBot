import re

# ----------------------------------------
# EMAIL VALIDATION
# ----------------------------------------
def is_valid_email(text: str) -> bool:
    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(email_regex, text.strip()) is not None


# ----------------------------------------
# INDIA-ONLY PHONE VALIDATION
# ----------------------------------------
def is_valid_indian_phone(text: str) -> bool:
    phone = text.strip().replace(" ", "").replace("-", "")

    # Allow formats:
    # 9876543210
    # +919876543210
    # 0919876543210
    if phone.startswith("+91"):
        phone = phone[3:]
    elif phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]
    elif phone.startswith("0") and len(phone) == 11:
        phone = phone[1:]

    return phone.isdigit() and len(phone) == 10


# ----------------------------------------
# NAME VALIDATION (simple but effective)
# ----------------------------------------
def is_valid_name(text: str) -> bool:
    name = text.strip()

    # Reject very short or numeric-only names
    if len(name) < 2:
        return False
    if any(char.isdigit() for char in name):
        return False

    return True
