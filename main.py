import json
import os
import requests
import sys
import re

registry_url = os.getenv("REGISTRY_URL")
if not registry_url:
    print("REGISTRY_URL is required")
    sys.exit(1)

nof_tags_to_keep = int(os.getenv("NOF_TAGS_TO_KEEP", 3))
image_ignore_regex_str = os.getenv("IMAGE_IGNORE_REGEX")
image_ignore_regex = (None if image_ignore_regex_str is None else re.compile(image_ignore_regex_str))
dry_run = os.getenv("DRY_RUN") is not None and os.getenv("DRY_RUN") not in ["0", "false", "False", "FALSE"]

if dry_run:
    print("Working in dry-run mode..")

result = requests.get(f"{registry_url}/v2/_catalog")
if result.status_code != 200:
    print("Could not fetch registry catalog. Please check parameters")
    sys.exit(2)
catalog = result.json()["repositories"]

stats = {image: 0 for image in catalog}
for image in catalog:
    if image_ignore_regex is not None:
        if image_ignore_regex.search(image) is not None:
            print("Skip {0} because it matches the ignore regex".format(image))
            continue

    print("Processing {0}..".format(image))

    result = requests.get(f"{registry_url}/v2/{image}/tags/list")
    tags = result.json()["tags"]

    if tags is None:
        print("Skip {0} due to no tags".format(image))
        continue

    tags = list(filter(lambda t: t != 'latest', tags))

    tags_to_delete = tags[:-nof_tags_to_keep]

    print("Tags to delete: ", tags_to_delete)

    for tag in tags_to_delete:
        print("{0}:{1} is a candidate for deletion".format(image, tag))

        if dry_run:
            continue

        print("Deleting {0}:{1}..".format(image, tag))

        manifests_url = f"{registry_url}/v2/{image}/manifests"
        headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}

        result = requests.get(f"{manifests_url}/{tag}", headers=headers)

        if "Docker-Content-Digest" not in result.headers:
            print(f"Could not find digest sha for {image}:{tag}")
            continue

        sha = result.headers["Docker-Content-Digest"]
        delete_result = requests.delete(f"{manifests_url}/{sha}")
        if delete_result.status_code != 202:
            print(f"Could not delete {image}:{tag}")
            continue

        stats[image] += 1

if not dry_run:
    print("Image cleanup completed. Number of tags actually deleted:")
    print(json.dumps(stats, indent=4))
