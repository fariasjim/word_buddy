import subprocess
import sys
import requests


def generate_stable_machine_uid():
    # Automatically captures the hardware fingerprint. Rather than only using mac uid. it gets the actual CPU id.
    try:
        if sys.platform == "win32":
            cmd = "wmic csproduct get uuid"
            output = subprocess.check_output(cmd, shell=True).decode().split()
            return output[1] if len(output) > 1 else "WIN_HWID_FALLBACK"
        else:
            # Linux fallback (e.g., Arch Linux)
            for path in ["/var/lib/dbus/machine-id", "/etc/machine-id"]:
                try:
                    with open(path, "r") as f:
                        return f.read().strip()
                except FileNotFoundError:
                    continue
            return "LINUX_HWID_FALLBACK"
    except Exception:
        import uuid

        return str(uuid.getnode())


def login_user(username, password, demo_days=7):
    """
    Pure Login Handler.
    Only requires username and password from the user UI.
    """
    # Automatically grab the local device ID
    uid = generate_stable_machine_uid()

    # Replace with your actual Google Apps Script Web App URL
    url = "https://script.google.com/macros/s/AKfycbz9GNuhpwEFTG_jxvKjxL27p0MQMrLNFi244oSxW1wwXPlVsvI_BHemulyE6jqOe545/exec"

    # Construct payload for matching on the server
    payload = {
        "username": username,
        "password": password,
        "uid": uid,
        "demo_days": demo_days,  # Fallback threshold managed by your app
    }

    try:
        response = requests.post(url, data=payload, allow_redirects=True, timeout=8)

        if response.status_code == 200:
            res_data = response.json()
            status = res_data.get("status")
            message = res_data.get("message")
            days_left = res_data.get("days_left")

            # --- Evaluate Server Status Responses ---
            if status == "SUCCESS":
                print("🔓 Login Successful! Premium License verified.")
                return True, "PREMIUM"

            elif status == "DEMO_ACTIVE":
                print(f"⏳ Login Successful! Trial Mode: {days_left} days remaining.")
                return True, "DEMO"

            elif status == "USER_NOT_FOUND":
                print(
                    "❌ Account does not exist. Please register via the registration form first."
                )
                return False, status

            elif status == "AUTH_FAILED":
                print("❌ Incorrect password.")
                return False, status

            elif status == "HARDWARE_MISMATCH":
                print(
                    "⚠️ Security Block: This account is registered to a different device footprint."
                )
                return False, status

            elif status == "PAUSED" or status == "DEMO_EXPIRED":
                print(f"🚫 Access Denied: {message}")
                return False, status

            else:
                print(f"Unexpected response state: {status}")
                return False, "UNKNOWN_ERROR"
        else:
            print("Server returned an invalid status routing code.")
            return False, "SERVER_ERROR"

    except requests.RequestException as e:
        print(f"Connection failed: {e}")
        return False, "OFFLINE"


# --- UI Action Trigger Examples ---
# user_login = login_user("fariasjim", "fariasjim")
