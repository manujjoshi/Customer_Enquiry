# KYC Entry Form (Streamlit)

This app collects:
- First Name
- Last Name
- Email ID
- Contact Number

After submission, it sends an automated email to the user with this KYC URL:
`https://customerverification-gbbd2od7cryndnqqhbvn7i.streamlit.app/`

## 1) Run Locally

### Prerequisites
- Python 3.9+
- pip

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure email credentials
You can configure with either `.streamlit/secrets.toml` or `.env`.

#### Option A: `.streamlit/secrets.toml`
Create `.streamlit/secrets.toml`:

```toml
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
SENDER_EMAIL = "your-email@gmail.com"
```

Notes:
- For Gmail, use an **App Password** (not your normal account password).
- Keep secrets private. Do not commit them.

#### Option B: `.env` (easy local setup)
Create a `.env` file in project root:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=your-email@gmail.com
```

You can copy from `.env.example` and then replace values.

### Start app
```bash
streamlit run app.py
```

## 2) Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select your repository.
4. Set main file path as `app.py`.
5. Add the same SMTP values in app **Secrets**:
   - `SMTP_HOST`
   - `SMTP_PORT`
   - `SMTP_USER`
   - `SMTP_PASSWORD`
   - `SENDER_EMAIL`
6. Deploy.

## 3) Environment Variables

You can set these directly in your shell/OS:
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SENDER_EMAIL`

The app reads Streamlit secrets first, then environment variables.
