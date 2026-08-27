# AI-Driven Vulnerability Scanner & Analytical Harness

A custom vulnerability scanning architecture built within a Kali Linux environment. This project utilizes Python to orchestrate standard offensive security tools, parse their outputs into structured data, and leverage OpenAI's LLM API for vulnerability triage and CVE summarization. 

Designed for safe, authorized bug bounty reconnaissance, this tool strictly adheres to a Human-in-the-Loop (HITL) model to verify findings and prevent autonomous execution risks.

## 🛠️ Tech Stack & Tools
* **Languages & Formats:** Python, JSON, XML
* **Security Tools:** Nmap, Sublist3r, Burp Suite, FFuF
* **AI & Integration:** OpenAI API (gpt-5.6-luna), REST APIs
* **Environment:** Kali Linux

## 🏗️ System Architecture & Data Pipeline
This scanner operates on a sequential three-stage data pipeline:

1. **Reconnaissance Module (`recon.py`):** Acts as the orchestration layer, executing scoped network discovery scans against authorized targets and capturing raw network artifacts (e.g., Nmap XML outputs).
2. **Data Normalization (`parser.py`):** Ingests raw outputs, strips irrelevant network noise, and extracts open ports, banners, and specific software version strings into structured JSON payloads.
3. **LLM Triage Engine (`analyzer.py`):** Connects to the OpenAI REST API, transmitting the structured JSON payloads to identify outdated service versions, map known CVEs, and generate remediation summaries.

## 🛡️ Operational Safety & Compliance
Integrating automated tooling with bug bounty targets requires strict guardrails. This project implements several safety measures:
* **Human-in-the-Loop (HITL) Validation:** The AI model is strictly limited to data interpretation and reporting. All AI-suggested vulnerabilities are manually reviewed by the operator to eliminate hallucinations and prevent autonomous exploit execution.
* **Scope Enforcement:** Target domain whitelists and hardcoded scopes prevent scans outside of authorized bug bounty parameters.
* **Platform Adherence:** Prevents heavy, aggressive automated scanning that could degrade target services, adhering to standard bug bounty Terms of Service.

## 🚀 Quick Start
*(Note: Requires a valid OpenAI Developer API Key)*

```bash
# 1. Clone the repository
git clone [https://github.com/AZA738/ai-vuln-scanner.git](https://github.com/AZA738/ai-vuln-scanner.git)
cd ai-vuln-scanner

# 2. Activate virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install openai

# 3. Load API Key
export OPENAI_API_KEY="your-api-key-here"

# 4. Run the pipeline modules
python3 recon.py
python3 parser.py
python3 analyzer.py
