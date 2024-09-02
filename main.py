import requests
import time
import docker

website_url = "https://libre-media.com"
container_name = "lm-api"
check_interval = 120 # Time in seconds for the interval 

# Docker client
docker_client = docker.from_env()

def check_website(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.RequestException as error:
        print(f"Libre-Media returned an error status : {error}")
        return None

def restart_docker_container(container_name):
    try:
        container = docker_client.containers.get(container_name)
        print(f"Restarting the api container {container_name}")
        container.restart()
        print("Container successfully restarted")
    except docker.errors.NotFound:
        print(f"Container {container_name} not found")
    except docker.errors.APIError as error:
        print(f"An error ocurred while restaring the container: {error}")


def monitor_website():
    while True:
        status_code = check_website(website_url)
        if status_code == 502:
            print("502 error detected. Restarting the api container")
            restart_docker_container(container_name)
        elif status_code:
            print(f"Libre-Media is running. Status code: {status_code}")
        else:
            print("Could not retrieve a status code. Is the script working?")

        time.sleep(check_interval)

if __name__ == "__main__":
    monitor_website()