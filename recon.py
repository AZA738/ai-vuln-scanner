import subprocess
import os
import sys

def run_nmap_scan(target: str, output_dir: str = "outputs") -> str:
    """
    Executes a service version scan (-sV) against an authorized target
    and exports the results to an XML file for downstream parsing.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_xml_path = os.path.join(output_dir, f"{target}_scan.xml")
    
    # Construct the CLI command
    # -sV: Probe open ports to determine service/version info
    # -oX: Output scan results in XML format
    command = ["nmap", "-sV", "-oX", output_xml_path, target]
    
    print(f"[*] Launching Nmap service scan against: {target}")
    print(f"[*] Command: {' '.join(command)}")
    
    try:
        # Run command via subprocess
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[+] Scan completed successfully.")
        print(f"[+] Raw XML saved to: {output_xml_path}")
        return output_xml_path

    except FileNotFoundError:
        print("[-] Error: 'nmap' is not installed or not found in system PATH.", file=sys.stderr)
        return ""
    except subprocess.CalledProcessError as e:
        print(f"[-] Nmap scan failed with return code {e.returncode}:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return ""

if __name__ == "__main__":
    # Test against Nmap's officially authorized scan target
    TARGET_HOST = "scanme.nmap.org"
    
    scan_file = run_nmap_scan(TARGET_HOST)
    if scan_file:
        print(f"[*] Ready for parsing module: {scan_file}")
