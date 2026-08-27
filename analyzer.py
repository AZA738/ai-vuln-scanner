import json
import os
import sys
from openai import OpenAI

def analyze_services(json_file: str):
    if not os.path.exists(json_file):
        print(f"[-] Missing {json_file}. Run parser.py first.")
        sys.exit(1)

    with open(json_file, 'r') as f:
        services = json.load(f)

    if not services:
        print("[-] No active services found to analyze.")
        sys.exit(0)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[-] Error: OPENAI_API_KEY environment variable not set.")
        print("[-] Run: export OPENAI_API_KEY='your_key_here'")
        sys.exit(1)
        
    print(f"[*] Loaded {len(services)} services. Connecting to OpenAI Triage Engine...")
    
    client = OpenAI(api_key=api_key)

    prompt = (
        "You are a cybersecurity vulnerability analyst. Review the following list of scanned services "
        "and their version numbers. For each service, identify any known major Common Vulnerabilities "
        "and Exposures (CVEs) and provide a brief remediation summary. Do not execute any commands.\n\n"
        f"Services Data: {json.dumps(services, indent=2)}"
    )

    try:
        # Temperature parameter removed for gpt-5.6-luna compatibility
        response = client.chat.completions.create(
            model="gpt-5.6-luna", 
            messages=[
                {"role": "system", "content": "You are a helpful cybersecurity assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
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
