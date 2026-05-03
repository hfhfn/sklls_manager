# Langchain - Getting Started

**Pages:** 15

---

## Agent Builder setup

**URL:** llms-txt#agent-builder-setup

**Contents:**
- How to add workspace secrets
- Required model key
- Agent Builder specific secrets
- Optional tool keys
- MCP server configuration

Source: https://docs.langchain.com/langsmith/agent-builder-setup

Add required workspace secrets for models and tools used by Agent Builder.

This page lists the workspace secrets you need to add before using Agent Builder. Add these in your LangSmith workspace settings under Secrets. Keep values scoped to your workspace and avoid placing credentials in prompts or code.

## How to add workspace secrets

In the [LangSmith UI](https://smith.langchain.com), ensure that you have an LLM API key set as a [workspace secret](/langsmith/administration-overview#workspace-secrets) (either Anthropic or OpenAI API key).

1. Navigate to <Icon icon="gear" /> **Settings** and then move to the **Secrets** tab.
2. Select **Add secret** and enter either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` as the **name**, and your API key as the **value**.
3. Select **Save secret**.

<Note> When adding workspace secrets in the LangSmith UI, make sure the secret keys match the environment variable names expected by your model provider.</Note>

## Required model key

For Agent Builder to make API calls to LLMs, you need to set an OpenAI or Anthropic API key as a workspace secret. The agent graphs load this key from workspace secrets for inference.

<Note icon="wand-magic-sparkles" iconType="regular">
  Agent Builder supports custom models per agent. See [Custom models](/langsmith/agent-builder-essentials#custom-models) for more information.
</Note>

## Agent Builder specific secrets

Secrets prefixed with `AGENT_BUILDER_` are prioritized over workspace secrets within Agent Builder. This way, you can better track the usage of Agent Builder vs other parts of LangSmith which use the same secrets.

If you have both `OPENAI_API_KEY` and `AGENT_BUILDER_OPENAI_API_KEY`, the `AGENT_BUILDER_OPENAI_API_KEY` secret will be used.

## Optional tool keys

Add keys for any tools you enable. These are read from workspace secrets at runtime.

* `EXA_API_KEY`: Required for Exa search tools (general web and LinkedIn profile search).
* `TAVILY_API_KEY`: Required for Tavily web search.
* `TWITTER_API_KEY` and `TWITTER_API_KEY_SECRET`: Required for Twitter/X read operations (app‑only bearer). Posting/media upload is not enabled.

## MCP server configuration

Agent Builder can pull tools from one or more remote [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers. Configure MCP servers and headers in your [workspace](/langsmith/administration-overview#workspaces) settings. Agent Builder automatically discovers tools and applies the configured headers when calling them.

For more details on using the remote MCP servers, refer to the the [MCP Framework](/langsmith/agent-builder-mcp-framework#using-remote-mcp-servers) page.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/agent-builder-setup.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Cloud

**URL:** llms-txt#cloud

**Contents:**
- Get started
- Cloud architecture and scalability
  - Architecture
  - Allowlisting IP addresses
  - API rate limits

Source: https://docs.langchain.com/langsmith/cloud

<Callout icon="rocket" color="#4F46E5" iconType="regular">
  If you're ready to deploy your app to Cloud, follow the [Cloud deployment quickstart](/langsmith/deployment-quickstart) or the [full setup guide](/langsmith/deploy-to-cloud). This page explains the Cloud managed architecture for reference.
</Callout>

The **Cloud** option is a fully managed model where LangChain hosts and operates all LangSmith infrastructure and services:

* **Fully managed infrastructure**: LangChain handles all infrastructure, updates, scaling, and maintenance.
* **Deploy from GitHub**: Connect your repositories and deploy with a few clicks.
* **Automated CI/CD**: Build process is handled automatically by the platform.
* **LangSmith UI**: Full access to [observability](/langsmith/observability), [evaluation](/langsmith/evaluation), [deployment management](/langsmith/deployments), and [Studio](/langsmith/studio).

|                                               | **Who manages it** | **Where it runs** |
| --------------------------------------------- | ------------------ | ----------------- |
| **LangSmith platform (UI, APIs, datastores)** | LangChain          | LangChain's cloud |
| **Your Agent Servers**                        | LangChain          | LangChain's cloud |
| **CI/CD for your apps**                       | LangChain          | LangChain's cloud |

<img src="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/langgraph-cloud-architecture.png?fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=3f0316122425895270d0ecd47b12e139" alt="Cloud deployment: LangChain hosts and manages all components including the UI, APIs, and your Agent Servers." data-og-width="1425" width="1425" data-og-height="1063" height="1063" data-path="langsmith/images/langgraph-cloud-architecture.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/langgraph-cloud-architecture.png?w=280&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=b34a10fb40ca5188dddfb6be69696c75 280w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/langgraph-cloud-architecture.png?w=560&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=d310ce86e8421878575cf4d4fa72bf78 560w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/langgraph-cloud-architecture.png?w=840&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=7cc3fcee9c36a8d1e8da4cc4abbde3b9 840w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/langgraph-cloud-architecture.png?w=1100&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=a184c950c8585e2fdb5e75ac7f0f5642 1100w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/langgraph-cloud-architecture.png?w=1650&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=cb778e4a6707b00eaf703886d32569bd 1650w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/langgraph-cloud-architecture.png?w=2500&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=00f9d9df44512dded307613502d03299 2500w" />

To deploy your first application to Cloud, follow the [Cloud deployment quickstart](/langsmith/deployment-quickstart) or refer to the [comprehensive setup guide](/langsmith/deploy-to-cloud).

## Cloud architecture and scalability

<Note>
  This section is only relevant for the cloud-managed LangSmith services available at [https://smith.langchain.com](https://smith.langchain.com) and [https://eu.smith.langchain.com](https://eu.smith.langchain.com).

For information on the self-hosted LangSmith solution, please refer to the [self-hosted documentation](/langsmith/self-hosted).
</Note>

LangSmith is deployed on Google Cloud Platform (GCP) and is designed to be highly scalable. Many customers run production workloads on LangSmith for LLM application observability, evaluation, and agent deployment

The US-based LangSmith service is deployed in the `us-central1` (Iowa) region of GCP.

<Note>
  The [EU-based LangSmith service](https://eu.smith.langchain.com) is now available (as of mid-July 2024) and is deployed in the `europe-west4` (Netherlands) region of GCP. If you are interested in an enterprise plan in this region, [contact our sales team](https://www.langchain.com/contact-sales).
</Note>

#### Regional storage

The resources and services in this table are stored in the location corresponding to the URL where sign-up occurred (either the US or EU). Cloud-managed LangSmith uses [Supabase](https://supabase.com) for authentication/authorization and [ClickHouse Cloud](https://clickhouse.com/cloud) for data warehouse.

|                                                | US                                                                 | EU                                                                       |
| ---------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| URL                                            | [https://smith.langchain.com](https://smith.langchain.com)         | [https://eu.smith.langchain.com](https://eu.smith.langchain.com)         |
| API URL                                        | [https://api.smith.langchain.com](https://api.smith.langchain.com) | [https://eu.api.smith.langchain.com](https://eu.api.smith.langchain.com) |
| GCP                                            | us-central1 (Iowa)                                                 | europe-west4 (Netherlands)                                               |
| Supabase                                       | AWS us-east-1 (N. Virginia)                                        | AWS eu-central-1 (Germany)                                               |
| ClickHouse Cloud                               | us-central1 (Iowa)                                                 | europe-west4 (Netherlands)                                               |
| [LangSmith deployment](/langsmith/deployments) | us-central1 (Iowa)                                                 | europe-west4 (Netherlands)                                               |

See the [Regions FAQ](/langsmith/regions-faq) for more information.

#### Region-independent storage

Data listed here is stored exclusively in the US:

* Payment and billing information with Stripe and Metronome

LangSmith is composed of the following services, all deployed on Google Kubernetes Engine (GKE):

* LangSmith Frontend: serves the LangSmith UI.
* LangSmith Backend: serves the LangSmith API.
* LangSmith Platform Backend: handles authentication and other high-volume tasks. (Internal service)
* LangSmith Playground: handles forwarding requests to various LLM providers for the Playground feature.
* LangSmith Queue: handles processing of asynchronous tasks. (Internal service)

LangSmith uses the following GCP storage services:

* Google Cloud Storage (GCS) for runs inputs and outputs.
* Google Cloud SQL PostgreSQL for transactional workloads.
* Google Cloud Memorystore for Redis for queuing and caching.
* Clickhouse Cloud on GCP for trace ingestion and analytics. Our services connect to Clickhouse Cloud, which is hosted in the same GCP region, via a private endpoint.

Some additional GCP services we use include:

* Google Cloud Load Balancer for routing traffic to the LangSmith services.
* Google Cloud CDN for caching static assets.
* Google Cloud Armor for security and rate limits. For more information on rate limits we enforce, please refer to [this guide](/langsmith/administration-overview#rate-limits).

<div style={{ textAlign: 'center' }}>
  <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=0790cbdf4fe131c74d1e60bb120834e3" alt="Light mode overview" data-og-width="2210" width="2210" data-og-height="1463" height="1463" data-path="langsmith/images/cloud-arch-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=280&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=c04d8a044d221559fe2f7b9121275638 280w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=560&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=a15351b254f11cc149ce237ba8853e91 560w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=840&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=d4a409e73830e588519cb1d0b2a17f3b 840w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=1100&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=6dbeda77b57083efb988e15af38f0a6e 1100w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=1650&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=24aadbe2e79db02d76fd5deaea6564e1 1650w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=2500&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=a126aa1f02d36de0a8e391f0e1059b8e 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=767f3bc3dc73ffe1a806f54e0aaa428b" alt="Dark mode overview" data-og-width="2210" width="2210" data-og-height="1463" height="1463" data-path="langsmith/images/cloud-arch-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=280&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=f7367df5b782c821882605418c50563f 280w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=560&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=60759ef9e927ba0985e21e38acacae6d 560w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=840&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=383ac38ba52733548d8d97ffabfe384e 840w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=1100&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=b045b8e19a9926d4d10ec8ad2d2767c1 1100w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=1650&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=23778aa891c1b42336b274ab1b2f8bec 1650w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=2500&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=5a64734b4e9fb5dd4af690edf3fa6248 2500w" />
</div>

### Allowlisting IP addresses

#### Egress from LangChain SaaS

All traffic leaving LangSmith services will be routed through a NAT gateway. All traffic will appear to originate from the following IP addresses:

| US             | EU             |
| -------------- | -------------- |
| 34.59.65.97    | 34.13.192.67   |
| 34.67.51.221   | 34.147.105.64  |
| 34.46.212.37   | 34.90.22.166   |
| 34.132.150.88  | 34.147.36.213  |
| 35.188.222.201 | 34.32.137.113  |
| 34.58.194.127  | 34.91.238.184  |
| 34.59.97.173   | 35.204.101.241 |
| 104.198.162.55 | 35.204.48.32   |

It may be helpful to allowlist these IP addresses if connecting to your own AzureOpenAI service or other endpoints that may be required by the Playground or Online Evaluation.

#### Ingress into LangChain SaaS

The langchain endpoints map to the following static IP addresses:

| US             | EU           |
| -------------- | ------------ |
| 34.8.121.39    | 34.95.92.214 |
| 34.107.251.234 | 34.13.73.122 |

You may need to allowlist these to enable traffic from your private network to LangSmith SaaS endpoints (`api.smith.langchain.com`, `smith.langchain.com`, `beacon.langchain.com`, `eu.api.smith.langchain.com`, `eu.smith.langchain.com`, `eu.beacon.langchain.com`).

LangSmith enforces rate limits on API endpoints to ensure service stability and fair usage. The following table shows the rate limits for different endpoints in both US and EU regions. Note that:

* Rate limits are expressed as `count / interval` where count is the number of requests allowed within the interval (in seconds). For example, `2000 / 10` means 2000 requests per 10 seconds.
* When no HTTP method is specified in the endpoint column, the rate limit applies to all HTTP methods for that endpoint.
* When a specific method is listed (e.g., `POST`, `GET`), the rate limit applies only to that method.

| Match / Endpoint (method)                   | Identity key     | US prod limit | EU prod limit | Category                                     |
| ------------------------------------------- | ---------------- | ------------- | ------------- | -------------------------------------------- |
| OPTIONS, `/info`, `*/v1/metadata/submit`    | IP               | 2000 / 10     | 2000 / 10     | [High throughput](#rate-limit-categories)    |
| `/auth`                                     | `x-api-key`      | 2000 / 10     | 2000 / 10     | [High throughput](#rate-limit-categories)    |
| `/auth`                                     | `x-user-id` + IP | 2000 / 10     | 2000 / 10     | [High throughput](#rate-limit-categories)    |
| `/v1/beacon`                                | IP               | 2000 / 10     | 2000 / 10     | [High throughput](#rate-limit-categories)    |
| `/repos`                                    | `x-api-key`      | 100 / 60      | 100 / 60      | [Repository](#rate-limit-categories)         |
| `/repos`                                    | `x-user-id` + IP | 100 / 60      | 100 / 60      | [Repository](#rate-limit-categories)         |
| `POST /runs/batch`                          | `x-api-key`      | 2000 / 10     | 2000 / 10     | [High throughput](#rate-limit-categories)    |
| `POST /otel/v1/traces`                      | `x-api-key`      | 2000 / 10     | 2000 / 10     | [Run ingest](#rate-limit-categories)         |
| `POST` containing `/charts`                 | `x-api-key`      | 750 / 600     | 750 / 600     | [Charts](#rate-limit-categories)             |
| `POST` containing `/charts`                 | `x-user-id` + IP | 750 / 600     | 750 / 600     | [Charts](#rate-limit-categories)             |
| `POST /runs/multipart`                      | `x-api-key`      | 6000 / 10     | 6000 / 10     | [Multipart ingest](#rate-limit-categories)   |
| `POST /runs/query`                          | `x-api-key`      | 15 / 10       | 15 / 10       | [Run query (API)](#rate-limit-categories)    |
| `POST /runs/query`                          | `x-user-id` + IP | 300 / 10      | 300 / 10      | [Run query (User)](#rate-limit-categories)   |
| `/generate`                                 | `x-api-key`      | 30 / 3600     | 30 / 3600     | [Generation](#rate-limit-categories)         |
| `/generate`                                 | `x-user-id` + IP | 30 / 3600     | 30 / 3600     | [Generation](#rate-limit-categories)         |
| `/commits`                                  | `x-api-key`      | 10000 / 60    | 2000 / 60     | [Commits](#rate-limit-categories)            |
| `/commits`                                  | `x-user-id` + IP | 10000 / 60    | 2000 / 60     | [Commits](#rate-limit-categories)            |
| `DELETE /sessions` or `*/trigger`           | `x-api-key`      | 10 / 60       | 10 / 60       | [Deletion](#rate-limit-categories)           |
| `DELETE /sessions` or `*/trigger`           | `x-user-id` + IP | 30 / 60       | 30 / 60       | [Deletion](#rate-limit-categories)           |
| `POST /runs` (single run ingest)            | `x-api-key`      | 2000 / 10     | 2000 / 10     | [Run ingest](#rate-limit-categories)         |
| `PATCH` containing `/runs`                  | `x-api-key`      | 2000 / 10     | 2000 / 10     | [Run ingest](#rate-limit-categories)         |
| `POST /feedback`                            | `x-api-key`      | 2000 / 10     | 2000 / 10     | [High throughput](#rate-limit-categories)    |
| `GET /runs/{uuid}` or `/api/v1/runs/{uuid}` | `x-api-key`      | 30 / 60       | 30 / 60       | [Run lookup](#rate-limit-categories)         |
| `GET` containing `/examples`                | `x-api-key`      | 5000 / 60     | 5000 / 60     | [Examples](#rate-limit-categories)           |
| Any request with `x-api-key`                | `x-api-key`      | 1000 / 10     | 1000 / 10     | [Default (API key)](#rate-limit-categories)  |
| Any request with `x-user-id`                | `x-user-id` + IP | 1000 / 10     | 1000 / 10     | [Default (User)](#rate-limit-categories)     |
| `/public/download`                          | IP               | 5000 / 60     | 5000 / 60     | [Public download](#rate-limit-categories)    |
| `/runs/stats`                               | `x-api-key`      | 1 / 10        | 20 / 10       | [Stats](#rate-limit-categories)              |
| All other IPs (catch-all)                   | IP               | 100 / 60      | 100 / 60      | [Public (catch-all)](#rate-limit-categories) |

#### Rate limit categories

* **High throughput**: General high-volume endpoints for core operations like authentication, metadata, and feedback.
* **Repository**: Repository and prompt management operations.
* **Run ingest**: Individual trace/run ingestion endpoints for observability.
* **Charts**: Chart generation and visualization endpoints.
* **Multipart ingest**: Bulk run ingestion via multipart upload for high-volume tracing.
* **Run query (API)**: API key-based run query operations with stricter limits for complex queries.
* **Run query (User)**: User-based run query operations with higher limits for interactive use.
* **Generation**: AI-powered code and content generation endpoints (limited to prevent abuse).
* **Commits**: Prompt versioning and commit operations.
* **Deletion**: Session deletion and workflow trigger operations.
* **Run lookup**: Retrieving specific runs by UUID.
* **Examples**: Fetching dataset examples for few-shot prompting.
* **Default (API key)**: Fallback rate limit for authenticated API requests not matching specific patterns.
* **Default (User)**: Fallback rate limit for authenticated user requests not matching specific patterns.
* **Public download**: High-volume public download endpoints for shared resources.
* **Stats**: Run statistics and analytics endpoints (region-specific limits apply).
* **Public (catch-all)**: Default rate limit for unauthenticated public access.

For more information on rate limits and other service limits, refer to the [Administration overview](/langsmith/administration-overview#rate-limits).

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/cloud.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Create an Ingress for installations (Kubernetes)

**URL:** llms-txt#create-an-ingress-for-installations-(kubernetes)

**Contents:**
- Requirements
- Parameters
- Configuration
  - Option 1: Standard Ingress
  - Option 2: Gateway API
  - Option 3: Istio Gateway

Source: https://docs.langchain.com/langsmith/self-host-ingress

By default, LangSmith will provision a LoadBalancer service for the `langsmith-frontend`. Depending on your cloud provider, this may result in a public IP address being assigned to the service. If you would like to use a custom domain or have more control over the routing of traffic to your LangSmith installation, you can configure an Ingress, Gateway API, or Istio Gateway.

* An existing Kubernetes cluster
* One of the following installed in your Kubernetes cluster:
  * An Ingress Controller (for standard Ingress)
  * Gateway API CRDs and a Gateway resource (for Gateway API)
  * Istio (for Istio Gateway)

You may need to provide certain parameters to your LangSmith installation to configure the Ingress. Additionally, we will want to convert the `langsmith-frontend` service to a ClusterIP service.

* *Hostname (optional)*: The hostname that you would like to use for your LangSmith installation. E.g `"langsmith.example.com"`. If you leave this empty, the ingress will serve all traffic to the LangSmith installation.

* *BasePath (optional)*: If you would like to serve LangSmith under a URL basePath, you can specify it here. For example, adding `"langsmith"` will serve the application at `"example.hostname.com/langsmith"`. This will apply to UI paths as well as API endpoints.

* *IngressClassName (optional)*: The name of the Ingress class that you would like to use. If not set, the default Ingress class will be used.

* *Annotations (optional)*: Additional annotations to add to the Ingress. Certain providers like AWS may use annotations to control things like TLS termination.

For example, you can add the following annotations using the AWS ALB Ingress Controller to attach an ACM certificate to the Ingress:

* *Labels (optional)*: Additional labels to add to the Ingress.

* *TLS (optional)*: If you would like to serve LangSmith over HTTPS, you can add TLS configuration here (many Ingress controllers may have other ways of controlling TLS so this is often not needed). This should be an array of TLS configurations. Each TLS configuration should have the following fields:

* hosts: An array of hosts that the certificate should be valid for. E.g \["langsmith.example.com"]

* secretName: The name of the Kubernetes secret that contains the certificate and private key. This secret should have the following keys:

* tls.crt: The certificate
    * tls.key: The private key

* You can read more about creating a TLS secret [here](https://kubernetes.io/do/langsmith/observability-concepts/services-networking/ingress/#tls).

You can configure your LangSmith instance to use one of three routing options: standard Ingress, Gateway API, or Istio Gateway. Choose the option that best fits your infrastructure.

### Option 1: Standard Ingress

With these parameters in hand, you can configure your LangSmith instance to use an Ingress. You can do this by modifying the `config.yaml` file for your LangSmith Helm Chart installation.

Once configured, you will need to update your LangSmith installation. If everything is configured correctly, your LangSmith instance should now be accessible via the Ingress. You can run the following to check the status of your Ingress:

You should see something like this in the output:

<Warning>
  If you do not have automated DNS setup, you will need to add the IP address to your DNS provider manually.
</Warning>

### Option 2: Gateway API

<Note>
  Gateway API support is available as of LangSmith v0.12.0
</Note>

If your cluster uses the [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/), you can configure LangSmith to provision HTTPRoute resources. This will create an HTTPRoute for LangSmith and an HTTPRoute for each [agent deployment](/langsmith/deployments).

* *name (required)*: The name of the Gateway resource to reference
* *namespace (required)*: The namespace where the Gateway resource is located
* *hostname (optional)*: The hostname that you would like to use for your LangSmith installation. E.g `"langsmith.example.com"`
* *basePath (optional)*: If you would like to serve LangSmith under a base path, you can specify it here. E.g "example.com/langsmith"
* *sectionName (optional)*: The name of a specific listener section in the Gateway to use
* *annotations (optional)*: Additional annotations to add to the HTTPRoute resources
* *labels (optional)*: Additional labels to add to the HTTPRoute resources

Once configured, you can check the status of your HTTPRoutes:

### Option 3: Istio Gateway

<Note>
  Istio Gateway support is available as of LangSmith v0.12.0
</Note>

If your cluster uses [Istio](https://istio.io/), you can configure LangSmith to provision VirtualService resources. This will create a VirtualService for LangSmith and a VirtualService for each [agent deployment](/langsmith/deployments).

* *name (optional)*: The name of the Istio Gateway resource to reference. Defaults to `"istio-gateway"`
* *namespace (optional)*: The namespace where the Istio Gateway resource is located. Defaults to `"istio-system"`
* *hostname (optional)*: The hostname that you would like to use for your LangSmith installation. E.g `"langsmith.example.com"`
* *basePath (optional)*: If you would like to serve LangSmith under a base path, you can specify it here. E.g "example.com/langsmith"
* *annotations (optional)*: Additional annotations to add to the VirtualService resources
* *labels (optional)*: Additional labels to add to the VirtualService resources

Once configured, you can check the status of your VirtualServices:

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/self-host-ingress.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
* *Labels (optional)*: Additional labels to add to the Ingress.

* *TLS (optional)*: If you would like to serve LangSmith over HTTPS, you can add TLS configuration here (many Ingress controllers may have other ways of controlling TLS so this is often not needed). This should be an array of TLS configurations. Each TLS configuration should have the following fields:

  * hosts: An array of hosts that the certificate should be valid for. E.g \["langsmith.example.com"]

  * secretName: The name of the Kubernetes secret that contains the certificate and private key. This secret should have the following keys:

    * tls.crt: The certificate
    * tls.key: The private key

  * You can read more about creating a TLS secret [here](https://kubernetes.io/do/langsmith/observability-concepts/services-networking/ingress/#tls).

## Configuration

You can configure your LangSmith instance to use one of three routing options: standard Ingress, Gateway API, or Istio Gateway. Choose the option that best fits your infrastructure.

### Option 1: Standard Ingress

With these parameters in hand, you can configure your LangSmith instance to use an Ingress. You can do this by modifying the `config.yaml` file for your LangSmith Helm Chart installation.
```

Example 2 (unknown):
```unknown
Once configured, you will need to update your LangSmith installation. If everything is configured correctly, your LangSmith instance should now be accessible via the Ingress. You can run the following to check the status of your Ingress:
```

Example 3 (unknown):
```unknown
You should see something like this in the output:
```

Example 4 (unknown):
```unknown
<Warning>
  If you do not have automated DNS setup, you will need to add the IP address to your DNS provider manually.
</Warning>

### Option 2: Gateway API

<Note>
  Gateway API support is available as of LangSmith v0.12.0
</Note>

If your cluster uses the [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/), you can configure LangSmith to provision HTTPRoute resources. This will create an HTTPRoute for LangSmith and an HTTPRoute for each [agent deployment](/langsmith/deployments).

#### Parameters

* *name (required)*: The name of the Gateway resource to reference
* *namespace (required)*: The namespace where the Gateway resource is located
* *hostname (optional)*: The hostname that you would like to use for your LangSmith installation. E.g `"langsmith.example.com"`
* *basePath (optional)*: If you would like to serve LangSmith under a base path, you can specify it here. E.g "example.com/langsmith"
* *sectionName (optional)*: The name of a specific listener section in the Gateway to use
* *annotations (optional)*: Additional annotations to add to the HTTPRoute resources
* *labels (optional)*: Additional labels to add to the HTTPRoute resources

#### Configuration
```

---

## Deploy on Cloud

**URL:** llms-txt#deploy-on-cloud

**Contents:**
- Prerequisites
- Create new deployment
- Create new revision
- View build and server logs
- View deployment metrics
- Interrupt revision
- Delete deployment
- Deployment settings
- Add or remove GitHub repositories
- Allowlist IP addresses

Source: https://docs.langchain.com/langsmith/deploy-to-cloud

This is the comprehensive setup and management guide for deploying applications to LangSmith Cloud.

<Callout icon="zap" color="#4F46E5" iconType="regular">
  **If you're looking for a quick setup**, try the [quickstart guide](/langsmith/deployment-quickstart) first.
</Callout>

Before setting up, review the [Cloud overview page](/langsmith/cloud) to understand the Cloud hosting model.

* Applications are deployed from GitHub repositories. Configure and upload an application to a GitHub repository.
* [Verify that the LangGraph API runs locally](/langsmith/local-server). If the API does not run successfully (i.e., `langgraph dev`), deploying to LangSmith will fail as well.

<Note>
  **One-Time Setup Required**: A GitHub organization owner or admin must complete the OAuth flow in the LangSmith UI to authorize the `hosted-langserve` GitHub app. This only needs to be done once per workspace. After the initial OAuth authorization, all developers with deployment permissions can create and manage deployments without requiring GitHub admin access.
</Note>

## Create new deployment

Starting from the [LangSmith UI](https://smith.langchain.com), select **Deployments** in the left-hand navigation panel, **Deployments**. In the top-right corner, select **+ New Deployment** to create a new deployment:

1. In the **Create New Deployment** panel, fill out the required fields. For **Deployment details**:
   1. Select **Import from GitHub** and follow the GitHub OAuth workflow to install and authorize LangChain's `hosted-langserve` GitHub app to access the selected repositories. After installation is complete, return to the **Create New Deployment** panel and select the GitHub repository to deploy from the dropdown menu.
      <Note> The GitHub user installing LangChain's `hosted-langserve` GitHub app must be an [owner](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization#organization-owners) of the organization or account. This authorization only needs to be completed once per LangSmith workspace—subsequent deployments can be created by any user with deployment permissions.</Note>
   2. Specify a name for the deployment.
   3. Specify the desired **Git Branch**. A deployment is linked to a branch. When a new revision is created, code for the linked branch will be deployed. The branch can be updated later in the [Deployment Settings](#deployment-settings).
   4. Specify the full path to the [LangGraph API config file](/langsmith/cli#configuration-file) including the file name. For example, if the file `langgraph.json` is in the root of the repository, specify `langgraph.json`.
   5. Use the checkbox to **Automatically update deployment on push to branch**. If checked, the deployment will automatically be updated when changes are pushed to the specified **Git Branch**. You can enable or disable this setting on the [Deployment Settings](#deployment-settings) in [the UI](https://smith.langchain.com).
      For **Deployment Type**:
      * Development deployments are meant for non-production use cases and are provisioned with minimal resources.
      * Production deployments can serve up to 500 requests/second and are provisioned with highly available storage with automatic backups.
   6. Determine if the deployment should be **Shareable through Studio**.
      1. If unchecked, the deployment will only be accessible with a valid LangSmith API key for the [workspace](/langsmith/administration-overview#workspaces).
      2. If checked, the deployment will be accessible through [Studio](/langsmith/studio) to any LangSmith user. A direct URL to Studio for the deployment will be provided to share with other LangSmith users.
   7. Specify **Environment Variables** and secrets. To configure additional variables for the deployment, refer to the [Environment Variables reference](/langsmith/env-var).
      1. Sensitive values such as API keys (e.g., `OPENAI_API_KEY`) should be specified as secrets.
      2. Additional non-secret environment variables can be specified as well.
   8. A new LangSmith [tracing project](/langsmith/observability) is automatically created with the same name as the deployment.
2. In the top-right corner, select **Submit**. After a few seconds, the **Deployment** view appears and the new deployment will be queued for provisioning.

## Create new revision

When [creating a new deployment](#create-new-deployment), a new revision is created by default. You can create subsequent revisions to deploy new code changes.

Starting from the [LangSmith UI](https://smith.langchain.com), select **Deployments** in the left-hand navigation panel. Select an existing deployment to create a new revision for.

1. In the **Deployment** view, in the top-right corner, select **+ New Revision**.
2. In the **New Revision** modal, fill out the required fields.
   1. Specify the full path to the [API config file](/langsmith/cli#configuration-file) including the file name. For example, if the file `langgraph.json` is in the root of the repository, specify `langgraph.json`.
   2. Determine if the deployment should be **Shareable through Studio**.
      * If unchecked, the deployment will only be accessible with a valid LangSmith API key for the [workspace](/langsmith/administration-overview#workspaces).
      * If checked, the deployment will be accessible through [Studio](/langsmith/studio) to any LangSmith user. A direct URL to Studio for the deployment will be provided to share with other LangSmith users.
   3. Specify **Environment Variables** and secrets. Existing secrets and environment variables are prepopulated. To configure additional variables for the revision, refer to the [Environment Variables reference](/langsmith/env-var).
      1. Add new secrets or environment variables.
      2. Remove existing secrets or environment variables.
      3. Update the value of existing secrets or environment variables.
3. Select **Submit\`**. After a few seconds, the **New Revision** modal will close and the new revision will be queued for deployment.

## View build and server logs

Build and server logs are available for each revision.

Starting from the **Deployments** view:

1. Select the desired revision from the **Revisions** table. A panel slides open from the right-hand side and the **Build** tab is selected by default, which displays build logs for the revision.
2. In the panel, select the **Server** tab to view server logs for the revision. Server logs are only available after a revision has been deployed.
3. Within the **Server** tab, adjust the date/time range picker as needed. By default, the date/time range picker is set to the **Last 7 days**.

## View deployment metrics

Starting from the [LangSmith UI](https://smith.langchain.com):

1. In the left-hand navigation panel, select **Deployments**.
2. Select an existing deployment to monitor.
3. Select the **Monitoring** tab to view the deployment metrics. Refer to a list of [all available metrics](/langsmith/control-plane#monitoring).
4. Within the **Monitoring** tab, use the date/time range picker as needed. By default, the date/time range picker is set to the **Last 15 minutes**.

## Interrupt revision

Interrupting a revision will stop deployment of the revision.

<Warning>
  **Undefined Behavior**
  Interrupted revisions have undefined behavior. This is only useful if you need to deploy a new revision and you already have a revision "stuck" in progress. In the future, this feature may be removed.
</Warning>

Starting from the **Deployments** view:

1. Select the menu icon (three dots) on the right-hand side of the row for the desired revision from the **Revisions** table.
2. Select **Interrupt** from the menu.
3. A modal will appear. Review the confirmation message. Select **Interrupt revision**.

Starting from the [LangSmith UI](https://smith.langchain.com):

1. In the left-hand navigation panel, select **Deployments**, which contains a list of existing deployments.
2. Select the menu icon (three dots) on the right-hand side of the row for the desired deployment and select **Delete**.
3. A **Confirmation** modal will appear. Select **Delete**.

## Deployment settings

Starting from the **Deployments** view:

1. In the top-right corner, select the gear icon (**Deployment Settings**).
2. Update the `Git Branch` to the desired branch.
3. Check/uncheck checkbox to **Automatically update deployment on push to branch**.
   1. Branch creation/deletion and tag creation/deletion events will not trigger an update. Only pushes to an existing branch will trigger an update.
   2. Pushes in quick succession to a branch will queue subsequent updates. Once a build completes, the most recent commit will begin building and the other queued builds will be skipped.

## Add or remove GitHub repositories

After installing and authorizing LangChain's `hosted-langserve` GitHub app, repository access for the app can be modified to add new repositories or remove existing repositories. If a new repository is created, it may need to be added explicitly.

1. From the GitHub profile, navigate to **Settings** > **Applications** > `hosted-langserve` > click **Configure**.
2. Under **Repository access**, select **All repositories** or **Only select repositories**. If **Only select repositories** is selected, new repositories must be explicitly added.
3. Click **Save**.
4. When creating a new deployment, the list of GitHub repositories in the dropdown menu will be updated to reflect the repository access changes.

## Allowlist IP addresses

All traffic from LangSmith deployments created after January 6th 2025 will come through a NAT gateway.
This NAT gateway will have several static ip addresses depending on the region you are deploying in. Refer to the table below for the list of IP addresses to allowlist:

| US             | EU             |
| -------------- | -------------- |
| 35.197.29.146  | 34.90.213.236  |
| 34.145.102.123 | 34.13.244.114  |
| 34.169.45.153  | 34.32.180.189  |
| 34.82.222.17   | 34.34.69.108   |
| 35.227.171.135 | 34.32.145.240  |
| 34.169.88.30   | 34.90.157.44   |
| 34.19.93.202   | 34.141.242.180 |
| 34.19.34.50    | 34.32.141.108  |
| 34.59.244.194  |                |
| 34.9.99.224    |                |
| 34.68.27.146   |                |
| 34.41.178.137  |                |
| 34.123.151.210 |                |
| 34.135.61.140  |                |
| 34.121.166.52  |                |
| 34.31.121.70   |                |

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/deploy-to-cloud.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Deploy your app to Cloud

**URL:** llms-txt#deploy-your-app-to-cloud

**Contents:**
- Prerequisites
- 1. Create a repository on GitHub
- 2. Deploy to LangSmith
- 3. Test your application in Studio
- 4. Get the API URL for your deployment
- 5. Test the API
- Next steps

Source: https://docs.langchain.com/langsmith/deployment-quickstart

This is a quickstart guide for deploying your first application to LangSmith Cloud.

<Tip>
  For a comprehensive Cloud deployment guide with all configuration options, refer to the [Cloud deployment setup guide](/langsmith/deploy-to-cloud).
</Tip>

Before you begin, ensure you have the following:

* A [GitHub account](https://github.com/)
* A [LangSmith account](https://smith.langchain.com/) (free to sign up)

## 1. Create a repository on GitHub

To deploy an application to **LangSmith**, your application code must reside in a GitHub repository. Both public and private repositories are supported. For this quickstart, use the [`new-langgraph-project` template](https://github.com/langchain-ai/react-agent) for your application:

1. Go to the [`new-langgraph-project` repository](https://github.com/langchain-ai/new-langgraph-project) or [`new-langgraphjs-project` template](https://github.com/langchain-ai/new-langgraphjs-project).
2. Click the `Fork` button in the top right corner to fork the repository to your GitHub account.
3. Click **Create fork**.

## 2. Deploy to LangSmith

1. Log in to [LangSmith](https://smith.langchain.com/).
2. In the left sidebar, select **Deployments**.
3. Click the **+ New Deployment** button. A pane will open where you can fill in the required fields.
4. If you are a first time user or adding a private repository that has not been previously connected, click the **Import from GitHub** button and follow the instructions to connect your GitHub account.
5. Select your New LangGraph Project repository.
6. Click **Submit** to deploy.
   This may take about 15 minutes to complete. You can check the status in the **Deployment details** view.

## 3. Test your application in Studio

Once your application is deployed:

1. Select the deployment you just created to view more details.
2. Click the **Studio** button in the top right corner. [Studio](/langsmith/studio) will open to display your graph.

## 4. Get the API URL for your deployment

1. In the **Deployment details** view, click the **API URL** to copy it to your clipboard.
2. Click the `URL` to copy it to the clipboard.

You can now test the API:

<Tabs>
  <Tab title="Python SDK (Async)">
    1. Install the LangGraph Python SDK:

2. Send a message to the assistant (threadless run):

<Tab title="Python SDK (Sync)">
    1. Install the LangGraph Python SDK:

2. Send a message to the assistant (threadless run):

<Tab title="JavaScript SDK">
    1. Install the LangGraph JS SDK

2. Send a message to the assistant (threadless run):

<Tab title="Rest API">
    
  </Tab>
</Tabs>

You've successfully deployed your application to LangSmith Cloud. Here are some next steps:

* **Explore Studio**: Use [Studio](/langsmith/studio) to visualize and debug your graph interactively.
* **Monitor your app**: Set up [observability](/langsmith/observability) with traces, dashboards, and alerts.
* **Learn more about Cloud**: See the [complete Cloud setup guide](/langsmith/deploy-to-cloud) for all configuration options.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/deployment-quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
2. Send a message to the assistant (threadless run):
```

Example 2 (unknown):
```unknown
</Tab>

  <Tab title="Python SDK (Sync)">
    1. Install the LangGraph Python SDK:
```

Example 3 (unknown):
```unknown
2. Send a message to the assistant (threadless run):
```

Example 4 (unknown):
```unknown
</Tab>

  <Tab title="JavaScript SDK">
    1. Install the LangGraph JS SDK
```

---

## Evaluation quickstart

**URL:** llms-txt#evaluation-quickstart

**Contents:**
- Prerequisites
- Video guide

Source: https://docs.langchain.com/langsmith/evaluation-quickstart

[*Evaluations*](/langsmith/evaluation-concepts) are a quantitative way to measure the performance of LLM applications. LLMs can behave unpredictably, even small changes to prompts, models, or inputs can significantly affect results. Evaluations provide a structured way to identify failures, compare versions, and build more reliable AI applications.

Running an evaluation in LangSmith requires three key components:

* [*Dataset*](/langsmith/evaluation-concepts#datasets): A set of test inputs (and optionally, expected outputs).
* [*Target function*](/langsmith/define-target-function): The part of your application you want to test—this might be a single LLM call with a new prompt, one module, or your entire workflow.
* [*Evaluators*](/langsmith/evaluation-concepts#evaluators): Functions that score your target function’s outputs.

This quickstart guides you through running a starter evaluation that checks the correctness of LLM responses, using either the LangSmith SDK or UI.

<Tip>
  If you prefer to watch a video on getting started with tracing, refer to the datasets and evaluations [Video guide](#video-guide).
</Tip>

Before you begin, make sure you have:

* **A LangSmith account**: Sign up or log in at [smith.langchain.com](https://smith.langchain.com).
* **A LangSmith API key**: Follow the [Create an API key](/langsmith/create-account-api-key#create-an-api-key) guide.
* **An OpenAI API key**: Generate this from the [OpenAI dashboard](https://platform.openai.com/account/api-keys).

**Select the UI or SDK filter for instructions:**

<Tabs>
  <Tab title="UI" icon="window">
    ## 1. Set workspace secrets

In the [LangSmith UI](https://smith.langchain.com), ensure that your OpenAI API key is set as a [workspace secret](/langsmith/administration-overview#workspace-secrets).

1. Navigate to <Icon icon="gear" /> **Settings** and then move to the **Secrets** tab.
    2. Select **Add secret** and enter the `OPENAI_API_KEY` and your API key as the **Value**.
    3. Select **Save secret**.

<Note> When adding workspace secrets in the LangSmith UI, make sure the secret keys match the environment variable names expected by your model provider.</Note>

## 2. Create a prompt

LangSmith's [Prompt Playground](/langsmith/observability-concepts#prompt-playground) makes it possible to run evaluations over different prompts, new models, or test different model configurations.

1. In the [LangSmith UI](https://smith.langchain.com), navigate to the **Playground** under **Prompt Engineering**.
    2. Under the **Prompts** panel, modify the **system** prompt to:

Leave the **Human** message as is: `{question}`.

## 3. Create a dataset

1. Click **Set up Evaluation**, which will open a **New Experiment** table at the bottom of the page.

2. In the **Select or create a new dataset** dropdown, click the **+ New** button to create a new dataset.

<div style={{ textAlign: 'center' }}>
         <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-light.png?fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=b068f4407a83e31403da9a5473960fee" alt="Playground with the edited system prompt and new experiment with the dropdown for creating a new dataset." data-og-width="1422" width="1422" data-og-height="743" height="743" data-path="langsmith/images/playground-system-prompt-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-light.png?w=280&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=d43b9466988d5077d0d2efe44b80b578 280w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-light.png?w=560&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=1bf60ab2d71b1b9e734c28694f7974bc 560w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-light.png?w=840&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=131d3d7bdc6c16e7738d3ea50fbc3abf 840w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-light.png?w=1100&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=5396dc8c14902762a7499cf9dced6907 1100w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-light.png?w=1650&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=b5eb2c32e461f50e7c85672cb5646f80 1650w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-light.png?w=2500&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=db0ceb217623931ff1084e86b5d50981 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-dark.png?fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=a114b1a83bf8d0a074b4ce2759207e4d" alt="Playground with the edited system prompt and new experiment with the dropdown for creating a new dataset." data-og-width="1421" width="1421" data-og-height="736" height="736" data-path="langsmith/images/playground-system-prompt-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-dark.png?w=280&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=b88848b64b77bf1e2e997b956bbdd171 280w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-dark.png?w=560&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=c036a354ec2e314d50426814028106d4 560w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-dark.png?w=840&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=69fd6ef5aebac86623c203592a6038ae 840w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-dark.png?w=1100&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=89ddb65e1ee37a1901e1f653ecd917ed 1100w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-dark.png?w=1650&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=d8ec3af511ae661b55c9bcb79a18726f 1650w, https://mintcdn.com/langchain-5e9cc07a/hVPHwyb3hetqtQnG/langsmith/images/playground-system-prompt-dark.png?w=2500&fit=max&auto=format&n=hVPHwyb3hetqtQnG&q=85&s=824698630c1325a8082df4b8923492a9 2500w" />
       </div>

3. Add the following examples to the dataset:

| Inputs                                                   | Reference Outputs                                 |
       | -------------------------------------------------------- | ------------------------------------------------- |
       | question: Which country is Mount Kilimanjaro located in? | output: Mount Kilimanjaro is located in Tanzania. |
       | question: What is Earth's lowest point?                  | output: Earth's lowest point is The Dead Sea.     |

4. Click **Save** and enter a name to save your newly created dataset.

## 4. Add an evaluator

1. Click **+ Evaluator** and select **Correctness** from the **Pre-built Evaluator** options.
    2. In the **Correctness** panel, click **Save**.

## 5. Run your evaluation

1. Select <Icon icon="circle-play" /> **Start** on the top right to run your evaluation. This will create an [*experiment*](/langsmith/evaluation-concepts#experiment) with a preview in the **New Experiment** table. You can view in full by clicking the experiment name.

<div style={{ textAlign: 'center' }}>
         <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-light.png?fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=efa004b4032d0e439a58d08567b75478" alt="Full experiment view of the results that used the example dataset." data-og-width="1241" width="1241" data-og-height="671" height="671" data-path="langsmith/images/full-experiment-view-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-light.png?w=280&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=6d76d0e8d11cfdab4ac142f2d5c4bde1 280w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-light.png?w=560&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=b712e5a37af115a401d8d0d34812ef93 560w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-light.png?w=840&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=30c491438801b77eb4377401f26fd65d 840w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-light.png?w=1100&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=dc75651029fb4a83549714b41f06f541 1100w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-light.png?w=1650&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=7f3ade3f66b44d7080284112502a5812 1650w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-light.png?w=2500&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=e084175b15d368419c77835fbad3b53e 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-dark.png?fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=34c2921eeadd1b7782ac64b579bcef6a" alt="Full experiment view of the results that used the example dataset." data-og-width="1241" width="1241" data-og-height="665" height="665" data-path="langsmith/images/full-experiment-view-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-dark.png?w=280&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=e02feba8a82d493bf55c6801368b5c9b 280w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-dark.png?w=560&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=5f184bcab87fa6a55a948a54aa393a14 560w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-dark.png?w=840&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=c0bc9d71281293065f696cf85632179b 840w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-dark.png?w=1100&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=f8715bb40e847ad482fa1b5ff573ae2e 1100w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-dark.png?w=1650&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=5da023adf8b5bc693335baae7159169b 1650w, https://mintcdn.com/langchain-5e9cc07a/3SZlGm2zGXjJWzA5/langsmith/images/full-experiment-view-dark.png?w=2500&fit=max&auto=format&n=3SZlGm2zGXjJWzA5&q=85&s=64a53655134ae7554edaf47b1a957d26 2500w" />
       </div>

<Tip>
      To learn more about running experiments in LangSmith, read the [evaluation conceptual guide](/langsmith/evaluation-concepts).
    </Tip>

* For more details on evaluations, refer to the [Evaluation documentation](/langsmith/evaluation).
    * Learn how to [create and manage datasets in the UI](/langsmith/manage-datasets-in-application#set-up-your-dataset).
    * Learn how to [run an evaluation from the prompt playground](/langsmith/run-evaluation-from-prompt-playground).
  </Tab>

<Tab title="SDK" icon="code">
    <Tip>
      This guide uses prebuilt LLM-as-judge evaluators from the open-source [`openevals`](https://github.com/langchain-ai/openevals) package. OpenEvals includes a set of commonly used evaluators and is a great starting point if you're new to evaluations. If you want greater flexibility in how you evaluate your apps, you can also [define completely custom evaluators](/langsmith/code-evaluator).
    </Tip>

## 1. Install dependencies

In your terminal, create a directory for your project and install the dependencies in your environment:

<Info>
      If you are using `yarn` as your package manager, you will also need to manually install `@langchain/core` as a peer dependency of `openevals`. This is not required for LangSmith evals in general, you may define evaluators [using arbitrary custom code](/langsmith/code-evaluator).
    </Info>

## 2. Set up environment variables

Set the following environment variables:

* `LANGSMITH_TRACING`
    * `LANGSMITH_API_KEY`
    * `OPENAI_API_KEY` (or your LLM provider's API key)
    * (optional) `LANGSMITH_WORKSPACE_ID`: If your LangSmith API key is linked to multiple [workspaces](/langsmith/administration-overview#workspaces), set this variable to specify which workspace to use.

<Note>
      If you're using Anthropic, use the [Anthropic wrapper](/langsmith/annotate-code#wrap-the-anthropic-client-python-only) to trace your calls. For other providers, use [the traceable wrapper](/langsmith/annotate-code#use-%40traceable-%2F-traceable).
    </Note>

## 3. Create a dataset

1. Create a file and add the following code, which will:

* Import the `Client` to connect to LangSmith.
       * Create a dataset.
       * Define example [*inputs* and *outputs*](/langsmith/evaluation-concepts#examples).
       * Associate the input and output pairs with that dataset in LangSmith so they can be used in evaluations.

2. In your terminal, run the `dataset` file to create the datasets you'll use to evaluate your app:

You'll see the following output:

## 4. Create your target function

Define a [target function](/langsmith/define-target-function) that contains what you're evaluating. In this guide, you'll define a target function that contains a single LLM call to answer a question.

Add the following to an `eval` file:

## 5. Define an evaluator

In this step, you’re telling LangSmith how to grade the answers your app produces.

Import a prebuilt evaluation prompt (`CORRECTNESS_PROMPT`) from [`openevals`](https://github.com/langchain-ai/openevals) and a helper that wraps it into an [*LLM-as-judge evaluator*](/langsmith/evaluation-concepts#llm-as-judge), which will score the application's output.

<Info>
      `CORRECTNESS_PROMPT` is just an f-string with variables for `"inputs"`, `"outputs"`, and `"reference_outputs"`. See [here](https://github.com/langchain-ai/openevals#customizing-prompts) for more information on customizing OpenEvals prompts.
    </Info>

The evaluator compares:

* `inputs`: what was passed into your target function (e.g., the question text).
    * `outputs`: what your target function returned (e.g., the model’s answer).
    * `reference_outputs`: the ground truth answers you attached to each dataset example in [Step 3](#3-create-a-dataset).

Add the following highlighted code to your `eval` file:

## 6. Run and view results

To run the evaluation experiment, you'll call `evaluate(...)`, which:

* Pulls example from the dataset you created in [Step 3](#3-create-a-dataset).
    * Sends each example's inputs to your target function from [Step 4](#4-add-an-evaluator).
    * Collects the outputs (the model's answers).
    * Passes the outputs along with the `reference_outputs` to your evaluator from [Step 5](#5-define-an-evaluator).
    * Records all results in LangSmith as an experiment, so you can view them in the UI.

1. Add the highlighted code to your `eval` file:

2. Run your evaluator:

3. You'll receive a link to view the evaluation results and metadata for the experiment results:

4. Follow the link in the output of your evaluation run to access the **Datasets & Experiments** page in the [LangSmith UI](https://smith.langchain.com), and explore the results of the experiment. This will direct you to the created experiment with a table showing the **Inputs**, **Reference Output**, and **Outputs**. You can select a dataset to open an expanded view of the results.

<div style={{ textAlign: 'center' }}>
         <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-light.png?fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=94341c15219e46866589140d87efb8f6" alt="Experiment results in the UI after following the link." data-og-width="1816" width="1816" data-og-height="464" height="464" data-path="langsmith/images/experiment-results-link-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-light.png?w=280&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=a21a3329260ad62c96f334cda7956fe9 280w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-light.png?w=560&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=a35065f0c34ec47116cf07320d15feee 560w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-light.png?w=840&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=4f505f7b711829c9948e07aea7199869 840w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-light.png?w=1100&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=cc258bf607ab9c601e6770e35b03d6ca 1100w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-light.png?w=1650&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=dde47e9fa8c00e81776c32df132e1191 1650w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-light.png?w=2500&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=2f690dfd90d40401f5fa0cfabe08d070 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-dark.png?fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=d741b33219f7d130e80e1dfb7e743ac6" alt="Experiment results in the UI after following the link." data-og-width="1567" width="1567" data-og-height="455" height="455" data-path="langsmith/images/experiment-results-link-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-dark.png?w=280&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=49cc262a4941e5af43659dc1351e9ade 280w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-dark.png?w=560&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=177c8f916e53cb2d7396e7f10352eb50 560w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-dark.png?w=840&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=801e51a8002dac8add3ed14796b989bc 840w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-dark.png?w=1100&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=feab9e0fb21a720a8aefa80e4b6aedca 1100w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-dark.png?w=1650&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=0bf74f76e36d30e9520504281dd6b2ff 1650w, https://mintcdn.com/langchain-5e9cc07a/DDMvkseOvrCjx9sx/langsmith/images/experiment-results-link-dark.png?w=2500&fit=max&auto=format&n=DDMvkseOvrCjx9sx&q=85&s=84dd1248a09df55b3bd872276ef7c3ad 2500w" />
       </div>

Here are some topics you might want to explore next:

* [Evaluation concepts](/langsmith/evaluation-concepts) provides descriptions of the key terminology for evaluations in LangSmith.
    * [OpenEvals README](https://github.com/langchain-ai/openevals) to see all available prebuilt evaluators and how to customize them.
    * [Define custom evaluators](/langsmith/code-evaluator).
    * [Python](https://docs.smith.langchain.com/reference/python/reference) or [TypeScript](https://docs.smith.langchain.com/reference/js) SDK references for comprehensive descriptions of every class and function.
  </Tab>
</Tabs>

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/iEgjJyk3aTw?si=C7BPKXPmdE1yAflv" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/evaluation-quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
Answer the following question accurately:
```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown
</CodeGroup>

    <Info>
      If you are using `yarn` as your package manager, you will also need to manually install `@langchain/core` as a peer dependency of `openevals`. This is not required for LangSmith evals in general, you may define evaluators [using arbitrary custom code](/langsmith/code-evaluator).
    </Info>

    ## 2. Set up environment variables

    Set the following environment variables:

    * `LANGSMITH_TRACING`
    * `LANGSMITH_API_KEY`
    * `OPENAI_API_KEY` (or your LLM provider's API key)
    * (optional) `LANGSMITH_WORKSPACE_ID`: If your LangSmith API key is linked to multiple [workspaces](/langsmith/administration-overview#workspaces), set this variable to specify which workspace to use.
```

Example 4 (unknown):
```unknown
<Note>
      If you're using Anthropic, use the [Anthropic wrapper](/langsmith/annotate-code#wrap-the-anthropic-client-python-only) to trace your calls. For other providers, use [the traceable wrapper](/langsmith/annotate-code#use-%40traceable-%2F-traceable).
    </Note>

    ## 3. Create a dataset

    1. Create a file and add the following code, which will:

       * Import the `Client` to connect to LangSmith.
       * Create a dataset.
       * Define example [*inputs* and *outputs*](/langsmith/evaluation-concepts#examples).
       * Associate the input and output pairs with that dataset in LangSmith so they can be used in evaluations.

       <CodeGroup>
```

---

## Mirror images for your LangSmith installation

**URL:** llms-txt#mirror-images-for-your-langsmith-installation

**Contents:**
- Requirements
- Mirroring the Images

Source: https://docs.langchain.com/langsmith/self-host-mirroring-images

By default, LangSmith will pull images from our public Docker registry. However, if you are running LangSmith in an environment that does not have internet access, or if you would like to use a private Docker registry, you can mirror the images to your own registry and then configure your LangSmith installation to use those images.

* Authenticated access to a Docker registry that your Kubernetes cluster/machine has access to.
* Docker installed on your local machine or a machine that has access to the Docker registry.
* A Kubernetes cluster or a machine where you can run LangSmith.

## Mirroring the Images

For your convenience, we have provided a script that will mirror the images for you. You can find the script in the [LangSmith Helm Chart repository](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/mirror_langsmith_images.sh)

To use the script, you will need to run the script with the following command specifying your registry and platform:

Where `<your-registry>` is the URL of your Docker registry (e.g. `myregistry.com`) and `<platform>` is the platform you are using (e.g. `linux/amd64`, `linux/arm64`, etc.). If you do not specify a platform, it will default to `linux/amd64`.

For example, if your registry is `myregistry.com`, your platform is `linux/arm64`, and you want to use the latest version of the images, you would run:

Note that this script will assume that you have Docker installed and that you are authenticated to your registry. It will also push the images to the specified registry with the same repository/tag as the original images.

Alternatively, you can pull, mirror, and push the images manually. The images that you will need to mirror are found in the `values.yaml` file of the LangSmith Helm Chart. These can be found here: [LangSmith Helm Chart values.yaml](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml#L14)

Here is an example of how to mirror the images using Docker:

```bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
Where `<your-registry>` is the URL of your Docker registry (e.g. `myregistry.com`) and `<platform>` is the platform you are using (e.g. `linux/amd64`, `linux/arm64`, etc.). If you do not specify a platform, it will default to `linux/amd64`.

For example, if your registry is `myregistry.com`, your platform is `linux/arm64`, and you want to use the latest version of the images, you would run:
```

Example 2 (unknown):
```unknown
Note that this script will assume that you have Docker installed and that you are authenticated to your registry. It will also push the images to the specified registry with the same repository/tag as the original images.

Alternatively, you can pull, mirror, and push the images manually. The images that you will need to mirror are found in the `values.yaml` file of the LangSmith Helm Chart. These can be found here: [LangSmith Helm Chart values.yaml](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml#L14)

Here is an example of how to mirror the images using Docker:
```

---

## Prompt engineering quickstart

**URL:** llms-txt#prompt-engineering-quickstart

**Contents:**
- Prerequisites
- Next steps
- Video guide

Source: https://docs.langchain.com/langsmith/prompt-engineering-quickstart

Prompts guide the behavior of Large Language Models (LLM). [*Prompt engineering*](/langsmith/prompt-engineering-concepts) is the process of crafting, testing, and refining the instructions you give to an LLM so it produces reliable and useful responses.

LangSmith provides tools to create, version, test, and collaborate on prompts. You’ll also encounter common concepts like [*prompt templates*](/langsmith/prompt-engineering-concepts#prompts-vs-prompt-templates), which let you reuse structured prompts, and [*variables*](/langsmith/prompt-engineering-concepts#f-string-vs-mustache), which allow you to dynamically insert values (such as a user’s question) into a prompt.

In this quickstart, you’ll create, test, and improve prompts using either the UI or the SDK. This quickstart will use OpenAI as the example LLM provider, but the same workflow applies across other providers.

<Tip>
  If you prefer to watch a video on getting started with prompt engineering, refer to the quickstart [Video guide](#video-guide).
</Tip>

Before you begin, make sure you have:

* **A LangSmith account**: Sign up or log in at [smith.langchain.com](https://smith.langchain.com).
* **A LangSmith API key**: Follow the [Create an API key](/langsmith/create-account-api-key#create-an-api-key) guide.
* **An OpenAI API key**: Generate this from the [OpenAI dashboard](https://platform.openai.com/account/api-keys).

Select the tab for UI or SDK workflows:

<Tabs>
  <Tab title="UI" icon="window">
    ## 1. Set workspace secret

In the [LangSmith UI](https://smith.langchain.com), ensure that your OpenAI API key is set as a [workspace secret](/langsmith/administration-overview#workspace-secrets).

1. Navigate to <Icon icon="gear" /> **Settings** and then move to the **Secrets** tab.
    2. Select **Add secret** and enter the `OPENAI_API_KEY` and your API key as the **Value**.
    3. Select **Save secret**.

<Note> When adding workspace secrets in the LangSmith UI, make sure the secret keys match the environment variable names expected by your model provider.</Note>

## 2. Create a prompt

1. In the [LangSmith UI](https://smith.langchain.com), navigate to the **Prompts** section in the left-hand menu.
    2. Click on **+ Prompt** to create a prompt.
    3. Modify the prompt by editing or adding prompts and input variables as needed.

<div style={{ textAlign: 'center' }}>
      <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=0cafd7b1330fd88caa7403772068a50d" alt="Prompt playground with the system prompt ready for editing." data-og-width="951" width="951" data-og-height="412" height="412" data-path="langsmith/images/create-a-prompt-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=280&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=86270ac274480c09b4b772c79835c96a 280w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=560&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=0bba28323e21330632a3368603cfd436 560w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=840&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=7c6ec959c52230f4a9c1153e05c2a257 840w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=1100&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=3c76f683eb2ef9c71dc1a3d7e337fffb 1100w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=1650&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=b900411f7aa605f20f6c5182834bf4c3 1650w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=2500&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=b3b11c7507cc57b2fc178b251c0173dc 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=16f217eb0e1c0b02ad0d7658f1a53f4d" alt="Prompt playground with the system prompt ready for editing." data-og-width="937" width="937" data-og-height="402" height="402" data-path="langsmith/images/create-a-prompt-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=280&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=401ae88da122905ab2e820fc22ce1b37 280w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=560&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=61c573f773dec1485545395c1fd37525 560w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=840&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=0fd582cf184a36f1f2ce7dc21d7be9b9 840w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=1100&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=32408b98f4df25413ba0e78b85c7b483 1100w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=1650&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=102ecf375a8d66ac339b12bc163588e7 1650w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=2500&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=3543f050b1e4e0e581c4386304284039 2500w" />
    </div>

1. Under the **Prompts** heading select the gear <Icon icon="gear" iconType="solid" /> icon next to the model name, which will launch the **Prompt Settings** window on the **Model Configuration** tab.

2. Set the [model configuration](/langsmith/managing-model-configurations) you want to use. The **Provider** and **Model** you select will determine the parameters that are configurable on this configuration page. Once set, click **Save as**.

<div style={{ textAlign: 'center' }}>
         <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=6c0f7d7012b1e5295fe545149f955e6b" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="886" width="886" data-og-height="689" height="689" data-path="langsmith/images/model-config-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=280&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=4e3b9ad92f6f14f4e0523bef50199318 280w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=560&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=e538eb740495a8afa8bfc552b13ae294 560w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=840&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=ebe73264e977153c869fd04d1552d09b 840w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1100&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=2eeb01882056046bc73cc019d674af7e 1100w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1650&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=8f28fe2fe8054cf0623fb9d17f91966f 1650w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=2500&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=cf9ad39be3623e73322d123699e73f19 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=2e9da272c3fc8f7ac958c6e6d1da85e3" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="881" width="881" data-og-height="732" height="732" data-path="langsmith/images/model-config-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=280&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=652fb75a4682cfc813743a1260764e59 280w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=560&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=02c980a8387f3d69a5870660b1668080 560w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=840&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ee633c06056fa7ad46ea58a179afa169 840w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1100&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=f62a35ed726b5f89c156a40c9ea76f2c 1100w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1650&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=18114575db8e6c7ce928763ddcb88c12 1650w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=2500&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ab24dc4975def52db55c4896ead5b77c 2500w" />
       </div>

3. Specify the input variables you would like to test in the **Inputs** box and then click <Icon icon="circle-play" iconType="solid" /> **Start**.

<div style={{ textAlign: 'center' }}>
         <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=bd86e76180c022a110ca0f0d9d19a198" alt="The input box with a question entered. The output box contains the response to the prompt." data-og-width="702" width="702" data-og-height="763" height="763" data-path="langsmith/images/set-input-start-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=280&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=dc5f16c448685e182a0001b9dbcb1afd 280w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=560&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=372a5f62109cd09b57ba2ca11d73c65b 560w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=840&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=1fcd9d131af34af4b5e10ab5fea2a9f8 840w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=1100&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=f30ae237c4d2cf55918918eca39bb5e9 1100w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=1650&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=26326dd6839418f161f6393118f8c441 1650w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=2500&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=2654906d801046f11e6f96bfa7c7a59e 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=bfd369e7426a57fc0cad75df8dd6942d" alt="The input box with a question entered. The output box contains the response to the prompt." data-og-width="698" width="698" data-og-height="769" height="769" data-path="langsmith/images/set-input-start-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=280&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=9538e3e173a2f19994f08865a389f247 280w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=560&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=fc8dc91b4564531bb5a27b971ca27c3e 560w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=840&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=ae9db3c1ec55c4653ad86b95addeec12 840w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=1100&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=0f169783a075952a0066de46aeb3bdc7 1100w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=1650&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=686196a3493642cf70ff89aa235a6715 1650w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=2500&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=0532f0c8cf0ff37ed7c9da7a67bf6700 2500w" />
       </div>

To learn about more options for configuring your prompt in the Playground, refer to [Configure prompt settings](/langsmith/managing-model-configurations).

4. After testing and refining your prompt, click **Save** to store it for future use.

## 4. Iterate on a prompt

LangSmith allows for team-based prompt iteration. [Workspace](/langsmith/administration-overview#workspaces) members can experiment with prompts in the playground and save their changes as a new [*commit*](/langsmith/prompt-engineering-concepts#commits) when ready.

To improve your prompts:

* Reference the documentation provided by your model provider for best practices in prompt creation, such as:
      * [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
      * [Gemini's Introduction to prompt design](https://ai.google.dev/gemini-api/docs/prompting-intro)
    * Build and refine your prompts with the Prompt Canvas—an interactive tool in LangSmith. Learn more in the [Prompt Canvas guide](/langsmith/write-prompt-with-ai).
    * Tag specific commits to mark important moments in your commit history.

1. To create a commit, navigate to the **Playground** and select **Commit**. Choose the prompt to commit changes to and then **Commit**.
      2. Navigate to **Prompts** in the left-hand menu. Select the prompt. Once on the prompt's detail page, move to the **Commits** tab. Find the tag icon <Icon icon="tag" iconType="solid" /> to **Add a Commit Tag**.

<div style={{ textAlign: 'center' }}>
        <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=80e7b49cb4036e15369c9e417d1d63ad" alt="The tag, the commit tag box with the commit label, and the commit tag name box to create the tag." data-og-width="702" width="702" data-og-height="226" height="226" data-path="langsmith/images/add-commit-tag-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=280&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=bbed6d72fa9986d211195f7cb6e3bbc3 280w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=560&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=93623e1b7ae7b4c9826c7a76694dd43d 560w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=840&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=c9ccfe378c982af55b6781691b0c6a1b 840w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=1100&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=d9464f4655a0ba67b81916eb9e69cdbc 1100w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=1650&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=43b3ad05600b7c9e0883541acccb1cc5 1650w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=2500&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=69019a8aad0d4733333f0f69ad468171 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=80883a09fbaea8c892d0a7de88f7a6ca" alt="The tag, the commit tag box with the commit label, and the commit tag name box to create the tag." data-og-width="698" width="698" data-og-height="221" height="221" data-path="langsmith/images/add-commit-tag-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=280&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=0c7eb9c966673a410811a5a08a39cbf7 280w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=560&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=9976856ffeca88d9f8d856e0d7766613 560w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=840&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=9a79984ca88bd3fa74b512ce8b26430b 840w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=1100&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=82c269188447b9ecf9f7ff17fa9805ec 1100w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=1650&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=83e03a2d056fc81440e6f11acfa1479c 1650w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=2500&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=cc7d694fc1cc6c4a76c7dca4a9ed9dc4 2500w" />
      </div>
  </Tab>

<Tab title="SDK" icon="code">
    ## 1. Set up your environment

1. In your terminal, prepare your environment:

2. Set your API keys:

## 2. Create a prompt

To create a prompt, you'll define a list of messages that you want in your prompt and then push to LangSmith.

Use the language-specific constructor and push method:

* Python: [`ChatPromptTemplate`](https://reference.langchain.com/python/langchain_core/prompts/#langchain_core.prompts.chat.ChatPromptTemplate) → [`client.push_prompt(...)`](https://docs.smith.langchain.com/reference/python/client/langsmith.client.Client#langsmith.client.Client.push_prompt)
    * TypeScript: [`ChatPromptTemplate.fromMessages(...)`](https://v03.api.js.langchain.com/classes/_langchain_core.prompts.ChatPromptTemplate.html#fromMessages) → [`client.pushPrompt(...)`](https://langsmith-docs-7jgx2bq8f-langchain.vercel.app/reference/js/classes/client.Client#pushprompt)

1. Add the following code to a `create_prompt` file:

This creates an ordered list of messages, wraps them in `ChatPromptTemplate`, and then pushes the prompt by name to your [workspace](/langsmith/administration-overview#workspaces) for versioning and reuse.

2. Run `create_prompt`:

Follow the resulting link to view the newly created Prompt Hub prompt in the LangSmith UI.

In this step, you'll pull the prompt you created in [step 2](#2-create-a-prompt) by name (`"prompt-quickstart"`), format it with a test input, convert it to OpenAI’s chat format, and call the OpenAI Chat Completions API.

Then, you'll iterate on the prompt by creating a new version. Members of your workspace can open an existing prompt, experiment with changes in the [UI](https://smith.langchain.com), and save those changes as a new commit on the same prompt, which preserves history for the whole team.

1. Add the following to a `test_prompt` file:

This loads the prompt by name using `pull` for the latest committed version of the prompt that you're testing. You can also specify a specific commit by passing the commit hash `"<prompt-name>:<commit-hash>"`

2. Run `test_prompt` :

3. To create a new version of a prompt, call the same push method you used initially with the same prompt name and your updated template. LangSmith will record it as a new commit and preserve prior versions.

Copy the following code to an `iterate_prompt` file:

4. Run `iterate_prompt` :

Now your prompt will contain two commits.

To improve your prompts:

* Reference the documentation provided by your model provider for best practices in prompt creation, such as:
      * [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
      * [Gemini's Introduction to prompt design](https://ai.google.dev/gemini-api/docs/prompting-intro)
    * Build and refine your prompts with the Prompt Canvas—an interactive tool in LangSmith. Learn more in the [Prompt Canvas guide](/langsmith/write-prompt-with-ai).
  </Tab>
</Tabs>

* Learn more about how to store and manage prompts using the Prompt Hub in the [Create a prompt guide](/langsmith/create-a-prompt).
* Learn how to set up the Playground to [Test multi-turn conversations](/langsmith/multiple-messages) in this tutorial.
* Learn how to test your prompt's performance over a dataset instead of individual examples, refer to [Run an evaluation from the Prompt Playground](/langsmith/run-evaluation-from-prompt-playground).

<Callout type="info" icon="bird">
  Use **[Polly](/langsmith/polly)** in the Playground to help optimize your prompts, generate tools, and create output schemas.
</Callout>

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/h4f6bIWGkog?si=IVJFfhldC7M3HL4G" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/prompt-engineering-quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
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

    2. Set your API keys:
```

Example 3 (unknown):
```unknown
## 2. Create a prompt

    To create a prompt, you'll define a list of messages that you want in your prompt and then push to LangSmith.

    Use the language-specific constructor and push method:

    * Python: [`ChatPromptTemplate`](https://reference.langchain.com/python/langchain_core/prompts/#langchain_core.prompts.chat.ChatPromptTemplate) → [`client.push_prompt(...)`](https://docs.smith.langchain.com/reference/python/client/langsmith.client.Client#langsmith.client.Client.push_prompt)
    * TypeScript: [`ChatPromptTemplate.fromMessages(...)`](https://v03.api.js.langchain.com/classes/_langchain_core.prompts.ChatPromptTemplate.html#fromMessages) → [`client.pushPrompt(...)`](https://langsmith-docs-7jgx2bq8f-langchain.vercel.app/reference/js/classes/client.Client#pushprompt)

    1. Add the following code to a `create_prompt` file:

       <CodeGroup>
```

Example 4 (unknown):
```unknown

```

---

## Quickstart

**URL:** llms-txt#quickstart

Source: https://docs.langchain.com/oss/python/langgraph/quickstart

This quickstart demonstrates how to build a calculator agent using the LangGraph Graph API or the Functional API.

* [Use the Graph API](#use-the-graph-api) if you prefer to define your agent as a graph of nodes and edges.
* [Use the Functional API](#use-the-functional-api) if you prefer to define your agent as a single function.

For conceptual information, see [Graph API overview](/oss/python/langgraph/graph-api) and [Functional API overview](/oss/python/langgraph/functional-api).

<Info>
  For this example, you will need to set up a [Claude (Anthropic)](https://www.anthropic.com/) account and get an API key. Then, set the `ANTHROPIC_API_KEY` environment variable in your terminal.
</Info>

<Tabs>
  <Tab title="Use the Graph API">
    ## 1. Define tools and model

In this example, we'll use the Claude Sonnet 4.5 model and define tools for addition, multiplication, and division.

The graph's state is used to store the messages and the number of LLM calls.

<Tip>
      State in LangGraph persists throughout the agent's execution.

The `Annotated` type with `operator.add` ensures that new messages are appended to the existing list rather than replacing it.
    </Tip>

## 3. Define model node

The model node is used to call the LLM and decide whether to call a tool or not.

## 4. Define tool node

The tool node is used to call the tools and return the results.

## 5. Define end logic

The conditional edge function is used to route to the tool node or end based upon whether the LLM made a tool call.

## 6. Build and compile the agent

The agent is built using the [`StateGraph`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.StateGraph) class and compiled using the [`compile`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.StateGraph.compile) method.

<Tip>
      To learn how to trace your agent with LangSmith, see the [LangSmith documentation](/langsmith/trace-with-langgraph).
    </Tip>

Congratulations! You've built your first agent using the LangGraph Graph API.

<Accordion title="Full code example">
      
    </Accordion>
  </Tab>

<Tab title="Use the Functional API">
    ## 1. Define tools and model

In this example, we'll use the Claude Sonnet 4.5 model and define tools for addition, multiplication, and division.

## 2. Define model node

The model node is used to call the LLM and decide whether to call a tool or not.

<Tip>
      The [`@task`](https://reference.langchain.com/python/langgraph/func/#langgraph.func.task) decorator marks a function as a task that can be executed as part of the agent. Tasks can be called synchronously or asynchronously within your entrypoint function.
    </Tip>

## 3. Define tool node

The tool node is used to call the tools and return the results.

The agent is built using the [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/#langgraph.func.entrypoint) function.

<Note>
      In the Functional API, instead of defining nodes and edges explicitly, you write standard control flow logic (loops, conditionals) within a single function.
    </Note>

<Tip>
      To learn how to trace your agent with LangSmith, see the [LangSmith documentation](/langsmith/trace-with-langgraph).
    </Tip>

Congratulations! You've built your first agent using the LangGraph Functional API.

<Accordion title="Full code example" icon="code">
      
    </Accordion>
  </Tab>
</Tabs>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
## 2. Define state

    The graph's state is used to store the messages and the number of LLM calls.

    <Tip>
      State in LangGraph persists throughout the agent's execution.

      The `Annotated` type with `operator.add` ensures that new messages are appended to the existing list rather than replacing it.
    </Tip>
```

Example 2 (unknown):
```unknown
## 3. Define model node

    The model node is used to call the LLM and decide whether to call a tool or not.
```

Example 3 (unknown):
```unknown
## 4. Define tool node

    The tool node is used to call the tools and return the results.
```

Example 4 (unknown):
```unknown
## 5. Define end logic

    The conditional edge function is used to route to the tool node or end based upon whether the LLM made a tool call.
```

---

## Setup claude_agent_sdk with langsmith tracing

**URL:** llms-txt#setup-claude_agent_sdk-with-langsmith-tracing

configure_claude_agent_sdk()

@tool(
    "get_weather",
    "Gets the current weather for a given city",
    {
        "city": str,
    },
)
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    """Simulated weather lookup tool"""
    city = args["city"]

# Simulated weather data
    weather_data = {
        "San Francisco": "Foggy, 62°F",
        "New York": "Sunny, 75°F",
        "London": "Rainy, 55°F",
        "Tokyo": "Clear, 68°F",
    }

weather = weather_data.get(city, "Weather data not available")
    return {"content": [{"type": "text", "text": f"Weather in {city}: {weather}"}]}

async def main():
    # Create SDK MCP server with the weather tool
    weather_server = create_sdk_mcp_server(
        name="weather",
        version="1.0.0",
        tools=[get_weather],
    )

options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        system_prompt="You are a friendly travel assistant who helps with weather information.",
        mcp_servers={"weather": weather_server},
        allowed_tools=["mcp__weather__get_weather"],
    )

async with ClaudeSDKClient(options=options) as client:
        await client.query("What's the weather like in San Francisco and Tokyo?")

async for message in client.receive_response():
            print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

Once configured, all Claude Agent SDK operations will be automatically traced to LangSmith, including:

* Agent queries and responses
* Tool invocations and results
* Claude model interactions
* MCP server operations

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/trace-claude-agent-sdk.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Setup recording directory

**URL:** llms-txt#setup-recording-directory

recordings_dir = Path(__file__).parent / "recordings"
recordings_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
recording_path = recordings_dir / f"conversation_{timestamp}.wav"

---

## Tracing quickstart

**URL:** llms-txt#tracing-quickstart

**Contents:**
- Prerequisites
- 1. Create a directory and install dependencies
- 2. Set up environment variables
- 3. Define your application
- 4. Trace LLM calls
- 5. Trace an entire application
- Next steps
- Video guide

Source: https://docs.langchain.com/langsmith/observability-quickstart

[*Observability*](/langsmith/observability-concepts) is a critical requirement for applications built with Large Language Models (LLMs). LLMs are non-deterministic, which means that the same prompt can produce different responses. This behavior makes debugging and monitoring more challenging than with traditional software.

LangSmith addresses this by providing end-to-end visibility into how your application handles a request. Each request generates a [*trace*](/langsmith/observability-concepts#traces), which captures the full record of what happened. Within a trace are individual [*runs*](/langsmith/observability-concepts#runs), the specific operations your application performed, such as an LLM call or a retrieval step. Tracing runs allows you to inspect, debug, and validate your application’s behavior.

In this quickstart, you will set up a minimal [*Retrieval Augmented Generation (RAG)*](https://www.mckinsey.com/featured-insights/mckinsey-explainers/what-is-retrieval-augmented-generation-rag) application and add tracing with LangSmith. You will:

1. Configure your environment.
2. Create an application that retrieves context and calls an LLM.
3. Enable tracing to capture both the retrieval step and the LLM call.
4. View the resulting traces in the LangSmith UI.

<Tip>
  If you prefer to watch a video on getting started with tracing, refer to the quickstart [Video guide](#video-guide).
</Tip>

Before you begin, make sure you have:

* **A LangSmith account**: Sign up or log in at [smith.langchain.com](https://smith.langchain.com).
* **A LangSmith API key**: Follow the [Create an API key](/langsmith/create-account-api-key#create-an-api-key) guide.
* **An OpenAI API key**: Generate this from the [OpenAI dashboard](https://platform.openai.com/account/api-keys).

The example app in this quickstart will use OpenAI as the LLM provider. You can adapt the example for your app's LLM provider.

<Tip>
  If you're building an application with [LangChain](https://python.langchain.com/docs/introduction/) or [LangGraph](https://langchain-ai.github.io/langgraph/), you can enable LangSmith tracing with a single environment variable. Get started by reading the guides for tracing with [LangChain](/langsmith/trace-with-langchain) or tracing with [LangGraph](/langsmith/trace-with-langgraph).
</Tip>

## 1. Create a directory and install dependencies

In your terminal, create a directory for your project and install the dependencies in your environment:

## 2. Set up environment variables

Set the following environment variables:

* `LANGSMITH_TRACING`
* `LANGSMITH_API_KEY`
* `OPENAI_API_KEY` (or your LLM provider's API key)
* (optional) `LANGSMITH_WORKSPACE_ID`: If your LangSmith API key is linked to multiple workspaces, set this variable to specify which workspace to use.

If you're using Anthropic, use the [Anthropic wrapper](/langsmith/annotate-code#wrap-the-anthropic-client-python-only) to trace your calls. For other providers, use [the traceable wrapper](/langsmith/annotate-code#use-%40traceable-%2F-traceable).

## 3. Define your application

You can use the example app code outlined in this step to instrument a RAG application. Or, you can use your own application code that includes an LLM call.

This is a minimal RAG app that uses the OpenAI SDK directly without any LangSmith tracing added yet. It has three main parts:

* **Retriever function**: Simulates document retrieval that always returns the same string.
* **OpenAI client**: Instantiates a plain OpenAI client to send a chat completion request.
* **RAG function**: Combines the retrieved documents with the user’s question to form a system prompt, calls the `chat.completions.create()` endpoint with `gpt-4o-mini`, and returns the assistant’s response.

Add the following code into your app file (e.g., `app.py` or `app.ts`):

## 4. Trace LLM calls

To start, you’ll trace all your OpenAI calls. LangSmith provides wrappers:

* Python: [`wrap_openai`](https://docs.smith.langchain.com/reference/python/wrappers/langsmith.wrappers._openai.wrap_openai)
* TypeScript: [`wrapOpenAI`](https://docs.smith.langchain.com/reference/js/functions/wrappers_openai.wrapOpenAI)

This snippet wraps the OpenAI client so that every subsequent model call is logged automatically as a traced child run in LangSmith.

1. Include the highlighted lines in your app file:

2. Call your application:

You'll receive the following output:

3. In the [LangSmith UI](https://smith.langchain.com), navigate to the **default** Tracing Project for your workspace (or the workspace you specified in [Step 2](#2-set-up-environment-variables)). You'll see the OpenAI call you just instrumented.

<div style={{ textAlign: 'center' }}>
  <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call.png?fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=ba8074e55cc17ec7bbf0f6987ce15b8d" alt="LangSmith UI showing an LLM call trace called ChatOpenAI with a system and human input followed by an AI Output." data-og-width="750" width="750" data-og-height="573" height="573" data-path="langsmith/images/trace-quickstart-llm-call.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call.png?w=280&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=b94da918edfd11078bc637fdfc7fcc44 280w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call.png?w=560&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=7f5f480bee06c54f0e5ad7ce122f722c 560w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call.png?w=840&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=5e4e621619664b26cbe2d54719667ded 840w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call.png?w=1100&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=c63599fdd8f12bc1abc80982af376053 1100w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call.png?w=1650&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=69730a230b5d2cff4d737fab7d965c9f 1650w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call.png?w=2500&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=d5e73432bdd2f3788f7600364f84c96f 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call-dark.png?fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=a00c55450b4a9937b8e557ef483a4bd6" alt="LangSmith UI showing an LLM call trace called ChatOpenAI with a system and human input followed by an AI Output." data-og-width="728" width="728" data-og-height="549" height="549" data-path="langsmith/images/trace-quickstart-llm-call-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call-dark.png?w=280&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=9b67fab1c4d3d0e2e45d4a38caa1aa82 280w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call-dark.png?w=560&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=3090d984d38ebac8d83272d235a11662 560w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call-dark.png?w=840&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=e515ea96b0e90b2c8dc639bccb7d81b2 840w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call-dark.png?w=1100&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=85584b64773a98555f22cad5c85ba46e 1100w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call-dark.png?w=1650&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=bc6e44054bb139c9ed00eeb375eb0f4f 1650w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-llm-call-dark.png?w=2500&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=e2cb7aa22421bc4a7d355658a6371d14 2500w" />
</div>

## 5. Trace an entire application

You can also use the `traceable` decorator for [Python](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.traceable) or [TypeScript](https://langsmith-docs-bdk0fivr6-langchain.vercel.app/reference/js/functions/traceable.traceable) to trace your entire application instead of just the LLM calls.

1. Include the highlighted code in your app file:

2. Call the application again to create a run:

3. Return to the [LangSmith UI](https://smith.langchain.com), navigate to the **default** Tracing Project for your workspace (or the workspace you specified in [Step 2](#2-set-up-environment-variables)). You'll find a trace of the entire app pipeline with the **rag** step and the **ChatOpenAI** LLM call.

<div style={{ textAlign: 'center' }}>
  <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app.png?fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=204edddb78b671c11a48de751c2e8e19" alt="LangSmith UI showing a trace of the entire application called rag with an input followed by an output." data-og-width="750" width="750" data-og-height="425" height="425" data-path="langsmith/images/trace-quickstart-app.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app.png?w=280&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=d5ad99d3c107fe3ccb63487f43bf912e 280w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app.png?w=560&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=9f3cdb47af6471d1e508f1fa76883900 560w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app.png?w=840&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=d1a496530ed1f98ccabbda138ef10b68 840w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app.png?w=1100&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=d165f3f228f5ffaeb68b0bacc00a0f6e 1100w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app.png?w=1650&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=ccc05e2cdbaf9bd71a6bcb8536997f2e 1650w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app.png?w=2500&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=2ebc113e6930abffa89644ccfd871404 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app-dark.png?fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=2392204346d412554fbda817e082bdcd" alt="LangSmith UI showing a trace of the entire application called rag with an input followed by an output." data-og-width="738" width="738" data-og-height="394" height="394" data-path="langsmith/images/trace-quickstart-app-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app-dark.png?w=280&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=7987f9046d36d015624c91f06d38efb2 280w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app-dark.png?w=560&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=4cf9bef39d55a3aa9a31e3911fe7bdba 560w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app-dark.png?w=840&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=0f0dc65c6705b4239afc33777e214cb7 840w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app-dark.png?w=1100&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=d2ccb5a3e2e91e45757f57f43b261861 1100w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app-dark.png?w=1650&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=2aec3b239854f4fd4f38807b991e5812 1650w, https://mintcdn.com/langchain-5e9cc07a/C5sS0isXOt0-nMfw/langsmith/images/trace-quickstart-app-dark.png?w=2500&fit=max&auto=format&n=C5sS0isXOt0-nMfw&q=85&s=b6ee98094ed25e6f2d61fed7241d648e 2500w" />
</div>

Here are some topics you might want to explore next:

* [Tracing integrations](/langsmith/trace-with-langchain) provide support for various LLM providers and agent frameworks.
* [Filtering traces](/langsmith/filter-traces-in-application) can help you effectively navigate and analyze data in tracing projects that contain a significant amount of data.
* [Trace a RAG application](/langsmith/observability-llm-tutorial) is a full tutorial, which adds observability to an application from development through to production.
* [Sending traces to a specific project](/langsmith/log-traces-to-project) changes the destination project of your traces.

<Callout type="info" icon="bird">
  After logging traces, use **[Polly](/langsmith/polly)** to analyze them and get AI-powered insights into your application's performance.
</Callout>

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/fA9b4D8IsPQ?si=0eBb1vzw5AxUtplS" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/observability-quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
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

## 2. Set up environment variables

Set the following environment variables:

* `LANGSMITH_TRACING`
* `LANGSMITH_API_KEY`
* `OPENAI_API_KEY` (or your LLM provider's API key)
* (optional) `LANGSMITH_WORKSPACE_ID`: If your LangSmith API key is linked to multiple workspaces, set this variable to specify which workspace to use.
```

Example 3 (unknown):
```unknown
If you're using Anthropic, use the [Anthropic wrapper](/langsmith/annotate-code#wrap-the-anthropic-client-python-only) to trace your calls. For other providers, use [the traceable wrapper](/langsmith/annotate-code#use-%40traceable-%2F-traceable).

## 3. Define your application

You can use the example app code outlined in this step to instrument a RAG application. Or, you can use your own application code that includes an LLM call.

This is a minimal RAG app that uses the OpenAI SDK directly without any LangSmith tracing added yet. It has three main parts:

* **Retriever function**: Simulates document retrieval that always returns the same string.
* **OpenAI client**: Instantiates a plain OpenAI client to send a chat completion request.
* **RAG function**: Combines the retrieved documents with the user’s question to form a system prompt, calls the `chat.completions.create()` endpoint with `gpt-4o-mini`, and returns the assistant’s response.

Add the following code into your app file (e.g., `app.py` or `app.ts`):

<CodeGroup>
```

Example 4 (unknown):
```unknown

```

---

## Upgrade an installation

**URL:** llms-txt#upgrade-an-installation

**Contents:**
- Kubernetes(Helm)
  - Validate your deployment:
- Docker
  - Validate your deployment:

Source: https://docs.langchain.com/langsmith/self-host-upgrades

For general upgrade instructions, please follow the instructions below. Certain versions may have specific upgrade instructions, which will be detailed in more specific upgrade guides.

If you don't have the repo added, run the following command to add it:

Update your local helm repo

Update your helm chart config file with any updates that are needed in the new version. These will be detailed in the release notes for the new version.

Run the following command to upgrade the chart(replace version with the version you want to upgrade to):

<Note>
  If you are using a namespace other than the default namespace, you will need to specify the namespace in the `helm` and `kubectl` commands by using the `-n <namespace` flag.
</Note>

Find the latest version of the chart. You can find this in the [LangSmith Helm Chart GitHub repository](https://github.com/langchain-ai/helm/releases) or by running the following command:

You should see an output similar to this:

Choose the version you want to upgrade to (generally the latest version is recommended) and note the version number.

Verify that the upgrade was successful:

All pods should be in the `Running` state. Verify that clickhouse is running and that both `migrations` jobs have completed.

### Validate your deployment:

1. Run `kubectl get services`

Output should look something like:

2. Curl the external ip of the `langsmith-frontend` service:

Check that the version matches the version you upgraded to.

3. Visit the external ip for the `langsmith-frontend` service on your browser

The LangSmith UI should be visible/operational

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=5310f686e7b9eebaaee4fe2a152a8675" alt="LangSmith UI" data-og-width="2886" width="2886" data-og-height="1698" height="1698" data-path="langsmith/images/langsmith-ui.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=5f155ce778ca848f89fefff237b69bcb 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=1d55d4068a9f53387c129b4688b0971e 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=feb20198d67249ece559e5fd0e6d8e98 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=3e5eba764d911e567d5aaa9e5702327b 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=d45af56632578a8d1b05e546dfc8d01d 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=16a49517a6c224930fdb81c9ccde5527 2500w" />

Upgrading the Docker version of LangSmith is a bit more involved than the Helm version and may require a small amount of downtime. Please follow the instructions below to upgrade your Docker version of LangSmith.

1. Update your `docker-compose.yml` file to the file used in the latest release. You can find this in the [LangSmith SDK GitHub repository](https://github.com/langchain-ai/langsmith-sdk/blob/main/python/langsmith/cli/docker-compose.yaml)
2. Update your `.env` file with any new environment variables that are required in the new version. These will be detailed in the release notes for the new version.
3. Run the following command to stop your current LangSmith instance:

4. Run the following command to start your new LangSmith instance in the background:

If everything ran successfully, you should see all the LangSmith containers running and healthy.

### Validate your deployment:

1. Curl the exposed port of the `cli-langchain-frontend-1` container:

2. Visit the exposed port of the `cli-langchain-frontend-1` container on your browser

The LangSmith UI should be visible/operational

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=5310f686e7b9eebaaee4fe2a152a8675" alt="LangSmith UI" data-og-width="2886" width="2886" data-og-height="1698" height="1698" data-path="langsmith/images/langsmith-ui.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=5f155ce778ca848f89fefff237b69bcb 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=1d55d4068a9f53387c129b4688b0971e 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=feb20198d67249ece559e5fd0e6d8e98 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=3e5eba764d911e567d5aaa9e5702327b 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=d45af56632578a8d1b05e546dfc8d01d 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-ui.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=16a49517a6c224930fdb81c9ccde5527 2500w" />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/self-host-upgrades.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
Update your local helm repo
```

Example 2 (unknown):
```unknown
Update your helm chart config file with any updates that are needed in the new version. These will be detailed in the release notes for the new version.

Run the following command to upgrade the chart(replace version with the version you want to upgrade to):

<Note>
  If you are using a namespace other than the default namespace, you will need to specify the namespace in the `helm` and `kubectl` commands by using the `-n <namespace` flag.
</Note>

Find the latest version of the chart. You can find this in the [LangSmith Helm Chart GitHub repository](https://github.com/langchain-ai/helm/releases) or by running the following command:
```

Example 3 (unknown):
```unknown
You should see an output similar to this:
```

Example 4 (unknown):
```unknown
Choose the version you want to upgrade to (generally the latest version is recommended) and note the version number.
```

---

## Use an existing secret for your installation (Kubernetes)

**URL:** llms-txt#use-an-existing-secret-for-your-installation-(kubernetes)

**Contents:**
- Requirements
- Parameters
- Configuration

Source: https://docs.langchain.com/langsmith/self-host-using-an-existing-secret

By default, LangSmith will provision several Kubernetes secrets to store sensitive information such as license keys, salts, and other configuration parameters. However, you may want to use an existing secret that you have already created in your Kubernetes cluster (or provisioned via some sort of secrets operator). This can be useful if you want to manage sensitive information in a centralized way or if you have specific security requirements.

By default we will provision the following secrets corresponding to different components of LangSmith:

* `langsmith-secrets`: This secret contains the license key and some other basic configuration parameters. You can see the template for this secret [here](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/secrets.yaml)
* `langsmith-redis`: This secret contains the Redis connection string (or node URIs if using Redis cluster) and password. You can see the template for this secret [here](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/redis/secrets.yaml)
* `langsmith-postgres`: This secret contains the Postgres connection string and password. You can see the template for this secret [here](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/postgres/secrets.yaml)
* `langsmith-clickhouse`: This secret contains the ClickHouse connection string and password. You can see the template for this secret [here](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/clickhouse/secrets.yaml)

* An existing Kubernetes cluster
* A way to create Kubernetes secrets in your cluster. This can be done using `kubectl`, a Helm chart, or a secrets operator like [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)

You will need to create your own Kubernetes secrets that adhere to the structure of the secrets provisioned by the LangSmith Helm Chart.

<Warning>
  The secrets must have the same structure as the ones provisioned by the LangSmith Helm Chart (refer to the links above to see the specific secrets). If you miss any of the required keys, your LangSmith instance may not work correctly.
</Warning>

An example secret may look like this:

With these secrets provisioned, you can configure your LangSmith instance to use the secrets directly to avoid passing in secret values through plaintext. You can do this by modifying the `langsmith_config.yaml` file for your LangSmith Helm Chart installation.

Once configured, you will need to update your LangSmith installation. You can follow our upgrade guide [here](/langsmith/self-host-upgrades). If everything is configured correctly, your LangSmith instance should now be accessible via the Ingress. You can run the following to check that your secrets are being used correctly:

You should see something like this in the output:

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/self-host-using-an-existing-secret.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
## Configuration

With these secrets provisioned, you can configure your LangSmith instance to use the secrets directly to avoid passing in secret values through plaintext. You can do this by modifying the `langsmith_config.yaml` file for your LangSmith Helm Chart installation.
```

Example 2 (unknown):
```unknown
Once configured, you will need to update your LangSmith installation. You can follow our upgrade guide [here](/langsmith/self-host-upgrades). If everything is configured correctly, your LangSmith instance should now be accessible via the Ingress. You can run the following to check that your secrets are being used correctly:
```

Example 3 (unknown):
```unknown
You should see something like this in the output:
```

---

## ... Setup authenticate, etc.

**URL:** llms-txt#...-setup-authenticate,-etc.

**Contents:**
- Learn more

@auth.on
async def add_owner(
    ctx: Auth.types.AuthContext,
    value: dict  # The payload being sent to this access method
) -> dict:  # Returns a filter dict that restricts access to resources
    if is_studio_user(ctx.user):
        return {}

filters = {"owner": ctx.user.identity}
    metadata = value.setdefault("metadata", {})
    metadata.update(filters)
    return filters
```

Only use this if you want to permit developer access to a graph deployed on the managed LangSmith SaaS.

* [Authentication & Access Control](/langsmith/auth)
* [Setting up custom authentication tutorial](/langsmith/set-up-custom-auth)

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/custom-auth.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---
