import subprocess


def get_wifi_passwords_linux():
    networks = []
    try:
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