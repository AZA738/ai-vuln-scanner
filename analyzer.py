import json
import os
import sys
from openai import OpenAI

def analyze_services(json_file: str):
    # Verify that the Data Normalization stage (parser.py) has successfully completed
    if not os.path.exists(json_file):
        print(f"[-] Missing {json_file}. Run parser.py first.")
        sys.exit(1)

    # Load the structured JSON payload containing isolated software version strings
    with open(json_file, 'r') as f:
        services = json.load(f)

    if not services:
        print("[-] No active services found to analyze.")
        sys.exit(0)

    # Securely load the OpenAI API key from the environment variables
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[-] Error: OPENAI_API_KEY environment variable not set.")
        print("[-] Run: export OPENAI_API_KEY='your_key_here'")
        sys.exit(1)
        
    print(f"[*] Loaded {len(services)} services. Connecting to OpenAI Triage Engine...")
    
    client = OpenAI(api_key=api_key)
    
    # Deterministic System Prompt: Instructs the model to evaluate only the provided 
    # service banners and restricts it from executing any autonomous commands
    prompt = (
        "You are a cybersecurity vulnerability analyst. Review the following list of scanned services "
        "and their version numbers. For each service, identify any known major Common Vulnerabilities "
        "and Exposures (CVEs) and provide a brief remediation summary. Do not execute any commands.\n\n"
        f"Services Data: {json.dumps(services, indent=2)}"
    )

    try:
        # Transmit the structured payload to the OpenAI API for CVE summarization
        response = client.chat.completions.create(
            model="gpt-5.6-luna", 
            messages=[
                {"role": "system", "content": "You are a helpful cybersecurity assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Output the findings directly to the terminal for Human-in-the-Loop (HITL) validation.
        # This manual review eliminates AI hallucinations and prevents autonomous exploit execution.
        print("\n" + "="*60)
        print("       AI VULNERABILITY TRIAGE REPORT (HITL REVIEW)")
        print("="*60)
        print(response.choices[0].message.content)
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"[-] API Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    target_data = "outputs/parsed_services.json"
    analyze_services(target_data)
