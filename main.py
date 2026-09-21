import platform
from utils.linux import get_wifi_passwords_linux
from utils.windows import get_wifi_passwords_windows


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