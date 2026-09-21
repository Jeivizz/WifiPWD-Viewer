import re
import subprocess


def get_wifi_passwords_windows():
    networks = []
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'],
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", output)

        for profile in profiles:
            profile_name = profile.strip("\r").strip()
            try:
                profile_info = subprocess.check_output(
                    ["netsh", "wlan", "show", "profile", profile_name, "key=clear"],
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )

                password_match = re.search(r"(?:Key Content|Conteúdo da Chave)\s*:\s*(.*)", profile_info)
                password = password_match.group(1).strip("\r").strip() if password_match else None
            except subprocess.CalledProcessError:
                password = None

            networks.append({"SSID": profile_name, "Password": password})
    except Exception as e:
        print(f"[Windows Error] {e}")
    return networks