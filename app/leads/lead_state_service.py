from datetime import datetime
from typing import Optional
import pymysql

from app.utils.validators import is_valid_email, is_valid_indian_phone
from app.core.config import get_settings


# ----------------------------------------
# DB CONNECTION
# ----------------------------------------
def get_db_connection():
    settings = get_settings()
    return pymysql.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )

# ----------------------------------------
# LEAD STATES (ENUM-LIKE)
# ----------------------------------------
LEAD_STATES = {
    "NONE",
    "ASKED_NAME",
    "ASKED_EMAIL",
    "ASKED_PHONE",
    "COMPLETED"
}

# ----------------------------------------
# SIGNAL KEYWORDS
# ----------------------------------------
LEAD_SIGNALS = [
    "price", "pricing", "cost",
    "demo", "trial",
    "contact", "call", "email",
    "consult", "consultation",
    "services", "partnership"
]

# ----------------------------------------
# STATE FETCH / CREATE
# ----------------------------------------
def get_or_create_lead_state(session_id: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT current_step FROM lead_states WHERE session_id = %s",
        (session_id,)
    )
    row = cursor.fetchone()

    if row:
        cursor.close()
        conn.close()
        return row[0]

    cursor.execute(
        """
        INSERT INTO lead_states (session_id, current_step, updated_at)
        VALUES (%s, %s, %s)
        """,
        (session_id, "NONE", datetime.utcnow())
    )
    conn.commit()

    cursor.close()
    conn.close()
    return "NONE"

# ----------------------------------------
# UPDATE STATE
# ----------------------------------------
def update_lead_state(session_id: str, new_state: str):
    if new_state not in LEAD_STATES:
        raise ValueError(f"Invalid lead state: {new_state}")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE lead_states
        SET current_step = %s, updated_at = %s
        WHERE session_id = %s
        """,
        (new_state, datetime.utcnow(), session_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

# ----------------------------------------
# SIGNAL DETECTION
# ----------------------------------------
def detect_lead_signal(user_message: str) -> bool:
    msg = user_message.lower()
    return any(keyword in msg for keyword in LEAD_SIGNALS)

# ----------------------------------------
# SHOULD START LEAD COLLECTION?
# ----------------------------------------
def should_start_lead_flow(session_id: str, user_message: str) -> bool:
    """
    Decides whether to flip lead_state from NONE → ASK_NAME
    using 3 triggers:
    1. Opportunistic (email/phone dropped)
    2. Explicit intent
    3. Proactive engagement
    """

    current_state = get_or_create_lead_state(session_id)

    # Lead flow already active
    if current_state != "NONE":
        print(f"[DETECT] Lead flow already active: {current_state}")
        return True

    # --------------------------------
    # 1. Opportunistic trigger
    # --------------------------------
    if detect_opportunistic_contact(user_message):
        print(f"[DETECT] Opportunistic contact detected")
        update_lead_state(session_id, "ASKED_NAME")
        store_intent_summary(session_id, user_message)
        return True

    # --------------------------------
    # 2. Explicit intent trigger
    # --------------------------------
    if detect_lead_signal(user_message):
        print(f"[DETECT] Lead signal detected")
        update_lead_state(session_id, "ASKED_NAME")
        store_intent_summary(session_id, user_message)
        return True

    # --------------------------------
    # 3. Proactive engagement trigger
    # --------------------------------
    user_turns = count_user_messages(session_id)
    print(f"[DETECT] User turns: {user_turns}")

    if user_turns >= 4:  # safe default
        print(f"[DETECT] Threshold reached (4+ messages)")
        update_lead_state(session_id, "ASKED_NAME")
        store_intent_summary(session_id, "User showed sustained interest after multiple messages")
        return True

    print(f"[DETECT] No lead trigger")
    return False

# ----------------------------------------
# NEXT QUESTION TO ASK
# ----------------------------------------
def next_lead_question(session_id: str) -> Optional[str]:
    state = get_or_create_lead_state(session_id)

    if state == "ASKED_NAME":
        return "Before we proceed, may I know your name?"
    if state == "ASKED_EMAIL":
        return "Thanks! Could you please share your email address?"
    if state == "ASKED_PHONE":
        return "Got it. May I also have your phone number?"

    return None

def count_user_messages(session_id: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM chats
        WHERE session_id = %s AND sender = 'user'
        """,
        (session_id,)
    )

    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def detect_opportunistic_contact(user_message: str) -> bool:
    text = user_message.strip()
    return is_valid_email(text) or is_valid_indian_phone(text)

# ----------------------------------------
# STORE INTENT SUMMARY
# ----------------------------------------
def store_intent_summary(session_id: str, intent_message: str):
    """
    Store the user's initial intent when lead flow starts.
    Only stores if not already set (to avoid overwriting).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if intent_summary already exists
    cursor.execute(
        "SELECT intent_summary FROM leads WHERE session_id = %s",
        (session_id,)
    )
    row = cursor.fetchone()
    
    # Only update if intent_summary is NULL
    if row:
        if row[0] is None:
            cursor.execute(
                """
                UPDATE leads
                SET intent_summary = %s
                WHERE session_id = %s
                """,
                (intent_message[:200], session_id)
            )
    else:
        # Insert new record with intent
        cursor.execute(
            """
            INSERT INTO leads (session_id, intent_summary, created_at)
            VALUES (%s, %s, %s)
            """,
            (session_id, intent_message[:200], datetime.utcnow())
        )

    conn.commit()
    cursor.close()
    conn.close()

