import docker
import docker.errors
import time
import os

def is_container_ready(container):
    container.reload()
    return container.status == 'running'
    

def wait_for_stable_status(container, stable_duration=3, interval=1):
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container=container):
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= stable_duration / interval:
            return True
        
        time.sleep(interval)
    return False


def start_database_container():
    scripts_dir = os.path.abspath('./scripts')
    client = docker.from_env()
    container_name = "test-db"

    try:
        existing_container = client.containers.get(container_name)
        print(f"Container {container_name} exist. Stopping and removing")
        existing_container.stop()
        existing_container.remove()
        print(f"Container {container_name} removed")

    except docker.errors.NotFound:
        print(f"Container {container_name} does not exist.")

    container_config ={
        "name": container_name,
        "image": "registry.sedrehgroup.ir/postgres:16-alpine",
        "detach": True,
        "ports": {"5432": "5433"},
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
        },
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
        "network_mode": "test_driven_fast_api_main"
    }

    container = client.containers.run(**container_config)
    while not is_container_ready(container=container):
        time.sleep(4)

    if not wait_for_stable_status(container):
        return RuntimeError("Container did not stabilize")

    return container
    
