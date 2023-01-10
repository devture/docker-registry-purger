# Docker Registry Purger

This is a small script used for purging a private Docker registry's old tags. It fetches the list of tags for an image, keeps `latest` and the most recent `NOF_TAGS_TO_KEEP` and deletes all other tags.

To actually reclaim the space, you'd need to also run the registry's [garbage collection](https://docs.docker.com/registry/garbage-collection/#run-garbage-collection).


## History

This is a fork of [blixhavn/docker-registry-retention](https://github.com/blixhavn/docker-registry-retention) which:

- adds `IMAGE_IGNORE_REGEX` / `DRY_RUN` support
- removes basic authentication support
- always keeps `latest` when deleting container image tags


## Prerequisites

A Docker registry must be run with [`storage.deleted.enabled`](https://docs.docker.com/registry/configuration/#delete) (e.g. `REGISTRY_STORAGE_DELETE_ENABLED=true`) to allow deletion.


## Environment variables

Set the following environment variables and run the docker image, e.g as a cron job.

|**Variable**         | **Description**                                                    | **Default value**|
|:--------------------|:-------------------------------------------------------------------|:-----------------|
|REGISTRY_URL         |Base URL of the registry, with protocol (e.g. https://)             | (undefined)      |
|NOF_TAGS_TO_KEEP     |Number of most recent tags to keep. `latest` is always kept.        | 3                |
|IMAGE_IGNORE_REGEX   |A regex for skipping processing of images (e.g. `postgres|alpine`)  | (undefined)      |
|DRY_RUN              |If set, performs a dry-run and does not delete anything             | (undefined)      |


## Usage

`docker run -it --rm -e REGISTRY_URL=https://registry.example.com -e NOF_TAGS_TO_KEEP=3 devture/docker-registry-purger:latest
