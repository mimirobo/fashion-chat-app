# Fashion Chat WebApp

This repository contains the implementation of ...

[[_TOC_]]

## Getting Started

## Prerequisites

- Python 3.12+
- pip (the Python package manager)
- Docker

#### 1. Network Configuration
> You can skip this part if you have already `fashion-chat-dev-network`

Set up a Docker network for service communication:

```shell
docker network create fashion-chat-dev-network
```


#### 2. Environment Setup

Create a `.env` file from the provided template and fill it with the required credentials and settings.
Template available at ["env.example"](./env.example).

<details>
<summary>
List of ENV. vars with sample and descriptions.
</summary>

| Environment Variable     | Sample Value                                             | Description                                                                                  |
|--------------------------|----------------------------------------------------------|----------------------------------------------------------------------------------------------|
| OPENAI_API_KEY           | ""                                                       | The API Key for your OPENAI account                                                          |
| API_PATH_PREFIX          | "/"                                                      | The default value is set to "/"                                                              |

</details>

#### 5. Building the Docker Image

```shell
docker compose build
```

#### 6. Launching the Container

```shell
docker compose up -d
```

> In case of running without docker, simply run `main.py` through your favorite IDE or in a command line.
> Just make sure that your environment variables in `.env` are set accordingly.

## Related Repositories

### Service Providing Repositories

- None

### Service Receiving Repositories

- None
