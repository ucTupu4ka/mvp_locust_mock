# Transfer Context For New Project

## Candidate Profile
- Name: Dmitry Yakovlev
- Target role: QA Automation Engineer (Python, pytest), Middle
- Core commercial background: mobile game automation (Python + pytest + Appium), API-first setup, E2E/UI testing
- CI/CD real experience: TeamCity
- Main strength: building and maintaining test frameworks, reusable fixtures/markers/hooks, test stability and reporting

## Current Goal
Prepare quickly for interviews where the stack includes:
- Python, pytest
- Docker, Linux
- API and microservice testing
- Message brokers (Kafka / RabbitMQ / NATS)
- Locust (load testing)
- Mock servers
- CI/CD (vacancy mentions Jenkins; candidate has TeamCity experience)

## Honest Experience Mapping (important for interview positioning)
- Python + pytest: strong practical commercial experience
- API automation/integration: strong practical commercial experience
- Docker: practical usage experience
- Linux/terminal: practical usage experience
- CI/CD: TeamCity (not Jenkins directly)
- Kafka/RabbitMQ/NATS: no direct commercial experience
- Locust: no direct commercial experience
- Mock servers: no direct commercial production ownership
- Hypervisors (vSphere/Hyper-V/Xen/oVirt): no direct experience
- Playwright: no direct commercial experience
- E-commerce domain: no direct domain experience (but has adjacent monetization flow testing in games)

## What Was Discussed As Interview Strategy
1. Be fully honest about missing tools (Locust, brokers, mock servers, hypervisors).
2. Emphasize transferable strengths:
   - framework architecture ownership,
   - integration/API testing,
   - CI/CD integration,
   - quality and maintainability practices.
3. For Jenkins questions:
   - explain TeamCity experience and mapping of principles (pipeline stages, artifacts, gates, retries, test reports).
4. For missing technologies:
   - show initiative with a fast MVP/pet project to demonstrate practical understanding.

## Suggested Fast MVP (4 hours) For Interview Proof
Objective: create a tiny but working project using Docker + mock API + Locust.

Minimum scope:
- Service 1: mock API (FastAPI or Flask), 2-3 endpoints
- Service 2: Locust load generator
- Docker Compose to run both
- Scenarios:
  - GET /health
  - POST /orders
  - GET /orders/{id}
- One negative behavior:
  - return occasional 500 or artificial delay
- Deliverables:
  - run instructions,
  - screenshot from Locust UI,
  - short conclusions (p95/error rate/basic observations)

Timebox:
- 45 min: mock API
- 35 min: Dockerfile + compose
- 60 min: locustfile scenarios
- 40 min: run/debug
- 40 min: test runs + screenshots
- 20 min: README + interview talking points

## Ready-To-Use Interview Positioning (short version)
"Commercially I have strong Python + pytest automation experience and framework development, API/integration and E2E testing, plus CI/CD via TeamCity. For technologies where I had no production ownership (Locust, brokers, mock servers), I built a small Dockerized MVP to validate practical basics and can ramp up quickly."

## Requested Workflow For Next Project
In the next project, assistant should:
1. Start with a detailed execution plan.
2. Guide step-by-step with clear "what to do" + "why it matters".
3. Keep each step small and verifiable.
4. Prioritize a realistic interview-ready outcome over overengineering.
5. Finish with:
   - interview script,
   - likely questions/answers,
   - concise project summary for CV/cover letter.
