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

    return phone.isdigit() and len(phone) == 10 and phone[0] in {"6", "7", "8", "9"}


# ----------------------------------------
# NAME VALIDATION (simple but effective)
# ----------------------------------------
def is_valid_name(text: str) -> bool:
    name = text.strip()

    # Reject very short/long names
    if len(name) < 2 or len(name) > 60:
        return False
    if any(char.isdigit() for char in name):
        return False

    # Disallow obvious non-name patterns
    if "@" in name:
        return False
    if not re.fullmatch(r"[A-Za-z][A-Za-z .'\-]*", name):
        return False

    words = [w for w in re.split(r"\s+", name) if w]
    if len(words) == 0 or len(words) > 3:
        return False

    disallowed_tokens = {
        "price", "pricing", "cost", "demo", "trial", "contact", "call", "email",
        "consult", "consultation", "services", "partnership", "help", "thanks",
        "thank", "interested", "information", "details", "support"
    }
    lowered_words = {w.lower().strip(".") for w in words}
    if lowered_words & disallowed_tokens:
        return False

    return True


def normalize_indian_phone(text: str) -> str:
    """
    Normalize common India number inputs to a 10-digit local format.
    Raises ValueError if the number is invalid.
    """
    phone = text.strip().replace(" ", "").replace("-", "")

    if phone.startswith("+91"):
        phone = phone[3:]
    elif phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]
    elif phone.startswith("0") and len(phone) == 11:
        phone = phone[1:]

    if not (phone.isdigit() and len(phone) == 10 and phone[0] in {"6", "7", "8", "9"}):
        raise ValueError("Invalid Indian phone number")

    return phone
