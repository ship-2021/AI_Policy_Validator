# AI Policy Validation Platform

A built, working AI system that validates cloud resources against security
and compliance policies. Resources are submitted to a FastAPI endpoint for
validation. Validation starts with deterministic Python rules for
predictable controls, then uses semantic retrieval (embeddings) so relevant
policies are found by meaning rather than keywords, and integrates an LLM
for ambiguous, natural-language policies. The result is a structured
PASS / FAIL / REVIEW outcome.

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
public_access == true	Deterministic rule	Fast, cheap, 100% reproducible
"Data must only be accessed via approved internal services"	RAG + LLM	Requires interpretation of natural language
Missing information	REVIEW	LLM instructed never to invent facts
Design principle: never use an LLM when a deterministic rule is enough.
This gives lower cost, lower latency, better auditability, and less
hallucination risk at scale.

3. Architecture
text
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
4. Tech Stack
Layer	Technology
API	FastAPI + Uvicorn
Rules	Pure Python
Policy store	YAML files
Retrieval	sentence-transformers (all-MiniLM-L6-v2), cosine similarity
LLM	OpenAI (gpt-4o-mini), JSON mode, temperature=0
Agent	Bounded tool orchestration
Testing	pytest + unittest.mock
Packaging	Docker
CI/CD	GitHub Actions
Cloud (target)	AWS ECS/Fargate, ECR, S3, IAM, Secrets Manager, CloudWatch
5. Project Structure
text
ai-policy-validator/
├── app/
│   ├── main.py               # FastAPI app + routes
│   ├── models.py             # Pydantic request models
│   ├── validator.py          # Deterministic rule engine
│   ├── semantic_retriever.py # Embeddings + cosine similarity search
│   ├── llm_validator.py      # OpenAI structured validation
│   ├── policy_service.py     # Orchestration: rules → RAG → LLM
│   └── policy_agent.py       # Agentic orchestration (bounded tools)
├── policies/                 # YAML policy definitions
├── tests/
│   ├── test_validator.py
│   ├── test_api.py
│   ├── test_semantic_retriever.py
│   └── test_llm_validator.py
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
6. API Endpoints
Method	Path	Description
GET	/health	Health check
POST	/validate	Validate a resource against policies
Interactive docs: http://127.0.0.1:8000/docs

7. Setup & Run
Install dependencies:

bash
python -m pip install -r requirements.txt
Set your OpenAI key (PowerShell):

powershell
$env:OPENAI_API_KEY="your-key-here"
Run tests:

bash
python -m pytest -q
Expected: 6 passed (the 2 Hugging Face symlink warnings on Windows are harmless).

Start the API:

bash
python -m uvicorn app.main:app --reload
8. RAG Pipeline Explained
Policy ingestion — YAML policies loaded from policies/.

Embedding — each policy is converted to a vector via sentence-transformers.

Query embedding — resource type + name + attributes are embedded.

Similarity search — cosine similarity, top-K policies retrieved.

LLM grounding — retrieved policies are passed as context to the LLM.

Structured output — LLM returns JSON validated against a schema.

Why RAG? Policies are external, private, and frequently changing.
RAG avoids retraining, keeps policies updateable, and provides evidence
for auditability.

9. Security & Responsible AI
Risk	Mitigation
Hallucination	RAG grounding + schema validation + confidence thresholds
Prompt injection	Treat retrieved docs as data, not instructions
Dangerous actions	LLM → agent → authorization → tool → validation → human approval
Secrets leakage	AWS Secrets Manager, IAM, least privilege
Unreliable output	Deterministic rules as authority; LLM assists, never decides alone
10. Docker
bash
docker build -t ai-policy-validator .
docker run -p 8000:8000 -e OPENAI_API_KEY=$env:OPENAI_API_KEY ai-policy-validator
11. CI/CD (GitHub Actions)
On every push/PR:

Install dependencies

Run pytest

Build Docker image

(extendable) Push to ECR → Deploy to ECS

12. AWS Target Architecture
text

Internet → ALB → ECS Fargate (FastAPI containers)
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
     S3         Vector Store   Secrets Manager
 (policy docs)                 (API keys)
                     │
                     ▼
                CloudWatch (logs + metrics)

13. Monitoring Checklist
API: requests, errors, latency, availability

LLM: token usage, cost, latency, timeouts

RAG: retrieval latency, top-K relevance, missing context

Agent: step count, tool failures, loops

Policy quality: PASS/FAIL accuracy, false positives/negatives, REVIEW rate, human overrides

14. Roadmap
☑ Python rule engine + tests
☑ FastAPI /validate + /health
☑ YAML policy repository
☑ Semantic retrieval (embeddings + cosine similarity)
☑ LLM validator with structured JSON output
☑ Agent orchestration
☑ Docker containerisation
☑ CI/CD pipeline (GitHub Actions)
☑ AWS deployment architecture documented
□ Live AWS deployment
□ Production monitoring + Responsible AI controls
text

