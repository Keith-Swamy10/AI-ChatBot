from datetime import datetime
from typing import Optional
import pymysql

from app.utils.validators import is_valid_email, is_valid_indian_phone
from app.core.config import get_settings

INTENT_SUMMARY_MAX_LEN = 500


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

def get_conversation_summary(session_id: str) -> str:
    """
    Build a concise intent summary from user conversation.
    """
    messages = get_conversation_messages(session_id)
    if not messages:
        return ""

    user_msgs = [
        msg.strip()
        for sender, msg in messages
        if str(sender).lower() == "user" and msg and msg.strip()
    ]
    if not user_msgs:
        return ""

    parts = []
    detected_topics = extract_lead_topics(" ".join(user_msgs))
    if detected_topics:
        parts.append(f"User intent: interested in {', '.join(detected_topics)}")
    else:
        parts.append("User intent: seeking information and support")

    parts.append(f"Engagement: {len(user_msgs)} user message(s)")

    question_count = sum(1 for msg in user_msgs if "?" in msg)
    if question_count:
        parts.append(f"Questioning behavior: asked {question_count} question(s)")

    if any(detect_opportunistic_contact(msg) for msg in user_msgs):
        parts.append("Contact signal: user shared direct contact details")

    latest_need = shorten_text(user_msgs[-1], 120)
    parts.append(f"Latest user need: {latest_need}")

    return shorten_text(" | ".join(parts), INTENT_SUMMARY_MAX_LEN)


def get_conversation_messages(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sender, message FROM chats
        WHERE session_id = %s
        ORDER BY id ASC
        """,
        (session_id,)
    )
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages


def shorten_text(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text

    marker = " ..."
    if max_len <= len(marker) + 1:
        return text[:max_len]

    return text[: max_len - len(marker)].rstrip() + marker


def extract_lead_topics(text: str):
    text_lower = text.lower()
    topics = []

    for topic in LEAD_SIGNALS:
        if topic in text_lower and topic not in topics:
            topics.append(topic)

    # Keep summary compact and stable.
    return topics[:5]

# ----------------------------------------
# STORE INTENT SUMMARY
# ----------------------------------------
def store_intent_summary(session_id: str, intent_message: str):
    """
    Store the user's initial intent when lead flow starts.
    Includes the trigger message + conversation context.
    Updates existing summary so context is not stale.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check existing lead row
    cursor.execute(
        "SELECT intent_summary FROM leads WHERE session_id = %s",
        (session_id,)
    )
    row = cursor.fetchone()
    
    # Build intent summary with conversation context
    conversation = get_conversation_summary(session_id)
    if conversation:
        full_intent = f"Trigger: {intent_message} | {conversation}"
    else:
        full_intent = f"Trigger: {intent_message}"
    
    # Insert or update so summary keeps improving over the session.
    if row:
        cursor.execute(
            """
            UPDATE leads
            SET intent_summary = %s
            WHERE session_id = %s
            """,
            (full_intent[:INTENT_SUMMARY_MAX_LEN], session_id)
        )
    else:
        # Insert new record with intent
        cursor.execute(
            """
            INSERT INTO leads (session_id, intent_summary, created_at)
            VALUES (%s, %s, %s)
            """,
            (session_id, full_intent[:INTENT_SUMMARY_MAX_LEN], datetime.utcnow())
        )

    conn.commit()
    cursor.close()
    conn.close()


def refresh_intent_summary_from_conversation(session_id: str):
    """
    Recompute intent summary from the full conversation and upsert it.
    Use this before final lead export to capture the whole chat.
    """
    conversation = get_conversation_summary(session_id)
    if not conversation:
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id FROM leads WHERE session_id = %s",
            (session_id,)
        )
        row = cursor.fetchone()

        if row:
            cursor.execute(
                """
                UPDATE leads
                SET intent_summary = %s
                WHERE session_id = %s
                """,
                (conversation[:INTENT_SUMMARY_MAX_LEN], session_id)
            )
        else:
            cursor.execute(
                """
                INSERT INTO leads (session_id, intent_summary, created_at)
                VALUES (%s, %s, %s)
                """,
                (session_id, conversation[:INTENT_SUMMARY_MAX_LEN], datetime.utcnow())
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

