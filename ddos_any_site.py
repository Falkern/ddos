import requests
import threading
import time
import logging
import random
import asyncio
import httpx
from queue import Queue
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global flag to stop all threads
stop_flag = False

def send_request(url, session, retries=3, backoff_factor=1):
    """Send a single HTTP GET request with retries, timeout, and exponential backoff."""
    global stop_flag
    for attempt in range(retries):
        if stop_flag:
            logging.info("Stopping request due to stop flag.")
            return
        try:
            response = session.get(url, timeout=5)
            logging.info(f"Response Code: {response.status_code} for URL: {url}")
            return
        except requests.exceptions.Timeout:
            logging.warning(f"Attempt {attempt + 1}: Timeout for URL: {url}")
        except requests.exceptions.ConnectionError:
            logging.warning(f"Attempt {attempt + 1}: Connection error for URL: {url}")
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1}: Request failed: {e}")
        
        time.sleep(backoff_factor * (2 ** attempt))
    logging.error(f"All retry attempts failed for URL: {url}")

def worker(url, queue, session, semaphore, min_delay, max_delay):
    """Thread worker function to process each request from the queue with rate limiting."""
    global stop_flag
    while not queue.empty() and not stop_flag:
        queue.get()
        with semaphore:
            send_request(url, session)
        queue.task_done()
        time.sleep(random.uniform(min_delay, max_delay))

def stop_listener():
    """Listen for the 'q' key to stop the script."""
    global stop_flag
    print("Press 'q' to stop the script.")
    while not stop_flag:
        if input().lower() == 'q':
            stop_flag = True
            logging.info("Stopping the script...")

def stress_test(url, num_requests, max_threads=5, min_delay=0.1, max_delay=0.3, use_async=False):
    """Function to manage the stress test using a thread pool or async if selected."""
    global stop_flag
    stop_flag = False  # Reset the stop flag

    # Start the listener thread
    listener_thread = threading.Thread(target=stop_listener, daemon=True)
    listener_thread.start()

    if use_async:
        logging.info("Starting asynchronous stress test...")
        asyncio.run(async_stress_test(url, num_requests, min_delay, max_delay))
    else:
        queue = Queue()
        for _ in range(num_requests):
            queue.put(None)

        session = requests.Session()
        semaphore = threading.Semaphore(max_threads)
        threads = []

        for _ in range(min(max_threads, num_requests)):
            thread = threading.Thread(target=worker, args=(url, queue, session, semaphore, min_delay, max_delay))
            thread.start()
            threads.append(thread)

        queue.join()
        for thread in threads:
            thread.join()

        logging.info("Stress test completed.")

async def async_request(url, client, retries=3, backoff_factor=1):
    """Send a single async GET request with retries and exponential backoff."""
    global stop_flag
    for attempt in range(retries):
        if stop_flag:
            logging.info("Stopping async request due to stop flag.")
            return
        try:
            response = await client.get(url, timeout=5)
            logging.info(f"Response Code: {response.status_code} for URL: {url}")
            return
        except httpx.TimeoutException:
            logging.warning(f"Attempt {attempt + 1}: Timeout for URL: {url}")
        except httpx.RequestError as e:
            logging.warning(f"Attempt {attempt + 1}: Request failed: {e}")
        
        await asyncio.sleep(backoff_factor * (2 ** attempt))
    logging.error(f"All retry attempts failed for URL: {url}")

async def async_stress_test(url, num_requests, min_delay, max_delay):
    """Asynchronous stress test using httpx and asyncio with rate limiting."""
    global stop_flag
    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(10)
        tasks = []

        async def sem_task():
            async with semaphore:
                if not stop_flag:
                    await async_request(url, client)
                    await asyncio.sleep(random.uniform(min_delay, max_delay))

        for _ in range(num_requests):
            tasks.append(sem_task())

        await asyncio.gather(*tasks)
    logging.info("Asynchronous stress test completed.")

def main():
    target_url = input("Enter the target URL: ").strip()
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    try:
        num_requests = int(input("Enter the number of requests (e.g., 100): "))
    except ValueError:
        logging.warning("Invalid input. Using default value of 100.")
        num_requests = 100

    try:
        max_threads = int(input("Enter max number of threads (e.g., 5): "))
    except ValueError:
        logging.warning("Invalid input. Using default value of 5.")
        max_threads = 5

    min_delay = float(input("Enter minimum delay between requests (e.g., 0.1): "))
    max_delay = float(input("Enter maximum delay between requests (e.g., 0.3): "))

    use_async = input("Use asynchronous mode for high volume? (y/n): ").strip().lower() == 'y'

    logging.info(f"Starting stress test on {target_url} with {num_requests} requests, "
                 f"using up to {max_threads} threads, and random delay between {min_delay}-{max_delay}s.")
    stress_test(target_url, num_requests, max_threads, min_delay, max_delay, use_async)

if __name__ == "__main__":
    main()
