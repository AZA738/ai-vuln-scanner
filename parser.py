import xml.etree.ElementTree as ET
import json
import os
import sys

def parse_nmap_xml(xml_file: str) -> list:
    """
    Parses Nmap XML output to extract open ports and service version strings.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except Exception as e:
        print(f"[-] Failed to parse XML: {e}", file=sys.stderr)
        return []

    services = []
    
    # Iterate through all detected hosts and ports
    for host in root.findall('.//host'):
        ip_addr = host.find('.//address').get('addr') if host.find('.//address') is not None else "Unknown"
        
        for port in host.findall('.//port'):
            state = port.find('state')
            if state is None or state.get('state') != 'open':
                continue # Skip closed or filtered ports
                
            port_id = port.get('portid')
            
            # Extract service version strings
            service = port.find('service')
            if service is not None:
                service_name = service.get('name', 'unknown')
                product = service.get('product', '')
                version = service.get('version', '')
                
                # Combine into a single readable string
                full_version = f"{product} {version}".strip()
                
                if full_version:
                    services.append({
                        "ip": ip_addr,
                        "port": port_id,
                        "service": service_name,
                        "version": full_version
                    })
                    
    return services

if __name__ == "__main__":
    target_file = "outputs/scanme.nmap.org_scan.xml"
    output_json = "outputs/parsed_services.json"
    
    if not os.path.exists(target_file):
        print(f"[-] Missing {target_file}. Run recon.py first.")
        sys.exit(1)
        
    print(f"[*] Parsing raw XML from {target_file}...")
    parsed_data = parse_nmap_xml(target_file)
    
    with open(output_json, "w") as f:
        json.dump(parsed_data, f, indent=4)
        
    print(f"[+] Parsing complete. Isolated {len(parsed_data)} services.")
    print(f"[+] Structured data saved to: {output_json}")
