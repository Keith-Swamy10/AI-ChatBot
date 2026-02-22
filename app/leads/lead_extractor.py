from datetime import datetime
from typing import Optional, Dict
import pymysql

from app.utils.validators import is_valid_email, is_valid_indian_phone, is_valid_name, normalize_indian_phone

from app.leads.lead_state_service import (
    get_or_create_lead_state,
    update_lead_state,
    refresh_intent_summary_from_conversation
)

from app.core.config import get_settings
from app.integrations.google_sheets import append_lead_to_sheet

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
# RETRIEVE COMPLETE LEAD
# ----------------------------------------
def get_lead_by_session_id(session_id: str) -> Optional[Dict]:
    """
    Fetch complete lead data from database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT session_id, name, email, phone, intent_summary, created_at
        FROM leads
        WHERE session_id = %s
        """,
        (session_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "session_id": row[0],
        "name": row[1],
        "email": row[2],
        "phone": row[3],
        "intent_summary": row[4],
        "created_at": row[5]
    }

# ----------------------------------------
# SAVE / UPDATE LEAD FIELD
# ----------------------------------------
def upsert_lead_field(session_id: str, field: str, value: str):
    allowed_fields = {"name", "email", "phone", "intent_summary"}
    if field not in allowed_fields:
        raise ValueError(f"Invalid lead field: {field}")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM leads WHERE session_id = %s",
        (session_id,)
    )
    row = cursor.fetchone()

    if row:
        cursor.execute(
            f"UPDATE leads SET {field} = %s WHERE session_id = %s",
            (value, session_id)
        )
    else:
        cursor.execute(
            f"""
            INSERT INTO leads (session_id, {field}, created_at)
            VALUES (%s, %s, %s)
            """,
            (session_id, value, datetime.utcnow())
        )

    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------------------
