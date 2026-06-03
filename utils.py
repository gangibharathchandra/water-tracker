import datetime

# Get current timestamp
def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Format issue types nicely
def format_issue(issue):
    mapping = {
        "Leakage": "💧 Leakage",
        "No Water": "🚱 No Water",
        "Dirty Water": "🟡 Dirty Water",
        "Low Pressure": "⚠️ Low Pressure"
    }
    return mapping.get(issue, issue)


# Validate phone number (basic)
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10