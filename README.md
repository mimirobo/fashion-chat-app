# Fashion Chat WebApp

## Problem Statement

Fashion Chat WebApp is a FastAPI-based web application designed to focus exclusively on the topic of fashion.
In a world where conversational AI often struggles to maintain topical consistency,
this application aims to provide a seamless and focused user experience by ensuring that all queries and responses
are relevant to the fashion domain.

## Naive Approach

To solve the problem of maintaining topical relevance, the application leverages **zero-shot intent classification**
using the `facebook/bart-large-mnli` model from Hugging Face.
When a user inputs a query, the model calculates the similarity score of the input text against predefined keywords.
These keywords are assigned weights to reflect their importance in determining topical relevance.

The weighted average is then computed to evaluate how closely the user's query aligns with the fashion domain.
Based on this score, the application decides whether the query is fashion-related and generates an appropriate response.

### Example Keywords and Weights (Defined via Environment Variables)
```json
{
    "fashion": 1.0,
    "clothing": 1.0,
    "t-shirt": 1.0,
    "red": 0.3
}
```


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
