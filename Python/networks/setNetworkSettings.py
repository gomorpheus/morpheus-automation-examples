import requests, json, urllib3  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bearerToken = morpheus['morpheus']['apiAccessToken']
host = morpheus['morpheus']['applianceHost']
morphheaders = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + bearerToken
}

def updateNetwork(network_vlanId, network_cidr, network_subnet, network_gateway):
    url = f"https://{host}/api/networks/{network_vlanId}"
    headers = morphheaders
    payload = {
        "network": {
            "vlanId": network_vlanId,
            "cidr": network_cidr,
            "subnet": network_subnet,
            "gateway": network_gateway
        }
    }
    response = requests.put(url, headers=headers, json=payload, verify=False)
    data = response.json()
    if data['success'] == True:
        print(f'Network {network_vlanId} updated successfully')
    else:
        print(f'Failed to update network {network_vlanId}')

def getAllNetworks():
    url = f"https://{host}/api/networks?max=-1"
    headers = morphheaders
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    if data['success'] == True:
        for network in data['networks']:
            raw_name = network['name']
            print(f'name = {raw_name}')

            # 1) Ignore everything after the first space (e.g., "2514-10.37.37.0-24 pp.local")
            name = raw_name.split(' ')[0]

            # 2) Split by '-'
            parts = name.split('-') if name else []
            if not parts:
                continue

            # 3) Find first part starting with a digit => vlanId; if none, skip this network
            vlan_part_index = None
            for i, p in enumerate(parts):
                if p and p[0].isdigit():
                    vlan_part_index = i
                    break
            if vlan_part_index is None:
                # Ignore all networks that don't start with numbers in any segment
                print(f'Skipping network {name}, no numeric-leading part present')
                continue

            network_vlanId = parts[vlan_part_index]
            print(f'network_vlanId = {network_vlanId}')

            # 4) Next, find the CIDR base part (IP or IP%2fMASK) after vlan part, skipping non-numeric-leading tokens
            cidr_base = None
            subnet_part = None
            j = vlan_part_index + 1
            while j < len(parts) and cidr_base is None:
                candidate = parts[j]
                if candidate and candidate[0].isdigit():
                    cidr_base = candidate
                else:
                    j += 1
                    continue
                # If we found a numeric-leading candidate, stop loop (handled below)
                break

            if cidr_base is None:
                print(f'Skipping network {name}, no CIDR base found after VLAN')
                continue

            # 5) Handle cases like 10.39.171.0%2f25 => split at %2f
            if '%2f' in cidr_base:
                ip_and_mask = cidr_base.split('%2f', 1)
                network_cidr = ip_and_mask[0]
                network_subnet = ip_and_mask[1] if len(ip_and_mask) > 1 else None
            else:
                network_cidr = cidr_base
                # Subnet is expected to be the next part, if numeric-leading
                next_idx = j + 1
                network_subnet = parts[next_idx] if next_idx < len(parts) and parts[next_idx] and parts[next_idx][0].isdigit() else None

            if not network_cidr or not network_subnet:
                print(f'Skipping network {name}, incomplete CIDR/subnet information')
                continue

            print(f'network_cidr = {network_cidr}/{network_subnet}')

            # 6) Compute a simple gateway from the last octet + 1 (retain existing behavior)
            try:
                network_gateway = int(network_cidr.split('.')[-1]) + 1
            except Exception:
                print(f'Skipping network {name}, unable to derive gateway')
                continue
            print(f'network_gateway = {network_gateway}')
            print(f'Updating network {name} with network_vlanId = {network_vlanId}, network_cidr = {network_cidr}, network_subnet = {network_subnet}, network_gateway = {network_gateway}')
            # updateNetwork(network_vlanId, network_cidr, network_subnet, network_gateway)
    else:
        print(f"Failed to get networks")
        return None
    
getAllNetworks()
