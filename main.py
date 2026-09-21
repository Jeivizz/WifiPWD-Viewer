import platform
import subprocess
import re

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

def get_wifi_passwords_linux():
    networks = []
    try:
        # 1. Obtém apenas o nome (id) das conexões Wi-Fi
        output = subprocess.check_output(
            ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"],
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        wifi_names = []
        for line in output.strip().split("\n"):
            if not line:
                continue
            parts = line.split(":")
            if len(parts) >= 2 and "802-11-wireless" in parts[1]:
                wifi_names.append(parts[0])


        for name in wifi_names:
            try:
                password = subprocess.check_output(
                    ["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", name],
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                ).strip()

                if not password:
                    password = None
            except subprocess.CalledProcessError:
                password = None

            networks.append({"SSID": name, "Password": password})
    except Exception as e:
        print(f"[Linux Error] {e}")

    return networks

def get_wifi_passwords():
    system = platform.system()
    if system == "Windows":
        return get_wifi_passwords_windows()
    elif system == "Linux":
        return get_wifi_passwords_linux()
    else:
        raise NotImplementedError(f"Operating system {system} NOT supported")

if __name__ == "__main__":
    wifi_list = get_wifi_passwords()

    for wifi in wifi_list:
        ssid = wifi["SSID"]
        password = wifi["Password"] if wifi["Password"] else "<Not Found>"
        print("SSID..........", ssid)
        print("PASSWORD......", password)
        print("-" * 40)