# PROCESS USER INPUT
# ----------------------------------------
def process_lead_input(session_id: str, user_message: str) -> Dict:
    """
    Fast-forward aware lead processor.
    """

    state = get_or_create_lead_state(session_id)
    text = user_message.strip()
    is_casual = is_casual_message(text)

    extracted = extract_contact_fields(text)

    # -----------------------------------------
    # Opportunistic storage (fast-forward)
    # -----------------------------------------
    if extracted["email"]:
        upsert_lead_field(session_id, "email", extracted["email"])

    if extracted["phone"]:
        upsert_lead_field(session_id, "phone", extracted["phone"])

    # Note: Don't store name here - it's handled in the state-based flow below

    # -----------------------------------------
    # STATE-BASED FLOW
    # -----------------------------------------

    # ASK NAME
    if state == "ASKED_NAME":
        if is_casual:
            return {
                "handled": False,
                "message": None,
                "lead_completed": False
            }

        if extracted["name"]:
            # User provided name
            upsert_lead_field(session_id, "name", extracted["name"])

            # Check what else we already have in DB (not just this message)
            lead_data = get_lead_by_session_id(session_id) or {}
            has_email = bool(lead_data.get("email"))
            has_phone = bool(lead_data.get("phone"))

            if has_email and has_phone:
                update_lead_state(session_id, "COMPLETED")
                refresh_intent_summary_from_conversation(session_id)
                lead_data = get_lead_by_session_id(session_id)
                if lead_data:
                    try:
                        append_lead_to_sheet(lead_data)
                    except Exception as e:
                        print(f"Error appending lead to Google Sheets: {e}")
                return {
                    "handled": True,
                    "message": "Thank you! Our team will reach out to you shortly!",
                    "lead_completed": True
                }
            elif has_email:
                update_lead_state(session_id, "ASKED_PHONE")
                return {
                    "handled": True,
                    "message": "Great! May I also have your phone number?",
                    "lead_completed": False
                }
            else:
                update_lead_state(session_id, "ASKED_EMAIL")
                return {
                    "handled": True,
                    "message": "Thanks! Could you please share your email address?",
                    "lead_completed": False
                }

        # User didn't provide a name, but might have provided email or phone
        elif extracted["email"] and extracted["phone"]:
            # They provided email+phone but not name, ask for name again
            return {
                "handled": True,
                "message": "I got your email and phone! Now, could you please tell me your name?",
                "lead_completed": False
            }
        elif extracted["email"]:
            # They provided email instead of name
            upsert_lead_field(session_id, "email", extracted["email"])
            return {
                "handled": True,
                "message": "Got your email! Still need your name though. What's your name?",
                "lead_completed": False
            }
        elif extracted["phone"]:
            # They provided phone instead of name
            upsert_lead_field(session_id, "phone", extracted["phone"])
            return {
                "handled": True,
                "message": "Got your phone! But I still need your name. What's your name?",
                "lead_completed": False
            }
        else:
            # No valid input
            return {
                "handled": True,
                "message": "Could you please tell me your name?",
                "lead_completed": False
            }

    # ASK EMAIL
    if state == "ASKED_EMAIL":
        if extracted["email"]:
            upsert_lead_field(session_id, "email", extracted["email"])

            lead_data = get_lead_by_session_id(session_id) or {}
            if lead_data.get("phone"):
                update_lead_state(session_id, "COMPLETED")
                refresh_intent_summary_from_conversation(session_id)
                
                # Get full lead data and push to Google Sheets
                lead_data = get_lead_by_session_id(session_id)
                if lead_data:
                    try:
                        append_lead_to_sheet(lead_data)
                    except Exception as e:
                        print(f"Error appending lead to Google Sheets: {e}")
                
                return {
                    "handled": True,
                    "message": "Thank you! Our team will reach out to you shortly!",
                    "lead_completed": True
                }

            update_lead_state(session_id, "ASKED_PHONE")
            return {
                "handled": True,
                "message": "Great. May I also have your phone number?",
                "lead_completed": False
            }
        
        elif extracted["phone"]:
            # They provided phone instead of email
            upsert_lead_field(session_id, "phone", extracted["phone"])
            return {
                "handled": True,
                "message": "Got your phone! I still need your email address. What's your email?",
                "lead_completed": False
            }

        elif is_casual:
            return {
                "handled": False,
                "message": None,
                "lead_completed": False
            }

        else:
            return {
                "handled": True,
                "message": "That doesn't seem like a valid email. Could you re-enter it?",
                "lead_completed": False
            }

    # ASK PHONE
    if state == "ASKED_PHONE":
        if extracted["phone"]:
            upsert_lead_field(session_id, "phone", extracted["phone"])
            update_lead_state(session_id, "COMPLETED")
            refresh_intent_summary_from_conversation(session_id)

            # Get full lead data and push to Google Sheets
            lead_data = get_lead_by_session_id(session_id)
            if lead_data:
                try:
                    append_lead_to_sheet(lead_data)
                except Exception as e:
                    print(f"Error appending lead to Google Sheets: {e}")

            return {
                "handled": True,
                "message": "Thank you! Our team will reach out to you shortly!",
                "lead_completed": True
            }

        if is_casual:
            return {
                "handled": False,
                "message": None,
                "lead_completed": False
            }

        return {
            "handled": True,
            "message": "Please enter a valid 10-digit Indian phone number.",
            "lead_completed": False
        }

    return {
        "handled": False,
        "message": None,
        "lead_completed": False
    }

def extract_contact_fields(text: str):
    name_candidate = extract_name_candidate(text)
    normalized_phone = None

    if is_valid_indian_phone(text):
        try:
            normalized_phone = normalize_indian_phone(text)
        except ValueError:
            normalized_phone = None

    return {
        "email": text if is_valid_email(text) else None,
        "phone": normalized_phone,
        "name": name_candidate
    }


def extract_name_candidate(text: str) -> Optional[str]:
    cleaned = text.strip()
    lowered = cleaned.lower()

    prefixes = ["my name is ", "i am ", "i'm ", "this is "]
    for prefix in prefixes:
        if lowered.startswith(prefix):
            candidate = cleaned[len(prefix):].strip(" .,!?:;")
            return candidate if is_valid_name(candidate) else None

    return cleaned if is_valid_name(cleaned) else None


def is_casual_message(text: str) -> bool:
    lowered = text.lower().strip()
    casual = {
        "hi", "hello", "hey", "yo", "hii",
        "ok", "okay", "sure", "hmm", "hmmm",
        "thanks", "thank you", "cool", "fine"
    }
    return lowered in casual
