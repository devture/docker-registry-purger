# Docker Registry Retention

This is a small script used for maintaining a private Docker registry where all images have tags (e.g. when tagging images with github sha). It fetches the list of tags for an image and deletes all but the `NOF_TAGS_TO_KEEP` latest. Must be used in combination with Docker Registrys own [garbage collection](https://docs.docker.com/registry/garbage-collection/#run-garbage-collection) to actually delete files.

> NB! Docker registry must be run with `REGISTRY_STORAGE_DELETE_ENABLED=true` to allow deletion

## How to run
Set the following environment variables and run the docker image, e.g as a cron job.

|**Variable** | **Description** | **Default value** |
|:--|:--|:--|
|REGISTRY_URL|Base URL of the registry, with protocol (e.g. https://)   | - |
|NOF_TAGS_TO_KEEP|Number of tags to retain. Will always keep the most recent tags. | 3 |
|DOCKER_USERNAME|Username for basic auth against the registry. If username or password is omitted, basic auth will not be used. | - |
|DOCKER_PASSWORD|Password for basic auth against the registry. | - |
