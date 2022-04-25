import json
import os
import logging
import requests
import sys

from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)

registry_url = os.getenv("REGISTRY_URL")
nof_tags_to_keep = int(os.getenv("NOF_TAGS_TO_KEEP", 3))
username = os.getenv("DOCKER_USERNAME")
password = os.getenv("DOCKER_PASSWORD")

if not registry_url:
    log.error("Registry URL not found. Please set REGISTRY_URL env variable.")
    sys.exit()

auth = HTTPBasicAuth(username, password) if (username and password) else None

result = requests.get(f"{registry_url}/v2/_catalog", auth=auth)
if result.status_code != 200:
    log.error("Could not fetch registry catalog. Please check parameters")
    sys.exit()
catalog = result.json()["repositories"]

stats = {image: 0 for image in catalog}
for image in catalog:
    result = requests.get(f"{registry_url}/v2/{image}/tags/list", auth=auth)
    tags = result.json()["tags"]

    tags_to_delete = tags[:-nof_tags_to_keep]

    for tag in tags_to_delete:
        manifests_url = f"{registry_url}/v2/{image}/manifests"
        headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
        result = requests.get(f"{manifests_url}/{tag}", auth=auth, headers=headers)
        if "Docker-Content-Digest" in result.headers:
            sha = result.headers["Docker-Content-Digest"]
            delete_result = requests.delete(f"{manifests_url}/{sha}", auth=auth)
            if delete_result.status_code == 202:
                stats[image] += 1
            else:
                log.error(f"Could not delete tag {tag} for image {image}")

        else:
            log.warning(f"Could not find digest sha for image tag {image}:{tag}")

print("Image cleanup completed. Number of tags deleted:")
print(json.dumps(stats, indent=4))