# Langchain - Retrieval

**Pages:** 16

---

## artist vectorstore for "prince" we'll get back the value "Prince", which we can then

**URL:** llms-txt#artist-vectorstore-for-"prince"-we'll-get-back-the-value-"prince",-which-we-can-then

---

## AzureOpenAIEmbeddings

**URL:** llms-txt#azureopenaiembeddings

**Contents:**
- Overview
  - Integration details
- Setup
  - Credentials

Source: https://docs.langchain.com/oss/javascript/integrations/text_embedding/azure_openai

[Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service/) is a cloud service to help you quickly develop generative AI experiences with a diverse set of prebuilt and curated models from OpenAI, Meta and beyond.

LangChain.js supports integration with [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service/) using the new Azure integration in the [OpenAI SDK](https://github.com/openai/openai-node).

You can learn more about Azure OpenAI and its difference with the OpenAI API on [this page](https://learn.microsoft.com/azure/ai-services/openai/overview). If you don't have an Azure account, you can [create a free account](https://azure.microsoft.com/free/) to get started.

This will help you get started with AzureOpenAIEmbeddings [embedding models](/oss/javascript/integrations/text_embedding) using LangChain. For detailed documentation on `AzureOpenAIEmbeddings` features and configuration options, please refer to the [API reference](https://api.js.langchain.com/classes/langchain_openai.AzureOpenAIEmbeddings.html).

<Info>
  **Previously, LangChain.js supported integration with Azure OpenAI using the dedicated [Azure OpenAI SDK](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai). This SDK is now deprecated in favor of the new Azure integration in the OpenAI SDK, which allows to access the latest OpenAI models and features the same day they are released, and allows seamless transition between the OpenAI API and Azure OpenAI.**

If you are using Azure OpenAI with the deprecated SDK, see the [migration guide](#migration-from-azure-openai-sdk) to update to the new API.
</Info>

### Integration details

| Class                                                                                                     | Package                                                                         | Local | [Py support](https://python.langchain.com/docs/integrations/text_embedding/azure_openai/) |                                             Downloads                                             |                                             Version                                            |
| :-------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------ | :---: | :---------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
| [AzureOpenAIEmbeddings](https://api.js.langchain.com/classes/langchain_openai.AzureOpenAIEmbeddings.html) | [@langchain/openai](https://api.js.langchain.com/modules/langchain_openai.html) |   ❌   |                                             ✅                                             | ![NPM - Downloads](https://img.shields.io/npm/dm/@langchain/openai?style=flat-square\&label=%20&) | ![NPM - Version](https://img.shields.io/npm/v/@langchain/openai?style=flat-square\&label=%20&) |

To access Azure OpenAI embedding models you'll need to create an Azure account, get an API key, and install the `@langchain/openai` integration package.

You'll need to have an Azure OpenAI instance deployed. You can deploy a version on Azure Portal following [this guide](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).

Once you have your instance running, make sure you have the name of your instance and key. You can find the key in the Azure Portal, under the "Keys and Endpoint" section of your instance.

If you're using Node.js, you can define the following environment variables to use the service:

If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.langchain.com/langsmith/home) API key by uncommenting below:

```bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.langchain.com/langsmith/home) API key by uncommenting below:
```

---

## BedrockEmbeddings

**URL:** llms-txt#bedrockembeddings

**Contents:**
- Overview
  - Integration details
- Setup
  - Credentials

Source: https://docs.langchain.com/oss/javascript/integrations/text_embedding/bedrock

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon via a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI.

This will help you get started with Amazon Bedrock [embedding models](/oss/javascript/integrations/text_embedding) using LangChain. For detailed documentation on `Bedrock` features and configuration options, please refer to the [API reference](https://api.js.langchain.com/classes/langchain_aws.BedrockEmbeddings.html).

### Integration details

| Class                                                                                | Package                                                                   | Local | [Py support](https://python.langchain.com/docs/integrations/text_embedding/bedrock/) |                                            Downloads                                           |                                           Version                                           |
| :----------------------------------------------------------------------------------- | :------------------------------------------------------------------------ | :---: | :----------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------: |
| [Bedrock](https://api.js.langchain.com/classes/langchain_aws.BedrockEmbeddings.html) | [@langchain/aws](https://api.js.langchain.com/modules/langchain_aws.html) |   ❌   |                                           ✅                                          | ![NPM - Downloads](https://img.shields.io/npm/dm/@langchain/aws?style=flat-square\&label=%20&) | ![NPM - Version](https://img.shields.io/npm/v/@langchain/aws?style=flat-square\&label=%20&) |

To access Bedrock embedding models you'll need to create an AWS account, get an API key, and install the `@langchain/aws` integration package.

Head to the [AWS docs](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html) to sign up for AWS and setup your credentials. You'll also need to turn on model access for your account, which you can do by [following these instructions](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html).

If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.langchain.com/langsmith/home) API key by uncommenting below:

```bash  theme={null}

---

## Create your underlying embeddings model

**URL:** llms-txt#create-your-underlying-embeddings-model

underlying_embeddings = ... # e.g., OpenAIEmbeddings(), HuggingFaceEmbeddings(), etc.

---

## Data storage and privacy

**URL:** llms-txt#data-storage-and-privacy

**Contents:**
- CLI
- Agent Server
  - LangSmith Tracing
  - In-memory development server
  - Standalone Server
- Studio
- Quick reference

Source: https://docs.langchain.com/langsmith/data-storage-and-privacy

This document describes how data is processed in the LangGraph CLI and the Agent Server for both the in-memory server (`langgraph dev`) and the local Docker server (`langgraph up`). It also describes what data is tracked when interacting with the hosted Studio frontend.

LangGraph **CLI** is the command-line interface for building and running LangGraph applications; see the [CLI guide](/langsmith/cli) to learn more.

By default, calls to most CLI commands log a single analytics event upon invocation. This helps us better prioritize improvements to the CLI experience. Each telemetry event contains the calling process's OS, OS version, Python version, the CLI version, the command name (`dev`, `up`, `run`, etc.), and booleans representing whether a flag was passed to the command. You can see the full analytics logic [here](https://github.com/langchain-ai/langgraph/blob/main/libs/cli/langgraph-cli/analytics.py).

You can disable all CLI telemetry by setting `LANGGRAPH_CLI_NO_ANALYTICS=1`.

<a id="in-memory-docker" />

The [Agent Server](/langsmith/agent-server) provides a durable execution runtime that relies on persisting checkpoints of your application state, long-term memories, thread metadata, assistants, and similar resources to the local file system or a database. Unless you have deliberately customized the storage location, this information is either written to local disk (for `langgraph dev`) or a PostgreSQL database (for `langgraph up` and in all deployments).

### LangSmith Tracing

When running the Agent server (either in-memory or in Docker), LangSmith tracing may be enabled to facilitate faster debugging and offer observability of graph state and LLM prompts in production. You can always disable tracing by setting `LANGSMITH_TRACING=false` in your server's runtime environment.

<a id="langgraph-dev" />

### In-memory development server

`langgraph dev` runs an [in-memory development server](/langsmith/local-server) as a single Python process, designed for quick development and testing. It saves all checkpointing and memory data to disk within a `.langgraph_api` directory in the current working directory. Apart from the telemetry data described in the [CLI](#cli) section, no data leaves the machine unless you have enabled tracing or your graph code explicitly contacts an external service.

<a id="langgraph-up" />

### Standalone Server

`langgraph up` builds your local package into a Docker image and runs the server as the [data plane](/langsmith/self-hosted) consisting of three containers: the API server, a PostgreSQL container, and a Redis container. All persistent data (checkpoints, assistants, etc.) are stored in the PostgreSQL database. Redis is used as a pubsub connection for real-time streaming of events. You can encrypt all checkpoints before saving to the database by setting a valid `LANGGRAPH_AES_KEY` environment variable. You can also specify [TTLs](/langsmith/configure-ttl) for checkpoints and cross-thread memories in `langgraph.json` to control how long data is stored. All persisted threads, memories, and other data can be deleted via the relevant API endpoints.

Additional API calls are made to confirm that the server has a valid license and to track the number of executed runs and tasks. Periodically, the API server validates the provided license key (or API key).

If you've disabled [tracing](#langsmith-tracing), no user data is persisted externally unless your graph code explicitly contacts an external service.

[Studio](/langsmith/studio) is a graphical interface for interacting with your Agent Server. It does not persist any private data (the data you send to your server is not sent to LangSmith). Though the Studio interface is served at [smith.langchain.com](https://smith.langchain.com), it is run in your browser and connects directly to your local Agent Server so that no data needs to be sent to LangSmith.

If you are logged in, LangSmith does collect some usage analytics to help improve the debugging user experience. This includes:

* Page visits and navigation patterns
* User actions (button clicks)
* Browser type and version
* Screen resolution and viewport size

Importantly, no application data or code (or other sensitive configuration details) are collected. All of that is stored in the persistence layer of your Agent Server. When using Studio anonymously, no account creation is required and usage analytics are not collected.

In summary, you can opt-out of server-side telemetry by turning off CLI analytics and disabling tracing.

| Variable                       | Purpose                   | Default                |
| ------------------------------ | ------------------------- | ---------------------- |
| `LANGGRAPH_CLI_NO_ANALYTICS=1` | Disable CLI analytics     | Analytics enabled      |
| `LANGSMITH_API_KEY`            | Enable LangSmith tracing  | Tracing disabled       |
| `LANGSMITH_TRACING=false`      | Disable LangSmith tracing | Depends on environment |

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/data-storage-and-privacy.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Embedding models

**URL:** llms-txt#embedding-models

**Contents:**
- Overview
  - How it works
  - Similarity metrics
- Interface
- Top integrations
- Caching

Source: https://docs.langchain.com/oss/python/integrations/text_embedding/index

<Note>
  This overview covers **text-based embedding models**. LangChain does not currently support multimodal embeddings.

See [top embedding models](#top-integrations).
</Note>

Embedding models transform raw text—such as a sentence, paragraph, or tweet—into a fixed-length vector of numbers that captures its **semantic meaning**. These vectors allow machines to compare and search text based on meaning rather than exact words.

In practice, this means that texts with similar ideas are placed close together in the vector space. For example, instead of matching only the phrase *"machine learning"*, embeddings can surface documents that discuss related concepts even when different wording is used.

1. **Vectorization** — The model encodes each input string as a high-dimensional vector.
2. **Similarity scoring** — Vectors are compared using mathematical metrics to measure how closely related the underlying texts are.

### Similarity metrics

Several metrics are commonly used to compare embeddings:

* **Cosine similarity** — measures the angle between two vectors.
* **Euclidean distance** — measures the straight-line distance between points.
* **Dot product** — measures how much one vector projects onto another.

Here's an example of computing cosine similarity between two vectors:

LangChain provides a standard interface for text embedding models (e.g., OpenAI, Cohere, Hugging Face) via the [Embeddings](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings) interface.

Two main methods are available:

* `embed_documents(texts: List[str]) → List[List[float]]`: Embeds a list of documents.
* `embed_query(text: str) → List[float]`: Embeds a single query.

<Note>
  The interface allows queries and documents to be embedded with different strategies, though most providers handle them the same way in practice.
</Note>

| Model                                                                                          | Package                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`OpenAIEmbeddings`](/oss/python/integrations/text_embedding/openai)                           | [`langchain-openai`](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html)                              |
| [`AzureOpenAIEmbeddings`](/oss/python/integrations/text_embedding/azure_openai)                | [`langchain-openai`](https://python.langchain.com/api_reference/openai/embeddings/langchain_openai.embeddings.azure.AzureOpenAIEmbeddings.html)                    |
| [`GoogleGenerativeAIEmbeddings`](/oss/python/integrations/text_embedding/google_generative_ai) | [`langchain-google-genai`](https://python.langchain.com/api_reference/google_genai/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html) |
| [`OllamaEmbeddings`](/oss/python/integrations/text_embedding/ollama)                           | [`langchain-ollama`](https://python.langchain.com/api_reference/ollama/embeddings/langchain_ollama.embeddings.OllamaEmbeddings.html)                               |
| [`TogetherEmbeddings`](/oss/python/integrations/text_embedding/together)                       | [`langchain-together`](https://python.langchain.com/api_reference/together/embeddings/langchain_together.embeddings.TogetherEmbeddings.html)                       |
| [`FireworksEmbeddings`](/oss/python/integrations/text_embedding/fireworks)                     | [`langchain-fireworks`](https://python.langchain.com/api_reference/fireworks/embeddings/langchain_fireworks.embeddings.FireworksEmbeddings.html)                   |
| [`MistralAIEmbeddings`](/oss/python/integrations/text_embedding/mistralai)                     | [`langchain-mistralai`](https://python.langchain.com/api_reference/mistralai/embeddings/langchain_mistralai.embeddings.MistralAIEmbeddings.html)                   |
| [`CohereEmbeddings`](/oss/python/integrations/text_embedding/cohere)                           | [`langchain-cohere`](https://python.langchain.com/api_reference/community/llms/langchain_community.llms.cohere.Cohere.html)                                        |
| [`NomicEmbeddings`](/oss/python/integrations/text_embedding/nomic)                             | [`langchain-nomic`](https://python.langchain.com/api_reference/nomic/embeddings/langchain_nomic.embeddings.NomicEmbeddings.html)                                   |
| [`FakeEmbeddings`](/oss/python/integrations/text_embedding/fake)                               | [`langchain-core`](https://python.langchain.com/api_reference/core/embeddings/langchain_core.embeddings.fake.FakeEmbeddings.html)                                  |
| [`DatabricksEmbeddings`](/oss/python/integrations/text_embedding/databricks)                   | [`databricks-langchain`](https://api-docs.databricks.com/python/databricks-ai-bridge/latest/databricks_langchain.html#databricks_langchain.DatabricksEmbeddings)   |
| [`WatsonxEmbeddings`](/oss/python/integrations/text_embedding/ibm_watsonx)                     | [`langchain-ibm`](https://python.langchain.com/api_reference/ibm/embeddings/langchain_ibm.embeddings.WatsonxEmbeddings.html)                                       |
| [`NVIDIAEmbeddings`](/oss/python/integrations/text_embedding/nvidia_ai_endpoints)              | [`langchain-nvidia`](https://python.langchain.com/api_reference/nvidia_ai_endpoints/embeddings/langchain_nvidia_ai_endpoints.embeddings.NVIDIAEmbeddings.html)     |
| [`AimlapiEmbeddings`](/oss/python/integrations/text_embedding/aimlapi)                         | [`langchain-aimlapi`](https://python.langchain.com/api_reference/aimlapi/embeddings/langchain_aimlapi.embeddings.AimlapiEmbeddings.html)                           |

Embeddings can be stored or temporarily cached to avoid needing to recompute them.

Caching embeddings can be done using a `CacheBackedEmbeddings`. This wrapper stores embeddings in a key-value store, where the text is hashed and the hash is used as the key in the cache.

The main supported way to initialize a `CacheBackedEmbeddings` is `from_bytes_store`. It takes the following parameters:

* **`underlying_embedder`**: The embedder to use for embedding.
* **`document_embedding_cache`**: Any [`ByteStore`](/oss/python/integrations/stores/) for caching document embeddings.
* **`batch_size`**: (optional, defaults to `None`) The number of documents to embed between store updates.
* **`namespace`**: (optional, defaults to `""`) The namespace to use for the document cache. Helps avoid collisions (e.g., set it to the embedding model name).
* **`query_embedding_cache`**: (optional, defaults to `None`) A [`ByteStore`](/oss/python/integrations/stores/) for caching query embeddings, or `True` to reuse the same store as `document_embedding_cache`.

<Important>
  - Always set the `namespace` parameter to avoid collisions when using different embedding models.
  - `CacheBackedEmbeddings` does not cache query embeddings by default. To enable this, specify a `query_embedding_cache`.
</Important>

```python  theme={null}
import time
from langchain_classic.embeddings import CacheBackedEmbeddings  # [!code highlight]
from langchain_classic.storage import LocalFileStore # [!code highlight]
from langchain_core.vectorstores import InMemoryVectorStore

**Examples:**

Example 1 (unknown):
```unknown
## Interface

LangChain provides a standard interface for text embedding models (e.g., OpenAI, Cohere, Hugging Face) via the [Embeddings](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings) interface.

Two main methods are available:

* `embed_documents(texts: List[str]) → List[List[float]]`: Embeds a list of documents.
* `embed_query(text: str) → List[float]`: Embeds a single query.

<Note>
  The interface allows queries and documents to be embedded with different strategies, though most providers handle them the same way in practice.
</Note>

## Top integrations

| Model                                                                                          | Package                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`OpenAIEmbeddings`](/oss/python/integrations/text_embedding/openai)                           | [`langchain-openai`](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html)                              |
| [`AzureOpenAIEmbeddings`](/oss/python/integrations/text_embedding/azure_openai)                | [`langchain-openai`](https://python.langchain.com/api_reference/openai/embeddings/langchain_openai.embeddings.azure.AzureOpenAIEmbeddings.html)                    |
| [`GoogleGenerativeAIEmbeddings`](/oss/python/integrations/text_embedding/google_generative_ai) | [`langchain-google-genai`](https://python.langchain.com/api_reference/google_genai/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html) |
| [`OllamaEmbeddings`](/oss/python/integrations/text_embedding/ollama)                           | [`langchain-ollama`](https://python.langchain.com/api_reference/ollama/embeddings/langchain_ollama.embeddings.OllamaEmbeddings.html)                               |
| [`TogetherEmbeddings`](/oss/python/integrations/text_embedding/together)                       | [`langchain-together`](https://python.langchain.com/api_reference/together/embeddings/langchain_together.embeddings.TogetherEmbeddings.html)                       |
| [`FireworksEmbeddings`](/oss/python/integrations/text_embedding/fireworks)                     | [`langchain-fireworks`](https://python.langchain.com/api_reference/fireworks/embeddings/langchain_fireworks.embeddings.FireworksEmbeddings.html)                   |
| [`MistralAIEmbeddings`](/oss/python/integrations/text_embedding/mistralai)                     | [`langchain-mistralai`](https://python.langchain.com/api_reference/mistralai/embeddings/langchain_mistralai.embeddings.MistralAIEmbeddings.html)                   |
| [`CohereEmbeddings`](/oss/python/integrations/text_embedding/cohere)                           | [`langchain-cohere`](https://python.langchain.com/api_reference/community/llms/langchain_community.llms.cohere.Cohere.html)                                        |
| [`NomicEmbeddings`](/oss/python/integrations/text_embedding/nomic)                             | [`langchain-nomic`](https://python.langchain.com/api_reference/nomic/embeddings/langchain_nomic.embeddings.NomicEmbeddings.html)                                   |
| [`FakeEmbeddings`](/oss/python/integrations/text_embedding/fake)                               | [`langchain-core`](https://python.langchain.com/api_reference/core/embeddings/langchain_core.embeddings.fake.FakeEmbeddings.html)                                  |
| [`DatabricksEmbeddings`](/oss/python/integrations/text_embedding/databricks)                   | [`databricks-langchain`](https://api-docs.databricks.com/python/databricks-ai-bridge/latest/databricks_langchain.html#databricks_langchain.DatabricksEmbeddings)   |
| [`WatsonxEmbeddings`](/oss/python/integrations/text_embedding/ibm_watsonx)                     | [`langchain-ibm`](https://python.langchain.com/api_reference/ibm/embeddings/langchain_ibm.embeddings.WatsonxEmbeddings.html)                                       |
| [`NVIDIAEmbeddings`](/oss/python/integrations/text_embedding/nvidia_ai_endpoints)              | [`langchain-nvidia`](https://python.langchain.com/api_reference/nvidia_ai_endpoints/embeddings/langchain_nvidia_ai_endpoints.embeddings.NVIDIAEmbeddings.html)     |
| [`AimlapiEmbeddings`](/oss/python/integrations/text_embedding/aimlapi)                         | [`langchain-aimlapi`](https://python.langchain.com/api_reference/aimlapi/embeddings/langchain_aimlapi.embeddings.AimlapiEmbeddings.html)                           |

## Caching

Embeddings can be stored or temporarily cached to avoid needing to recompute them.

Caching embeddings can be done using a `CacheBackedEmbeddings`. This wrapper stores embeddings in a key-value store, where the text is hashed and the hash is used as the key in the cache.

The main supported way to initialize a `CacheBackedEmbeddings` is `from_bytes_store`. It takes the following parameters:

* **`underlying_embedder`**: The embedder to use for embedding.
* **`document_embedding_cache`**: Any [`ByteStore`](/oss/python/integrations/stores/) for caching document embeddings.
* **`batch_size`**: (optional, defaults to `None`) The number of documents to embed between store updates.
* **`namespace`**: (optional, defaults to `""`) The namespace to use for the document cache. Helps avoid collisions (e.g., set it to the embedding model name).
* **`query_embedding_cache`**: (optional, defaults to `None`) A [`ByteStore`](/oss/python/integrations/stores/) for caching query embeddings, or `True` to reuse the same store as `document_embedding_cache`.

<Important>
  - Always set the `namespace` parameter to avoid collisions when using different embedding models.
  - `CacheBackedEmbeddings` does not cache query embeddings by default. To enable this, specify a `query_embedding_cache`.
</Important>
```

---

## Enable blob storage

**URL:** llms-txt#enable-blob-storage

**Contents:**
- Requirements
- Authentication
  - Amazon S3
  - Google Cloud Storage
  - Azure Blob Storage
- CH Search
- Configuration
- TTL Configuration
  - Amazon S3
  - Google Cloud Storage

Source: https://docs.langchain.com/langsmith/self-host-blob-storage

By default, LangSmith stores run inputs, outputs, errors, manifests, extras, and events in ClickHouse. If you so choose, you can instead store this information in blob storage, which has a couple of notable benefits. For the best results in production deployments, we **strongly** recommend using blob storage, which offers the following benefits:

1. In high trace environments, inputs, outputs, errors, manifests, extras, and events may balloon the size of your databases.
2. If using LangSmith Managed ClickHouse, you may want sensitive information in blob storage that resides in your environment. To alleviate this, LangSmith supports storing run inputs, outputs, errors, manifests, extras, events, and attachments in an external blob storage system.

<Note>
  Azure blob storage is available in Helm chart versions 0.8.9 and greater. [Deleting trace projects](/langsmith/observability-concepts#deleting-traces-from-langsmith) is supported in Azure starting in Helm chart version 0.10.43.
</Note>

* Access to a valid blob storage service

* [Amazon S3](https://aws.amazon.com/s3/)
    * [Google Cloud Storage (GCS)](https://cloud.google.com/storage?hl=en)
  * [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs)

* A bucket/directory in your blob storage to store the data. We highly recommend creating a separate bucket/directory for LangSmith data.
  * **If you are using TTLs**, you will need to set up a lifecycle policy to delete old data. You can find more information on configuring TTLs [here](/langsmith/self-host-ttl). These policies should mirror the TTLs you have set in your LangSmith configuration, or you may experience data loss. See [here](#ttl-configuration) on how to setup the lifecycle rules for TTLs for blob storage.

* Credentials to permit LangSmith Services to access the bucket/directory
  * You will need to provide your LangSmith instance with the necessary credentials to access the bucket/directory. Read the authentication [section](#authentication) below for more information.

* If using S3 or GCS, an API url for your blob storage service

* This will be the URL that LangSmith uses to access your blob storage system
  * For Amazon S3, this will be the URL of the S3 endpoint. Something like: `https://s3.amazonaws.com` or `https://s3.us-west-1.amazonaws.com` if using a regional endpoint.
  * For Google Cloud Storage, this will be the URL of the GCS endpoint. Something like: `https://storage.googleapis.com`

To authenticate to [Amazon S3](https://aws.amazon.com/s3/), you will need to create an IAM policy granting the following permissions on your bucket.

Once you have the correct policy, there are three ways to authenticate with Amazon S3:

1. [**(Recommended) IAM Role for Service Account**](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html): You can create an IAM role for your LangSmith instance and attach the policy to that role. You can then provide the role to LangSmith. This is the recommended way to authenticate with Amazon S3 in production.

1. You will need to create an IAM role with the policy attached.
   2. You will need to allow LangSmith service accounts to assume the role. The `langsmith-queue`, `langsmith-backend`, and `langsmith-platform-backend` service accounts will need to be able to assume the role.
      <Warning>
        The service account names will be different if you are using a custom release name. You can find the service account names by running `kubectl get serviceaccounts` in your cluster.
      </Warning>
   3. You will need to provide the role ARN to LangSmith. You can do this by adding the `eks.amazonaws.com/role-arn: "<role_arn>"` annotation to the `queue`, `backend`, and `platform-backend` services in your Helm Chart installation.

2. [**Access Key and Secret Key**](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): You can provide LangSmith with an access key and secret key. This is the simplest way to authenticate with Amazon S3. However, it is not recommended for production use as it is less secure.
   1. You will need to create a user with the policy attached. Then you can provision an access key and secret key for that user.

3. [**VPC Endpoint Access**](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html): You can enable access to your S3 bucket via a VPC endpoint, which allows traffic to flow securely from your VPC to your S3 bucket.

1. You'll need to provision a VPC endpoint and configure it to allow access to your S3 bucket.
   2. You can refer to our [public Terraform modules](https://github.com/langchain-ai/terraform/blob/main/modules/aws/s3/main.tf#L12) for guidance and an example of configuring this.

#### KMS encryption header support for S3

Starting with LangSmith Helm chart version **0.11.24**, you can pass a KMS encryption key header and enforce a specific KMS key for writes by providing its ARN. To enable this, set the following values in your Helm chart:

### Google Cloud Storage

To authenticate with [Google Cloud Storage](https://cloud.google.com/storage?hl=en), you will need to create a [`service account`](https://cloud.google.com/iam/docs/service-account-overview) with the necessary permissions to access your bucket.

Your service account will need the `Storage Admin` role or a custom role with equivalent permissions. This can be scoped to the bucket that LangSmith will be using.

Once you have a provisioned service account, you will need to generate a [`HMAC key`](https://cloud.google.com/storage/docs/authentication/hmackeys) for that service account. This key and secret will be used to authenticate with Google Cloud Storage.

### Azure Blob Storage

To authenticate with [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs), you will need to use one of the following methods to grant LangSmith workloads permission to access your [container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#containers) (listed in order of precedence):

1. [Storage account and access key](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage)
2. [Connection string](https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string)
3. [Workload identity](https://azure.github.io/azure-workload-identity/docs/introduction.html) (recommended), managed identity, or environment variables supported by [`DefaultAzureCredential`](https://learn.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication?tabs=bash#2-authenticate-with-azure). This is the default authentication method when configuration for either option above is not present.
   1. To use workload identity, add the label `azure.workload.identity/use: true` to the `queue`, `backend`, and `platform-backend` deployments. Additionally, add the `azure.workload.identity/client-id` annotation to the corresponding service accounts, which should be an existing Azure AD Application's client ID or user-assigned managed identity's client ID. See [Azure's documentation](https://azure.github.io/azure-workload-identity/docs/topics/service-account-labels-and-annotations.html) for additional details.

<Note>
  Some deployments may need further customization of the connection configuration using a Service URL Override instead of the default service URL (`https://<storage_account_name>.blob.core.windows.net/`). For example, this override is necessary in order to use a different blob storage domain (e.g. government or china).
</Note>

By default, LangSmith will still store tokens for search in ClickHouse. If you are using LangSmith Managed Clickhouse, you may want to disable this feature to avoid sending potentially sensitive information to ClickHouse. You can do this in your blob storage configuration.

After creating your bucket and obtaining the necessary credentials, you can configure LangSmith to use your blob storage system.

<Note>
  Google Cloud Storage (GCS) exposes an S3-compatible API. When using GCS, set the blob storage engine to "S3", configure the <code>apiURL</code> to your GCS endpoint (for example, <code>[https://storage.googleapis.com](https://storage.googleapis.com)</code>), and authenticate using a service account HMAC access key and secret (using `accessKey` and `accessKeySecret`).

You must use **HMAC** access key and secret for GCS. We do not support service account annotations.
</Note>

<Note>
  If using an access key and secret, you can also provide an existing Kubernetes secret that contains the authentication information. This is recommended over providing the access key and secret key directly in your config. See the [generated secret template](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/secrets.yaml) for the expected secret keys.
</Note>

If using the [TTL](/langsmith/self-host-ttl) feature with LangSmith, you'll also have to configure TTL rules for your blob storage. Trace information stored on blob storage is stored on a particular prefix path, which determines the TTL for the data. When a trace's retention is extended, its corresponding blob storage path changes to ensure that it matches the new extended retention.

The following TTL prefix are used:

* `ttl_s/`: Short term TTL, configured for 14 days.
* `ttl_l/`: Long term TTL, configured for 400 days.

If you have customized the TTLs in your LangSmith configuration, you will need to adjust the TTLs in your blob storage configuration to match.

If using S3 for your blob storage, you will need to setup a filter lifecycle configuration that matches the prefixes above. You can find information for this [in the Amazon Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html#intro-lifecycle-rules-filter).

As an example, if you are using Terraform to manage your S3 bucket, you would setup something like this:

### Google Cloud Storage

You will need to setup lifecycle conditions for your GCS buckets that you are using. You can find information for this [in the Google Documentation](https://cloud.google.com/storage/docs/lifecycle#conditions), specifically using matchesPrefix.

As an example, if you are using Terraform to manage your GCS bucket, you would setup something like this:

### Azure blob storage

You will need to configure a [lifecycle management policy](https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-policy-configure) on the container in order to expire objects matching the prefixes above.

As an example, if you are [using Terraform to manage your blob storage container](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_management_policy), you would setup something like this:

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/self-host-blob-storage.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
Once you have the correct policy, there are three ways to authenticate with Amazon S3:

1. [**(Recommended) IAM Role for Service Account**](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html): You can create an IAM role for your LangSmith instance and attach the policy to that role. You can then provide the role to LangSmith. This is the recommended way to authenticate with Amazon S3 in production.

   1. You will need to create an IAM role with the policy attached.
   2. You will need to allow LangSmith service accounts to assume the role. The `langsmith-queue`, `langsmith-backend`, and `langsmith-platform-backend` service accounts will need to be able to assume the role.
      <Warning>
        The service account names will be different if you are using a custom release name. You can find the service account names by running `kubectl get serviceaccounts` in your cluster.
      </Warning>
   3. You will need to provide the role ARN to LangSmith. You can do this by adding the `eks.amazonaws.com/role-arn: "<role_arn>"` annotation to the `queue`, `backend`, and `platform-backend` services in your Helm Chart installation.

2. [**Access Key and Secret Key**](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): You can provide LangSmith with an access key and secret key. This is the simplest way to authenticate with Amazon S3. However, it is not recommended for production use as it is less secure.
   1. You will need to create a user with the policy attached. Then you can provision an access key and secret key for that user.

3. [**VPC Endpoint Access**](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html): You can enable access to your S3 bucket via a VPC endpoint, which allows traffic to flow securely from your VPC to your S3 bucket.

   1. You'll need to provision a VPC endpoint and configure it to allow access to your S3 bucket.
   2. You can refer to our [public Terraform modules](https://github.com/langchain-ai/terraform/blob/main/modules/aws/s3/main.tf#L12) for guidance and an example of configuring this.

#### KMS encryption header support for S3

Starting with LangSmith Helm chart version **0.11.24**, you can pass a KMS encryption key header and enforce a specific KMS key for writes by providing its ARN. To enable this, set the following values in your Helm chart:
```

Example 2 (unknown):
```unknown
### Google Cloud Storage

To authenticate with [Google Cloud Storage](https://cloud.google.com/storage?hl=en), you will need to create a [`service account`](https://cloud.google.com/iam/docs/service-account-overview) with the necessary permissions to access your bucket.

Your service account will need the `Storage Admin` role or a custom role with equivalent permissions. This can be scoped to the bucket that LangSmith will be using.

Once you have a provisioned service account, you will need to generate a [`HMAC key`](https://cloud.google.com/storage/docs/authentication/hmackeys) for that service account. This key and secret will be used to authenticate with Google Cloud Storage.

### Azure Blob Storage

To authenticate with [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs), you will need to use one of the following methods to grant LangSmith workloads permission to access your [container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#containers) (listed in order of precedence):

1. [Storage account and access key](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage)
2. [Connection string](https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string)
3. [Workload identity](https://azure.github.io/azure-workload-identity/docs/introduction.html) (recommended), managed identity, or environment variables supported by [`DefaultAzureCredential`](https://learn.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication?tabs=bash#2-authenticate-with-azure). This is the default authentication method when configuration for either option above is not present.
   1. To use workload identity, add the label `azure.workload.identity/use: true` to the `queue`, `backend`, and `platform-backend` deployments. Additionally, add the `azure.workload.identity/client-id` annotation to the corresponding service accounts, which should be an existing Azure AD Application's client ID or user-assigned managed identity's client ID. See [Azure's documentation](https://azure.github.io/azure-workload-identity/docs/topics/service-account-labels-and-annotations.html) for additional details.

<Note>
  Some deployments may need further customization of the connection configuration using a Service URL Override instead of the default service URL (`https://<storage_account_name>.blob.core.windows.net/`). For example, this override is necessary in order to use a different blob storage domain (e.g. government or china).
</Note>

## CH Search

By default, LangSmith will still store tokens for search in ClickHouse. If you are using LangSmith Managed Clickhouse, you may want to disable this feature to avoid sending potentially sensitive information to ClickHouse. You can do this in your blob storage configuration.

## Configuration

After creating your bucket and obtaining the necessary credentials, you can configure LangSmith to use your blob storage system.

<Note>
  Google Cloud Storage (GCS) exposes an S3-compatible API. When using GCS, set the blob storage engine to "S3", configure the <code>apiURL</code> to your GCS endpoint (for example, <code>[https://storage.googleapis.com](https://storage.googleapis.com)</code>), and authenticate using a service account HMAC access key and secret (using `accessKey` and `accessKeySecret`).

  You must use **HMAC** access key and secret for GCS. We do not support service account annotations.
</Note>

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

<Note>
  If using an access key and secret, you can also provide an existing Kubernetes secret that contains the authentication information. This is recommended over providing the access key and secret key directly in your config. See the [generated secret template](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/secrets.yaml) for the expected secret keys.
</Note>

## TTL Configuration

If using the [TTL](/langsmith/self-host-ttl) feature with LangSmith, you'll also have to configure TTL rules for your blob storage. Trace information stored on blob storage is stored on a particular prefix path, which determines the TTL for the data. When a trace's retention is extended, its corresponding blob storage path changes to ensure that it matches the new extended retention.

The following TTL prefix are used:

* `ttl_s/`: Short term TTL, configured for 14 days.
* `ttl_l/`: Long term TTL, configured for 400 days.

If you have customized the TTLs in your LangSmith configuration, you will need to adjust the TTLs in your blob storage configuration to match.

### Amazon S3

If using S3 for your blob storage, you will need to setup a filter lifecycle configuration that matches the prefixes above. You can find information for this [in the Amazon Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html#intro-lifecycle-rules-filter).

As an example, if you are using Terraform to manage your S3 bucket, you would setup something like this:
```

---

## Evaluate a RAG application

**URL:** llms-txt#evaluate-a-rag-application

**Contents:**
- Overview
- Setup
  - Environment
  - Application
- Dataset
- Evaluators
  - Correctness: Response vs reference answer
  - Relevance: Response vs input
  - Groundedness: Response vs retrieved docs
  - Retrieval relevance: Retrieved docs vs input

Source: https://docs.langchain.com/langsmith/evaluate-rag-tutorial

<Info>
  [RAG evaluation](/langsmith/evaluation-concepts#retrieval-augmented-generation-rag) | [Evaluators](/langsmith/evaluation-concepts#evaluators) | [LLM-as-judge evaluators](/langsmith/evaluation-concepts#llm-as-judge)
</Info>

Retrieval Augmented Generation (RAG) is a technique that enhances Large Language Models (LLMs) by providing them with relevant external knowledge. It has become one of the most widely used approaches for building LLM applications.

This tutorial will show you how to evaluate your RAG applications using LangSmith. You'll learn:

1. How to create test datasets
2. How to run your RAG application on those datasets
3. How to measure your application's performance using different evaluation metrics

A typical RAG evaluation workflow consists of three main steps:

1. Creating a dataset with questions and their expected answers

2. Running your RAG application on those questions

3. Using evaluators to measure how well your application performed, looking at factors like:

* Answer relevance
   * Answer accuracy
   * Retrieval quality

For this tutorial, we'll create and evaluate a bot that answers questions about a few of [Lilian Weng's](https://lilianweng.github.io/) insightful blog posts.

First, let's set our environment variables:

And install the dependencies we'll need:

<Info>
  While this tutorial uses LangChain, the evaluation techniques and LangSmith functionality demonstrated here work with any framework. Feel free to use your preferred tools and libraries.
</Info>

In this section, we'll build a basic Retrieval-Augmented Generation (RAG) application.

We'll stick to a simple implementation that:

* Indexing: chunks and indexes a few of Lilian Weng's blogs in a vector store
* Retrieval: retrieves those chunks based on the user question
* Generation: passes the question and retrieved docs to an LLM.

#### Indexing and retrieval

First, lets load the blog posts we want to build a chatbot for and index them.

We can now define the generative pipeline.

Now that we've got our application, let's build a dataset to evaluate it. Our dataset will be very simple in this case: we'll have example questions and reference answers.

One way to think about different types of RAG evaluators is as a tuple of what is being evaluated X what its being evaluated against:

1. **Correctness**: Response vs reference answer

* `Goal`: Measure "*how similar/correct is the RAG chain answer, relative to a ground-truth answer*"
* `Mode`: Requires a ground truth (reference) answer supplied through a dataset
* `Evaluator`: Use LLM-as-judge to assess answer correctness.

2. **Relevance**: Response vs input

* `Goal`: Measure "*how well does the generated response address the initial user input*"
* `Mode`: Does not require reference answer, because it will compare the answer to the input question
* `Evaluator`: Use LLM-as-judge to assess answer relevance, helpfulness, etc.

3. **Groundedness**: Response vs retrieved docs

* `Goal`: Measure "*to what extent does the generated response agree with the retrieved context*"
* `Mode`: Does not require reference answer, because it will compare the answer to the retrieved context
* `Evaluator`: Use LLM-as-judge to assess faithfulness, hallucinations, etc.

4. **Retrieval relevance**: Retrieved docs vs input

* `Goal`: Measure "*how relevant are my retrieved results for this query*"
* `Mode`: Does not require reference answer, because it will compare the question to the retrieved context
* `Evaluator`: Use LLM-as-judge to assess relevance

<img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rag-eval-overview.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=6f303c2a284296b42e7d2d2e658f5171" alt="Rag eval overview" data-og-width="1252" width="1252" data-og-height="547" height="547" data-path="langsmith/images/rag-eval-overview.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rag-eval-overview.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=b5531116cdd61ca9e8ea6fcd760643db 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rag-eval-overview.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=8f83816ac849c05dd8d3dee4c9670729 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rag-eval-overview.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=8656d8f8af7ffa7f2684376cf2f70874 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rag-eval-overview.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=4299367332fbefd15e938aefc23ca6fe 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rag-eval-overview.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=0bc19645279f119031a5cb8ca32f2f7d 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rag-eval-overview.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=185b7c4ba4f4127f780d5fa17b96c752 2500w" />

### Correctness: Response vs reference answer

### Relevance: Response vs input

The flow is similar to above, but we simply look at the `inputs` and `outputs` without needing the `reference_outputs`. Without a reference answer we can't grade accuracy, but can still grade relevance—as in, did the model address the user's question or not.

### Groundedness: Response vs retrieved docs

Another useful way to evaluate responses without needing reference answers is to check if the response is justified by (or "grounded in") the retrieved documents.

### Retrieval relevance: Retrieved docs vs input

We can now kick off our evaluation job with all of our different evaluators.

You can see an example of what these results look like here: [LangSmith link](https://smith.langchain.com/public/302573e2-20bf-4f8c-bdad-e97c20f33f1b/d)

<Accordion title="Here's a consolidated script with all the above code:">
  <CodeGroup>

</CodeGroup>
</Accordion>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/evaluate-rag-tutorial.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
</CodeGroup>

And install the dependencies we'll need:

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

### Application

<Info>
  While this tutorial uses LangChain, the evaluation techniques and LangSmith functionality demonstrated here work with any framework. Feel free to use your preferred tools and libraries.
</Info>

In this section, we'll build a basic Retrieval-Augmented Generation (RAG) application.

We'll stick to a simple implementation that:

* Indexing: chunks and indexes a few of Lilian Weng's blogs in a vector store
* Retrieval: retrieves those chunks based on the user question
* Generation: passes the question and retrieved docs to an LLM.

#### Indexing and retrieval

First, lets load the blog posts we want to build a chatbot for and index them.

<CodeGroup>
```

---

## How to evaluate an application's intermediate steps

**URL:** llms-txt#how-to-evaluate-an-application's-intermediate-steps

**Contents:**
- 1. Define your LLM pipeline
- 2. Create a dataset and examples to evaluate the pipeline
- 3. Define your custom evaluators
- 4. Evaluate the pipeline
- Related

Source: https://docs.langchain.com/langsmith/evaluate-on-intermediate-steps

While, in many scenarios, it is sufficient to evaluate the final output of your task, in some cases you might want to evaluate the intermediate steps of your pipeline.

For example, for retrieval-augmented generation (RAG), you might want to

1. Evaluate the retrieval step to ensure that the correct documents are retrieved w\.r.t the input query.
2. Evaluate the generation step to ensure that the correct answer is generated w\.r.t the retrieved documents.

In this guide, we will use a simple, fully-custom evaluator for evaluating criteria 1 and an LLM-based evaluator for evaluating criteria 2 to highlight both scenarios.

In order to evaluate the intermediate steps of your pipeline, your evaluator function should traverse and process the `run`/`rootRun` argument, which is a `Run` object that contains the intermediate steps of your pipeline.

## 1. Define your LLM pipeline

The below RAG pipeline consists of 1) generating a Wikipedia query given the input question, 2) retrieving relevant documents from Wikipedia, and 3) generating an answer given the retrieved documents.

Requires `langsmith>=0.3.13`

This pipeline will produce a trace that looks something like: <img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=3b691ca56f9d60035dcba2c248692fa1" alt="evaluation_intermediate_trace.png" data-og-width="2586" width="2586" data-og-height="1676" height="1676" data-path="langsmith/images/evaluation-intermediate-trace.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=23a9b9abdb3e43e0f6326f0d4293ab7d 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=4b771691bd1afffe9f371a105f7eaebe 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=beb01776de9a5fa663c82d4380bc78cd 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=ec84bd3345df3d2cef38878b902c355b 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=043a7f22da6b158e070c853d67bacd69 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=42a9ea799157fee30a6b243c02615a02 2500w" />

## 2. Create a dataset and examples to evaluate the pipeline

We are building a very simple dataset with a couple of examples to evaluate the pipeline.

Requires `langsmith>=0.3.13`

## 3. Define your custom evaluators

As mentioned above, we will define two evaluators: one that evaluates the relevance of the retrieved documents w\.r.t the input query and another that evaluates the hallucination of the generated answer w\.r.t the retrieved documents. We will be using LangChain LLM wrappers, along with [`with_structured_output`](https://python.langchain.com/v0.1/docs/modules/model_io/chat/structured_output/) to define the evaluator for hallucination.

The key here is that the evaluator function should traverse the `run` / `rootRun` argument to access the intermediate steps of the pipeline. The evaluator can then process the inputs and outputs of the intermediate steps to evaluate according to the desired criteria.

Example uses `langchain` for convenience, this is not required.

## 4. Evaluate the pipeline

Finally, we'll run `evaluate` with the custom evaluators defined above.

The experiment will contain the results of the evaluation, including the scores and comments from the evaluators: <img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-experiment.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=e926744573c6b9757ba22ff245a3da2c" alt="evaluation_intermediate_experiment.png" data-og-width="2446" width="2446" data-og-height="1244" height="1244" data-path="langsmith/images/evaluation-intermediate-experiment.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-experiment.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7b6e321b15a06b2adc7f1cacb8e07a35 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-experiment.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=c677007bcc1e2af4b3767d6b44fcb327 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-experiment.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=a39153399b6721b7c51693f5a59cf2b0 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-experiment.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=1132228eba6761a724ae98d85fcf536c 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-experiment.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=5d74785384737df0cf67145b397b1934 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-experiment.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=bef00e4bdc12289d9f1e4b77ed8489cf 2500w" />

* [Evaluate a `langgraph` graph](/langsmith/evaluate-on-intermediate-steps)

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/evaluate-on-intermediate-steps.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
</CodeGroup>

Requires `langsmith>=0.3.13`

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

This pipeline will produce a trace that looks something like: <img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=3b691ca56f9d60035dcba2c248692fa1" alt="evaluation_intermediate_trace.png" data-og-width="2586" width="2586" data-og-height="1676" height="1676" data-path="langsmith/images/evaluation-intermediate-trace.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=23a9b9abdb3e43e0f6326f0d4293ab7d 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=4b771691bd1afffe9f371a105f7eaebe 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=beb01776de9a5fa663c82d4380bc78cd 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=ec84bd3345df3d2cef38878b902c355b 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=043a7f22da6b158e070c853d67bacd69 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/evaluation-intermediate-trace.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=42a9ea799157fee30a6b243c02615a02 2500w" />

## 2. Create a dataset and examples to evaluate the pipeline

We are building a very simple dataset with a couple of examples to evaluate the pipeline.

Requires `langsmith>=0.3.13`

<CodeGroup>
```

---

## Human-in-the-loop leverages LangGraph's persistence layer.

**URL:** llms-txt#human-in-the-loop-leverages-langgraph's-persistence-layer.

---

## OpenAIEmbeddings

**URL:** llms-txt#openaiembeddings

**Contents:**
- Overview
  - Integration details
- Setup
  - Credentials

Source: https://docs.langchain.com/oss/javascript/integrations/text_embedding/openai

This will help you get started with OpenAIEmbeddings [embedding models](/oss/javascript/integrations/text_embedding) using LangChain. For detailed documentation on `OpenAIEmbeddings` features and configuration options, please refer to the [API reference](https://api.js.langchain.com/classes/langchain_openai.OpenAIEmbeddings.html).

### Integration details

| Class                                                                                           | Package                                                                         | Local | [Py support](https://python.langchain.com/docs/integrations/text_embedding/openai/) |                                             Downloads                                             |                                             Version                                            |
| :---------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------ | :---: | :---------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
| [OpenAIEmbeddings](https://api.js.langchain.com/classes/langchain_openai.OpenAIEmbeddings.html) | [@langchain/openai](https://api.js.langchain.com/modules/langchain_openai.html) |   ❌   |                                          ✅                                          | ![NPM - Downloads](https://img.shields.io/npm/dm/@langchain/openai?style=flat-square\&label=%20&) | ![NPM - Version](https://img.shields.io/npm/v/@langchain/openai?style=flat-square\&label=%20&) |

To access OpenAIEmbeddings embedding models you'll need to create an OpenAI account, get an API key, and install the `@langchain/openai` integration package.

Head to [platform.openai.com](https://platform.openai.com) to sign up to OpenAI and generate an API key. Once you've done this set the `OPENAI_API_KEY` environment variable:

If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.langchain.com/langsmith/home) API key by uncommenting below:

```bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.langchain.com/langsmith/home) API key by uncommenting below:
```

---

## Retrieval

**URL:** llms-txt#retrieval

**Contents:**
- Building a knowledge base
  - From retrieval to RAG
  - Retrieval Pipeline
  - Building Blocks
- RAG Architectures
  - 2-step RAG
  - Agentic RAG
  - Hybrid RAG

Source: https://docs.langchain.com/oss/python/langchain/retrieval

Large Language Models (LLMs) are powerful, but they have two key limitations:

* **Finite context** — they can’t ingest entire corpora at once.
* **Static knowledge** — their training data is frozen at a point in time.

Retrieval addresses these problems by fetching relevant external knowledge at query time. This is the foundation of **Retrieval-Augmented Generation (RAG)**: enhancing an LLM’s answers with context-specific information.

## Building a knowledge base

A **knowledge base** is a repository of documents or structured data used during retrieval.

If you need a custom knowledge base, you can use LangChain’s document loaders and vector stores to build one from your own data.

<Note>
  If you already have a knowledge base (e.g., a SQL database, CRM, or internal documentation system), you do **not** need to rebuild it. You can:

* Connect it as a **tool** for an agent in Agentic RAG.
  * Query it and supply the retrieved content as context to the LLM [(2-Step RAG)](#2-step-rag).
</Note>

See the following tutorial to build a searchable knowledge base and minimal RAG workflow:

<Card title="Tutorial: Semantic search" icon="database" href="/oss/python/langchain/knowledge-base" arrow cta="Learn more">
  Learn how to create a searchable knowledge base from your own data using LangChain’s document loaders, embeddings, and vector stores.
  In this tutorial, you’ll build a search engine over a PDF, enabling retrieval of passages relevant to a query. You’ll also implement a minimal RAG workflow on top of this engine to see how external knowledge can be integrated into LLM reasoning.
</Card>

### From retrieval to RAG

Retrieval allows LLMs to access relevant context at runtime. But most real-world applications go one step further: they **integrate retrieval with generation** to produce grounded, context-aware answers.

This is the core idea behind **Retrieval-Augmented Generation (RAG)**. The retrieval pipeline becomes a foundation for a broader system that combines search with generation.

### Retrieval Pipeline

A typical retrieval workflow looks like this:

Each component is modular: you can swap loaders, splitters, embeddings, or vector stores without rewriting the app’s logic.

<Columns cols={2}>
  <Card title="Document loaders" icon="file-import" href="/oss/python/integrations/document_loaders" arrow cta="Learn more">
    Ingest data from external sources (Google Drive, Slack, Notion, etc.), returning standardized [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) objects.
  </Card>

<Card title="Text splitters" icon="scissors" href="/oss/python/integrations/splitters" arrow cta="Learn more">
    Break large docs into smaller chunks that will be retrievable individually and fit within a model's context window.
  </Card>

<Card title="Embedding models" icon="diagram-project" href="/oss/python/integrations/text_embedding" arrow cta="Learn more">
    An embedding model turns text into a vector of numbers so that texts with similar meaning land close together in that vector space.
  </Card>

<Card title="Vector stores" icon="database" href="/oss/python/integrations/vectorstores/" arrow cta="Learn more">
    Specialized databases for storing and searching embeddings.
  </Card>

<Card title="Retrievers" icon="binoculars" href="/oss/python/integrations/retrievers/" arrow cta="Learn more">
    A retriever is an interface that returns documents given an unstructured query.
  </Card>
</Columns>

RAG can be implemented in multiple ways, depending on your system's needs. We outline each type in the sections below.

| Architecture    | Description                                                                | Control   | Flexibility | Latency    | Example Use Case                                  |
| --------------- | -------------------------------------------------------------------------- | --------- | ----------- | ---------- | ------------------------------------------------- |
| **2-Step RAG**  | Retrieval always happens before generation. Simple and predictable         | ✅ High    | ❌ Low       | ⚡ Fast     | FAQs, documentation bots                          |
| **Agentic RAG** | An LLM-powered agent decides *when* and *how* to retrieve during reasoning | ❌ Low     | ✅ High      | ⏳ Variable | Research assistants with access to multiple tools |
| **Hybrid**      | Combines characteristics of both approaches with validation steps          | ⚖️ Medium | ⚖️ Medium   | ⏳ Variable | Domain-specific Q\&A with quality validation      |

<Info>
  **Latency**: Latency is generally more **predictable** in **2-Step RAG**, as the maximum number of LLM calls is known and capped. This predictability assumes that LLM inference time is the dominant factor. However, real-world latency may also be affected by the performance of retrieval steps—such as API response times, network delays, or database queries—which can vary based on the tools and infrastructure in use.
</Info>

In **2-Step RAG**, the retrieval step is always executed before the generation step. This architecture is straightforward and predictable, making it suitable for many applications where the retrieval of relevant documents is a clear prerequisite for generating an answer.

<Card title="Tutorial: Retrieval-Augmented Generation (RAG)" icon="robot" href="/oss/python/langchain/rag#rag-chains" arrow cta="Learn more">
  See how to build a Q\&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation.
  This tutorial walks through two approaches:

* A **RAG agent** that runs searches with a flexible tool—great for general-purpose use.
  * A **2-step RAG** chain that requires just one LLM call per query—fast and efficient for simpler tasks.
</Card>

**Agentic Retrieval-Augmented Generation (RAG)** combines the strengths of Retrieval-Augmented Generation with agent-based reasoning. Instead of retrieving documents before answering, an agent (powered by an LLM) reasons step-by-step and decides **when** and **how** to retrieve information during the interaction.

<Tip>
  The only thing an agent needs to enable RAG behavior is access to one or more **tools** that can fetch external knowledge — such as documentation loaders, web APIs, or database queries.
</Tip>

<Expandable title="Extended example: Agentic RAG for LangGraph's llms.txt">
  This example implements an **Agentic RAG system** to assist users in querying LangGraph documentation. The agent begins by loading [llms.txt](https://llmstxt.org/), which lists available documentation URLs, and can then dynamically use a `fetch_documentation` tool to retrieve and process the relevant content based on the user’s question.

<Card title="Tutorial: Retrieval-Augmented Generation (RAG)" icon="robot" href="/oss/python/langchain/rag" arrow cta="Learn more">
  See how to build a Q\&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation.
  This tutorial walks through two approaches:

* A **RAG agent** that runs searches with a flexible tool—great for general-purpose use.
  * A **2-step RAG** chain that requires just one LLM call per query—fast and efficient for simpler tasks.
</Card>

Hybrid RAG combines characteristics of both 2-Step and Agentic RAG. It introduces intermediate steps such as query preprocessing, retrieval validation, and post-generation checks. These systems offer more flexibility than fixed pipelines while maintaining some control over execution.

Typical components include:

* **Query enhancement**: Modify the input question to improve retrieval quality. This can involve rewriting unclear queries, generating multiple variations, or expanding queries with additional context.
* **Retrieval validation**: Evaluate whether retrieved documents are relevant and sufficient. If not, the system may refine the query and retrieve again.
* **Answer validation**: Check the generated answer for accuracy, completeness, and alignment with source content. If needed, the system can regenerate or revise the answer.

The architecture often supports multiple iterations between these steps:

This architecture is suitable for:

* Applications with ambiguous or underspecified queries
* Systems that require validation or quality control steps
* Workflows involving multiple sources or iterative refinement

<Card title="Tutorial: Agentic RAG with Self-Correction" icon="robot" href="/oss/python/langgraph/agentic-rag" arrow cta="Learn more">
  An example of **Hybrid RAG** that combines agentic reasoning with retrieval and self-correction.
</Card>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/retrieval.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
Each component is modular: you can swap loaders, splitters, embeddings, or vector stores without rewriting the app’s logic.

### Building Blocks

<Columns cols={2}>
  <Card title="Document loaders" icon="file-import" href="/oss/python/integrations/document_loaders" arrow cta="Learn more">
    Ingest data from external sources (Google Drive, Slack, Notion, etc.), returning standardized [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) objects.
  </Card>

  <Card title="Text splitters" icon="scissors" href="/oss/python/integrations/splitters" arrow cta="Learn more">
    Break large docs into smaller chunks that will be retrievable individually and fit within a model's context window.
  </Card>

  <Card title="Embedding models" icon="diagram-project" href="/oss/python/integrations/text_embedding" arrow cta="Learn more">
    An embedding model turns text into a vector of numbers so that texts with similar meaning land close together in that vector space.
  </Card>

  <Card title="Vector stores" icon="database" href="/oss/python/integrations/vectorstores/" arrow cta="Learn more">
    Specialized databases for storing and searching embeddings.
  </Card>

  <Card title="Retrievers" icon="binoculars" href="/oss/python/integrations/retrievers/" arrow cta="Learn more">
    A retriever is an interface that returns documents given an unstructured query.
  </Card>
</Columns>

## RAG Architectures

RAG can be implemented in multiple ways, depending on your system's needs. We outline each type in the sections below.

| Architecture    | Description                                                                | Control   | Flexibility | Latency    | Example Use Case                                  |
| --------------- | -------------------------------------------------------------------------- | --------- | ----------- | ---------- | ------------------------------------------------- |
| **2-Step RAG**  | Retrieval always happens before generation. Simple and predictable         | ✅ High    | ❌ Low       | ⚡ Fast     | FAQs, documentation bots                          |
| **Agentic RAG** | An LLM-powered agent decides *when* and *how* to retrieve during reasoning | ❌ Low     | ✅ High      | ⏳ Variable | Research assistants with access to multiple tools |
| **Hybrid**      | Combines characteristics of both approaches with validation steps          | ⚖️ Medium | ⚖️ Medium   | ⏳ Variable | Domain-specific Q\&A with quality validation      |

<Info>
  **Latency**: Latency is generally more **predictable** in **2-Step RAG**, as the maximum number of LLM calls is known and capped. This predictability assumes that LLM inference time is the dominant factor. However, real-world latency may also be affected by the performance of retrieval steps—such as API response times, network delays, or database queries—which can vary based on the tools and infrastructure in use.
</Info>

### 2-step RAG

In **2-Step RAG**, the retrieval step is always executed before the generation step. This architecture is straightforward and predictable, making it suitable for many applications where the retrieval of relevant documents is a clear prerequisite for generating an answer.
```

Example 2 (unknown):
```unknown
<Card title="Tutorial: Retrieval-Augmented Generation (RAG)" icon="robot" href="/oss/python/langchain/rag#rag-chains" arrow cta="Learn more">
  See how to build a Q\&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation.
  This tutorial walks through two approaches:

  * A **RAG agent** that runs searches with a flexible tool—great for general-purpose use.
  * A **2-step RAG** chain that requires just one LLM call per query—fast and efficient for simpler tasks.
</Card>

### Agentic RAG

**Agentic Retrieval-Augmented Generation (RAG)** combines the strengths of Retrieval-Augmented Generation with agent-based reasoning. Instead of retrieving documents before answering, an agent (powered by an LLM) reasons step-by-step and decides **when** and **how** to retrieve information during the interaction.

<Tip>
  The only thing an agent needs to enable RAG behavior is access to one or more **tools** that can fetch external knowledge — such as documentation loaders, web APIs, or database queries.
</Tip>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
<Expandable title="Extended example: Agentic RAG for LangGraph's llms.txt">
  This example implements an **Agentic RAG system** to assist users in querying LangGraph documentation. The agent begins by loading [llms.txt](https://llmstxt.org/), which lists available documentation URLs, and can then dynamically use a `fetch_documentation` tool to retrieve and process the relevant content based on the user’s question.
```

---

## Store persists embeddings to the local filesystem

**URL:** llms-txt#store-persists-embeddings-to-the-local-filesystem

---

## This can be retrieved in a retrieval step

**URL:** llms-txt#this-can-be-retrieved-in-a-retrieval-step

context = "During this morning's meeting, we solved all world conflict."

messages = [
    {"role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context."},
    {"role": "user", "content": f"Question: {question}\nContext: {context}"}
]

---

## To ensure this, we'll create vectorstore indexes for all of the artists, tracks and albums

**URL:** llms-txt#to-ensure-this,-we'll-create-vectorstore-indexes-for-all-of-the-artists,-tracks-and-albums

---

## Trace a RAG application tutorial

**URL:** llms-txt#trace-a-rag-application-tutorial

**Contents:**
- Prototyping
  - Set up your environment
  - Trace your LLM calls
  - Trace the whole chain
- Beta Testing
  - Collecting Feedback
  - Logging Metadata
- Production
  - Monitoring
  - A/B Testing

Source: https://docs.langchain.com/langsmith/observability-llm-tutorial

In this tutorial, we'll build a simple RAG application using the OpenAI SDK. We'll add observability to the application at each stage of development, from prototyping to production.

Having observability set up from the start can help you iterate **much** more quickly than you would otherwise be able to. It allows you to have great visibility into your application as you are rapidly iterating on the prompt, or changing the data and models you are using. In this section we'll walk through how to set up observability so you can have maximal observability as you are prototyping.

### Set up your environment

First, create an API key by navigating to the [settings page](https://smith.langchain.com/settings).

Next, install the LangSmith SDK:

Finally, set up the appropriate environment variables. This will log traces to the `default` project (though you can easily change that).

<Note>
  You may see these variables referenced as `LANGCHAIN_*` in other places. These are all equivalent, however the best practice is to use `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`.

The `LANGSMITH_PROJECT` flag is only supported in JS SDK versions >= 0.2.16, use `LANGCHAIN_PROJECT` instead if you are using an older version.
</Note>

### Trace your LLM calls

The first thing you might want to trace is all your OpenAI calls. After all, this is where the LLM is actually being called, so it is the most important part! We've tried to make this as easy as possible with LangSmith by introducing a dead-simple OpenAI wrapper. All you have to do is modify your code to look something like:

Notice how we import `from langsmith.wrappers import wrap_openai` and use it to wrap the OpenAI client (`openai_client = wrap_openai(OpenAI())`).

What happens if you call it in the following way?

This will produce a trace of just the OpenAI call - it should look something like [this](https://smith.langchain.com/public/e7b7d256-10fe-4d49-a8d5-36ca8e5af0d2/r)

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-openai.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=8b3ad3b0d00851bce313311efa4e8bbb" alt="Tracing tutorial openai" data-og-width="1027" width="1027" data-og-height="615" height="615" data-path="langsmith/images/tracing-tutorial-openai.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-openai.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=c4ee9e306124a884702a7c0f5685e279 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-openai.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=995ebe3b7342ea797887a052f962919d 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-openai.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=24e6e8b84336197d23ed294d4d37c842 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-openai.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=822b72e7b0ea10a96cc05eeeefad7b51 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-openai.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=985061817d26e8f76b50d2638b34ecb7 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-openai.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=bf5bb01fa39af440f985666c39809cc5 2500w" />

### Trace the whole chain

Great - we've traced the LLM call. But it's often very informative to trace more than that. LangSmith is **built** for tracing the entire LLM pipeline - so let's do that! We can do this by modifying the code to now look something like this:

Notice how we import `from langsmith import traceable` and use it decorate the overall function (`@traceable`).

What happens if you call it in the following way?

This will produce a trace of the entire RAG pipeline - it should look something like [this](https://smith.langchain.com/public/8cafba6a-1a6d-4a73-8565-483186f31c29/r)

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-chain.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=00afea1ffa117b90159d30a53aac5a7f" alt="Tracing tutorial chain" data-og-width="1016" width="1016" data-og-height="635" height="635" data-path="langsmith/images/tracing-tutorial-chain.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-chain.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=01eb0588af8534c636796b1ffc673a14 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-chain.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=38625d3b2d93cd41b344bc2610272ff4 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-chain.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=f713b97cfd693fec7ea51d85d06c1358 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-chain.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=039262907891da16b2a13d69ce3650ac 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-chain.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=97e50a697c1ac249ca91a38c42beaaa9 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-chain.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=871e76f1794d7c3d0d7fc3bb875fd613 2500w" />

The next stage of LLM application development is beta testing your application. This is when you release it to a few initial users. Having good observability set up here is crucial as often you don't know exactly how users will actually use your application, so this allows you get insights into how they do so. This also means that you probably want to make some changes to your tracing set up to better allow for that. This extends the observability you set up in the previous section

### Collecting Feedback

A huge part of having good observability during beta testing is collecting feedback. What feedback you collect is often application specific - but at the very least a simple thumbs up/down is a good start. After logging that feedback, you need to be able to easily associate it with the run that caused that. Luckily LangSmith makes it easy to do that.

First, you need to log the feedback from your app. An easy way to do this is to keep track of a run ID for each run, and then use that to log feedback. Keeping track of the run ID would look something like:

Associating feedback with that run would look something like:

Once the feedback is logged, you can then see it associated with each run by clicking into the `Metadata` tab when inspecting the run. It should look something like [this](https://smith.langchain.com/public/8cafba6a-1a6d-4a73-8565-483186f31c29/r)

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-feedback.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=cb81a556fe40895ebb29d4428d4c62d9" alt="Tracing tutorial feedback" data-og-width="1025" width="1025" data-og-height="345" height="345" data-path="langsmith/images/tracing-tutorial-feedback.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-feedback.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=165c08ee4c4f96f9f3ebb6e8183dc539 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-feedback.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=f50e70bda816d314ac233430fe5703be 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-feedback.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=579ca04b25401fd98dbd1109e55f4a8c 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-feedback.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9763f2b2f5cbb347f796e2c1951102cf 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-feedback.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=8c84bd91d25dbb0514385aabf8b2dbc2 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-feedback.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=b9f44b64e395eb392e9a6a0348189e84 2500w" />

You can also query for all runs with positive (or negative) feedback by using the filtering logic in the runs table. You can do this by creating a filter like the following:

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-filtering.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=57ebc19f2e5443c21353064c082971bc" alt="Tracing tutorial filtering" data-og-width="940" width="940" data-og-height="496" height="496" data-path="langsmith/images/tracing-tutorial-filtering.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-filtering.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=630d2ed8d85794026cbf07fcc186f791 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-filtering.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9bc6f8a5464f3c0bbdcf172ecb3e1f67 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-filtering.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9daf8b6d1ecbc23112dba100a77bc0a6 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-filtering.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=fa18baf671267ec4a1bfce3cfdc1c789 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-filtering.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=b3184ab4bfe8361d1d52b4e63c054e58 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-filtering.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=2e1aeade5945fe20527a58c1966b5a10 2500w" />

It is also a good idea to start logging metadata. This allows you to start keep track of different attributes of your app. This is important in allowing you to know what version or variant of your app was used to produce a given result.

For this example, we will log the LLM used. Oftentimes you may be experimenting with different LLMs, so having that information as metadata can be useful for filtering. In order to do that, we can add it as such:

Notice we added `@traceable(metadata={"llm": "gpt-4o-mini"})` to the `rag` function.

Keeping track of metadata in this way assumes that it is known ahead of time. This is fine for LLM types, but less desirable for other types of information - like a User ID. In order to log information that, we can pass it in at run time with the run ID.

Now that we've logged these two pieces of metadata, we should be able to see them both show up in the UI [here](https://smith.langchain.com/public/37adf7e5-97aa-42d0-9850-99c0199bddf6/r).

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=db49738eba3e0ce26514df3c9b72f87c" alt="Tracing tutorial metadata" data-og-width="1016" width="1016" data-og-height="337" height="337" data-path="langsmith/images/tracing-tutorial-metadata.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=c9f46f9e36cc47a6b10cc37870e17ffc 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=dba6e396adec67b74df789cfd9cd2491 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e31ff00027f6c5741935cec40d997697 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=cf82f0eca41b0fb04ae181e38ae47ece 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=fd57501d821496d68d5921e3cb8ce457 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=568f6fb60e84333f677775817dbc79e8 2500w" />

We can filter for these pieces of information by constructing a filter like the following:

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata-filtering.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=3662dfc2d8fb2c274f622e3f67e14b34" alt="Tracing tutorial metadata filtering" data-og-width="932" width="932" data-og-height="436" height="436" data-path="langsmith/images/tracing-tutorial-metadata-filtering.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata-filtering.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=561f6c48361533d9ddcfc005136ff6c3 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata-filtering.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=1ea92820bc977b16368e89d923a631f5 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata-filtering.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=137d1faa53ec75e8aaecf3aa2da32378 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata-filtering.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=f9c7902430dbae7b10543bd9b747a5fc 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata-filtering.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=1494db66f66fceba483829a249a44a31 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-metadata-filtering.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=06c2f159f5ce8bf601640a8484be187f 2500w" />

Great - you've used this newfound observability to iterate quickly and gain confidence that your app is performing well. Time to ship it to production! What new observability do you need to add?

First of all, let's note that the same observability you've already added will keep on providing value in production. You will continue to be able to drill down into particular runs.

In production you likely have a LOT more traffic. So you don't really want to be stuck looking at datapoints one at a time. Luckily, LangSmith has a set of tools to help with observability in production.

If you click on the `Monitor` tab in a project, you will see a series of monitoring charts. Here we track lots of LLM specific statistics - number of traces, feedback, time-to-first-token, etc. You can view these over time across a few different time bins.

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=74f49882d9e6323e2ed467b525b81b9a" alt="Tracing tutorial monitor" data-og-width="946" width="946" data-og-height="746" height="746" data-path="langsmith/images/tracing-tutorial-monitor.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=d99a10225425733cc18b1da00c04ff27 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=88a2737937bfa46e5d44f665a757fb68 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=5825a3a92fc134fe8fb8f8f4a7b46e55 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=848482d02d40236a1911a9623c39a2f0 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=278ba4c130e01f1042d49069093a7285 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=dcef7cc8a6be73d02b2030f2bb9dc783 2500w" />

<Note>
  Group-by functionality for A/B testing requires at least 2 different values to exist for a given metadata key.
</Note>

You can also use this tab to perform a version of A/B Testing. In the previous tutorial we starting tracking a few different metadata attributes - one of which was `llm`. We can group the monitoring charts by ANY metadata attribute, and instantly get grouped charts over time. This allows us to experiment with different LLMs (or prompts, or other) and track their performance over time.

In order to do this, we just need to click on the `Metadata` button at the top. This will give us a drop down of options to choose from to group by:

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-metadata.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=dc91e44dac01fcb3966c7b57b1f41d66" alt="Tracing tutorial monitor metadata" data-og-width="957" width="957" data-og-height="534" height="534" data-path="langsmith/images/tracing-tutorial-monitor-metadata.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-metadata.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=8ddc7be16e3b0f6e09e83af55fbe917f 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-metadata.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=cbc8c4287707ff477695f12d9220c55f 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-metadata.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=70345f5ed014329e07046681734f412f 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-metadata.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=73662cff14eebb9498e295834e6b8c86 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-metadata.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=7a5e5124ffbc658a5a97d372f41b96c0 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-metadata.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=24dcb9a46ea8684c2fedd0b3f136d8a0 2500w" />

Once we select this, we will start to see charts grouped by this attribute:

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-grouped.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=a1bf8fb453d7721d85bca20fbd7cb431" alt="Tracing tutorial monitor grouped" data-og-width="973" width="973" data-og-height="621" height="621" data-path="langsmith/images/tracing-tutorial-monitor-grouped.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-grouped.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=896d99b5a7456e10d92aa58c8d3bb6d8 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-grouped.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=6cc318a5f30ed0e8e11accf1d6f7428d 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-grouped.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=892af43a1ce178ec34ed4124a7a0f5d4 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-grouped.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=7be53f1392b471c45b7d14febe0df6f9 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-grouped.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=61d68a5703c7e69fe4c96df6a861ab37 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/tracing-tutorial-monitor-grouped.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=e0a3af90e154e85c45f3de1cb0a908d5 2500w" />

One of the awesome abilities that LangSmith provides is the ability to easily drilldown into datapoints that you identify as problematic while looking at monitoring charts. In order to do this, you can simply hover over a datapoint in the monitoring chart. When you do this, you will be able to click the datapoint. This will lead you back to the runs table with a filtered view:

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-monitor-drilldown.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=1ca02e0473f1fdfff102f2ccba371828" alt="Tracing tutorial monitor drilldown" data-og-width="952" width="952" data-og-height="708" height="708" data-path="langsmith/images/tracing-tutorial-monitor-drilldown.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-monitor-drilldown.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=ddf0256ff1e85656a8339e16a652480d 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-monitor-drilldown.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=0fe248ccc799c0cef9e661c861e81605 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-monitor-drilldown.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=4c3f95dd9e31e1884f569bbf736b852c 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-monitor-drilldown.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=8ce416eec3bdc7b4289ba9fbedf6959a 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-monitor-drilldown.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=a2f93d8d48a5cf33f2f4b664c72644a7 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tracing-tutorial-monitor-drilldown.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=506f485087e2e7ab91e7a53c44fd8205 2500w" />

In this tutorial you saw how to set up your LLM application with best-in-class observability. No matter what stage your application is in, you will still benefit from observability.

If you have more in-depth questions about observability, check out the [how-to section](/langsmith/observability-concepts) for guides on topics like testing, prompt management, and more.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/observability-llm-tutorial.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
</CodeGroup>

## Prototyping

Having observability set up from the start can help you iterate **much** more quickly than you would otherwise be able to. It allows you to have great visibility into your application as you are rapidly iterating on the prompt, or changing the data and models you are using. In this section we'll walk through how to set up observability so you can have maximal observability as you are prototyping.

### Set up your environment

First, create an API key by navigating to the [settings page](https://smith.langchain.com/settings).

Next, install the LangSmith SDK:

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

Finally, set up the appropriate environment variables. This will log traces to the `default` project (though you can easily change that).
```

---
