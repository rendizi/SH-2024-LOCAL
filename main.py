import subprocess
import requests
import sys

def get_serviceId_from_args():
    for arg in sys.argv:
        if arg.startswith("serviceId="):
            return arg.split("=")[1]
    return None


def get_running_services():
    try:
        # Execute the systemctl command
        result = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--state=running"],
            stdout=subprocess.PIPE, text=True, check=True
        )
        # Extract service names
        services = []
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) > 0 and parts[0].endswith(".service"):
                services.append(parts[0])  # Append only the service name
        cleaned_services = [service.replace('.service', '') for service in services]
        return cleaned_services
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        return []

def scan_ports():
    try:
        result = subprocess.run(
            ["nmap", "-sV", "localhost"],
            stdout=subprocess.PIPE, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении nmap: {e}")
        return ""

def send_to_backend(data, id,url):
    try:
        response = requests.post(url, json={"technologies": data, "serviceId": int(id)})
        response.raise_for_status()
        print("Данные успешно отправлены на бэкенд.")
    except requests.RequestException as e:
        print(f"Ошибка при отправке данных: {e}")
if __name__ == "__main__":
    serviceId = get_serviceId_from_args()
    if serviceId:
        ports = scan_ports()
        
        services = get_running_services()
        print("Running Services:")
        print(services)

        send_to_backend(services,serviceId, url="http://20.64.237.199:4000/user/service/technologies")
    else:
        print("No serviceId provided.")
