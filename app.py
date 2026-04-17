import os
import re
import smtplib
from email.message import EmailMessage

import streamlit as st
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError

KYC_URL = "https://customerverification-gbbd2od7cryndnqqhbvn7i.streamlit.app/"
load_dotenv()


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def is_valid_phone(phone: str) -> bool:
    cleaned = re.sub(r"\D", "", phone)
    return 10 <= len(cleaned) <= 15


def get_mail_config() -> dict:
    def get_secret_value(key: str, default: str = "") -> str:
        try:
            return str(st.secrets[key])
        except (StreamlitSecretNotFoundError, KeyError):
            return default

    smtp_host = get_secret_value("SMTP_HOST", os.getenv("SMTP_HOST", "smtp.gmail.com"))
    smtp_port = int(get_secret_value("SMTP_PORT", os.getenv("SMTP_PORT", "587")))
    smtp_user = get_secret_value("SMTP_USER", os.getenv("SMTP_USER", ""))
    smtp_password = get_secret_value("SMTP_PASSWORD", os.getenv("SMTP_PASSWORD", ""))
    sender_email = get_secret_value("SENDER_EMAIL", os.getenv("SENDER_EMAIL", smtp_user))

    return {
        "smtp_host": smtp_host,
        "smtp_port": smtp_port,
        "smtp_user": smtp_user,
        "smtp_password": smtp_password,
        "sender_email": sender_email,
    }


def send_kyc_email(
    to_email: str,
    first_name: str,
    last_name: str,
    config: dict,
) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Complete your KYC verification"
    msg["From"] = config["sender_email"]
    msg["To"] = to_email

    msg.set_content(
        f"""Hi {first_name} {last_name},

Thank you for submitting your basic details.
Please complete the remaining verification details here:
{KYC_URL}

Regards,
KYC Team
"""
    )

    with smtplib.SMTP(config["smtp_host"], config["smtp_port"]) as server:
        server.starttls()
        server.login(config["smtp_user"], config["smtp_password"])
        refused_recipients = server.send_message(msg)
        if refused_recipients:
            raise smtplib.SMTPRecipientsRefused(refused_recipients)


st.set_page_config(page_title="KYC Entry Form", page_icon="📝")
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #f5f7fb 0%, #eef2ff 100%);
        }
        .enquiry-card {
            max-width: 760px;
            margin: 24px auto 0 auto;
            padding: 28px 28px 18px 28px;
            border-radius: 16px;
            background: #ffffff;
            border: 1px solid #e6e8ef;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        }
        .enquiry-title {
            font-size: 30px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 6px;
        }
        .enquiry-subtitle {
            color: #475569;
            font-size: 15px;
            margin-bottom: 18px;
        }
        .enquiry-footer {
            color: #64748b;
            font-size: 12px;
            margin-top: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="enquiry-card">
        <div class="enquiry-title">Customer Enquiry Form</div>
        <div class="enquiry-subtitle">
            Share your basic details and we will email your secure KYC link.
        </div>
    """,
    unsafe_allow_html=True,
)

with st.form("kyc_form"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input(
            "First Name",
            placeholder="Enter first name",
            help="As per your official records",
        ).strip()
    with col2:
        last_name = st.text_input(
            "Last Name",
            placeholder="Enter last name",
            help="As per your official records",
        ).strip()

    email = st.text_input(
        "Email ID",
        placeholder="name@example.com",
        help="The KYC link will be sent to this email",
    ).strip()
    contact_number = st.text_input(
        "Contact Number",
        placeholder="+91 9876543210",
        help="Include country code if applicable",
    ).strip()
    submitted = st.form_submit_button("Submit Enquiry", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    errors = []

    if not first_name:
        errors.append("First Name is required.")
    if not last_name:
        errors.append("Last Name is required.")
    if not is_valid_email(email):
        errors.append("Please enter a valid Email ID.")
    if not is_valid_phone(contact_number):
        errors.append("Please enter a valid Contact Number (10 to 15 digits).")

    config = get_mail_config()
    if not config["smtp_user"] or not config["smtp_password"] or not config["sender_email"]:
        errors.append(
            "Email service is not configured. Add SMTP_USER, SMTP_PASSWORD, and SENDER_EMAIL in Streamlit secrets or environment variables."
        )

    if errors:
        for error in errors:
            st.error(error)
    else:
        try:
            send_kyc_email(email, first_name, last_name, config)
            st.success("Submitted successfully. A KYC link has been sent to your email.")
            st.info("If you do not see the email, please check Spam/Junk folder.")
        except Exception as exc:
            st.error(f"Submission succeeded but email could not be sent: {exc}")

st.markdown(
    '<p class="enquiry-footer" style="text-align:center;">'
    "We only use this information to send your KYC continuation link."
    "</p>",
    unsafe_allow_html=True,
)
