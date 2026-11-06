**AI Policy Validation Platform
**


A hybrid AI system that validates cloud resources against security and

compliance policies. It combines \*\*deterministic rule-based validation\*\*

with \*\*RAG + LLM reasoning\*\* for ambiguous, natural-language policies.







 1. What It Does



Submit a resource (e.g. a database) and the platform decides whether it

\*\*PASSES\*\*, \*\*FAILS\*\*, or needs \*\*REVIEW\*\* against your policies.



Example request:



```json

{

 "resource\_type": "database",

 "resource\_name": "customer-db",

 "attributes": { "public\_access": true }

}



{

 "source": "deterministic\_rule",

 "policy\_id": "DB-001",

 "status": "FAIL",

 "reason": "Production databases must not be publicly accessible."

}



2. Why Hybrid (Rules + LLM)?

Case	Engine	Reason

public\_access == true	Deterministic rule	Fast, cheap, 100% reproducible

"Data must only be accessed via approved internal services"	RAG + LLM	Requires interpretation of natural language

Missing information	REVIEW	LLM instructed never to invent facts

Design principle: Never use an LLM when a deterministic rule is enough.

This gives lower cost, lower latency, better auditability, and less

hallucination risk at scale.



3 Architecture
                 ┌─────────────────────┐
                 │  Policy Documents   │  (YAML / S3)
                 └──────────┬──────────┘
                            │
                     Embeddings (RAG)
                            │
                            ▼
Client ──► FastAPI ──► Policy Agent
                         │       │
                 ┌───────┘       └────────┐
                 ▼                        ▼
          Rule Engine                  RAG + LLM
        (deterministic)               (reasoning)
                 │                        │
                 └──────────┬─────────────┘
                            ▼
                   PASS / FAIL / REVIEW
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
            Audit       Monitoring    Human Review
                        (CloudWatch)

4 Tech Stack

Layer	Technology

API	FastAPI + Uvicorn

Rules	Pure Python

Policy store	YAML files

Retrieval	sentence-transformers (all-MiniLM-L6-v2), cosine similarity

LLM	OpenAI (gpt-4o-mini), JSON mode, temperature=0

Testing	pytest + unittest.mock

Packaging	Docker

CI/CD	GitHub Actions

Cloud (target)	AWS ECS/Fargate, ECR, S3, IAM, Secrets Manager, CloudWatch

5\. Project Structure

text

ai-policy-validator/

├── app/

│   ├── main.py               # FastAPI app + routes

│   ├── models.py             # Pydantic request models

│   ├── validator.py          # Deterministic rule engine

│   ├── semantic\_retriever.py # Embeddings + cosine similarity search

│   ├── llm\_validator.py      # OpenAI structured validation

│   ├── policy\_service.py     # Orchestration: rules → RAG → LLM

│   └── policy\_agent.py       # Agentic orchestration (bounded tools)

├── policies/                 # YAML policy definitions

├── tests/

│   ├── test\_validator.py

│   ├── test\_api.py

│   ├── test\_semantic\_retriever.py

│   └── test\_llm\_validator.py

├── Dockerfile

├── requirements.txt

├── pytest.ini

└── README.md

6\. API Endpoints

Method	Path	Description

GET	/health	Health check

POST	/validate	Validate a resource against policies

Interactive docs: http://127.0.0.1:8000/docs



7\. Setup \& Run

Install dependencies

bash

python -m pip install -r requirements.txt

Set your OpenAI key (PowerShell)

powershell

$env:OPENAI\_API\_KEY="your-key-here"

Run tests

bash

python -m pytest -q

Expected: 6 passed (the 2 Hugging Face symlink warnings on Windows are harmless).



Start the API

bash

python -m uvicorn app.main:app --reload

8\. RAG Pipeline Explained

Policy ingestion — YAML policies loaded from policies/.



Embedding — Each policy is converted to a vector via sentence-transformers.



Query embedding — Resource type + name + attributes are embedded.



Similarity search — Cosine similarity, top-K policies retrieved.



LLM grounding — Retrieved policies are passed as context to the LLM.



Structured output — LLM returns JSON validated against a schema.



Why RAG? Policies are external, private, and frequently changing.

RAG avoids retraining, keeps policies updateable, and provides evidence

for auditability.



Security \& Responsible AI

Risk	Mitigation

Hallucination	RAG grounding + schema validation + confidence thresholds

Prompt injection	Treat retrieved docs as data, not instructions

Dangerous actions	LLM → agent → authorization → tool → validation → human approval

Secrets leakage	AWS Secrets Manager, IAM, least privilege

Unreliable output	Deterministic rules as authority; LLM assists, never decides alone

11\. Docker

bash

docker build -t ai-policy-validator .

docker run -p 8000:8000 -e OPENAI\_API\_KEY=$env:OPENAI\_API\_KEY ai-policy-validator

12\. CI/CD (GitHub Actions)

On every push/PR:



Install dependencies



Run pytest



Build Docker image



(extendable) Push to ECR → Deploy to ECS



13\. Target AWS Architecture

text

Internet → ALB → ECS Fargate (FastAPI containers)

&#x20;                    │

&#x20;     ┌──────────────┼──────────────┐

&#x20;     ▼              ▼              ▼

&#x20;    S3         Vector Store   Secrets Manager

&#x20;(policy docs)                 (API keys)

&#x20;                    │

&#x20;                    ▼

&#x20;               CloudWatch (logs + metrics)

14\. Monitoring Checklist

API: requests, errors, latency, availability



LLM: token usage, cost, latency, timeouts



RAG: retrieval latency, top-K relevance, missing context



Agent: step count, tool failures, loops



Policy quality: PASS/FAIL accuracy, false positives/negatives, REVIEW rate, human overrides



15\. Roadmap

☑ Python rule engine + tests

☑ FastAPI /validate + /health

☑ YAML policy repository

☑ Semantic retrieval (embeddings + cosine similarity)

☑ LLM validator with structured JSON output

□ Agent orchestration 







