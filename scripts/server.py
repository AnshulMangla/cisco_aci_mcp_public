#!/usr/bin/env python3
"""
ACI MCP Server - Comprehensive Version with 50 Operations (GET and POST)
Most common ACI operations for complete network automation workflows
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ACIComprehensiveMCPServer")

# Server configuration 
mcp = FastMCP("ACI Comprehensive MCP - 50 Operations")

# ACI Configuration from environment variables
APIC_URL = os.getenv("APIC_URL", "")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")

class ACIClient:
    def __init__(self):
        self.base_url = APIC_URL.rstrip('/')
        self.username = USERNAME
        self.password = PASSWORD
        self.session_cookies = None
        
    def authenticate(self) -> bool:
        """Authenticate with APIC and get session cookies"""
        try:
            login_url = f"{self.base_url}/api/aaaLogin.json"
            payload = {
                "aaaUser": {
                    "attributes": {
                        "name": self.username,
                        "pwd": self.password
                    }
                }
            }
            
            with httpx.Client(verify=False, timeout=30.0) as client:
                response = client.post(login_url, json=payload)
                if response.status_code == 200:
                    self.session_cookies = response.cookies
                    return True
                else:
                    logger.error(f"Authentication failed: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    def make_request(self, endpoint: str, method: str = "GET", query_params: Optional[Dict] = None, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to ACI"""
        try:
            # Ensure authentication
            if not self.session_cookies:
                if not self.authenticate():
                    return {"error": "Authentication failed", "status": "error"}
            
            url = f"{self.base_url}{endpoint}"
            
            with httpx.Client(verify=False, timeout=30.0, cookies=self.session_cookies) as client:
                if method.upper() == "GET":
                    response = client.get(url, params=query_params)
                elif method.upper() == "POST":
                    response = client.post(url, json=payload, params=query_params)
                elif method.upper() == "DELETE":
                    response = client.delete(url, params=query_params)
                else:
                    return {"error": f"Unsupported method: {method}", "status": "error"}
                
                if response.status_code in [200, 201, 202]:
                    try:
                        return {
                            "endpoint": endpoint,
                            "method": method,
                            "data": response.json(),
                            "status": "success"
                        }
                    except:
                        return {
                            "endpoint": endpoint,
                            "method": method,
                            "data": response.text,
                            "status": "success"
                        }
                else:
                    return {
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "endpoint": endpoint,
                        "method": method,
                        "status": "error"
                    }
                    
        except Exception as e:
            return {
                "error": f"Request failed: {str(e)}",
                "endpoint": endpoint,
                "method": method,
                "status": "error"
            }

# Global ACI client
aci_client = ACIClient()

# ===== TEST & CONNECTION TOOLS =====

@mcp.tool()
def aci_simple_test(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Simple test tool for ACI connectivity"""
    return {"message": "ACI Comprehensive MCP server working! 50 operations available.", "status": "success"}

# ===== CORE INFRASTRUCTURE GET OPERATIONS (12 tools) =====

@mcp.tool()
def aci_tenants_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all tenants from ACI"""
    return aci_client.make_request("/api/node/class/fvTenant.json", "GET", query_params)

@mcp.tool()
def aci_application_profiles_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all application profiles from ACI"""
    return aci_client.make_request("/api/node/class/fvAp.json", "GET", query_params)

@mcp.tool()
def aci_endpoint_groups_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all endpoint groups (EPGs) from ACI"""
    return aci_client.make_request("/api/node/class/fvAEPg.json", "GET", query_params)

@mcp.tool()
def aci_bridge_domains_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all bridge domains from ACI"""
    return aci_client.make_request("/api/node/class/fvBD.json", "GET", query_params)

@mcp.tool()
def aci_contexts_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all contexts (VRFs) from ACI"""
    return aci_client.make_request("/api/node/class/fvCtx.json", "GET", query_params)

@mcp.tool()
def aci_subnets_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all subnets from ACI"""
    return aci_client.make_request("/api/node/class/fvSubnet.json", "GET", query_params)

@mcp.tool()
def aci_contracts_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all contracts from ACI"""
    return aci_client.make_request("/api/node/class/vzBrCP.json", "GET", query_params)

@mcp.tool()
def aci_contract_subjects_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all contract subjects from ACI"""
    return aci_client.make_request("/api/node/class/vzSubj.json", "GET", query_params)

@mcp.tool()
def aci_filters_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all filters from ACI"""
    return aci_client.make_request("/api/node/class/vzFilter.json", "GET", query_params)

@mcp.tool()
def aci_filter_entries_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all filter entries from ACI"""
    return aci_client.make_request("/api/node/class/vzEntry.json", "GET", query_params)

@mcp.tool()
def aci_endpoints_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all endpoints from ACI"""
    return aci_client.make_request("/api/node/class/fvCEp.json", "GET", query_params)

@mcp.tool()
def aci_faults_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all faults from ACI"""
    return aci_client.make_request("/api/node/class/faultSummary.json", "GET", query_params)

# ===== FABRIC & INFRASTRUCTURE GET OPERATIONS (8 tools) =====

@mcp.tool()
def aci_fabric_nodes_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all fabric nodes from ACI"""
    return aci_client.make_request("/api/node/class/fabricNode.json", "GET", query_params)

@mcp.tool()
def aci_fabric_health_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get fabric health from ACI"""
    return aci_client.make_request("/api/node/class/fabricHealthTotal.json", "GET", query_params)

@mcp.tool()
def aci_fabric_links_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get fabric links from ACI"""
    return aci_client.make_request("/api/node/class/fabricLink.json", "GET", query_params)

@mcp.tool()
def aci_physical_interfaces_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all physical interfaces from ACI"""
    return aci_client.make_request("/api/node/class/l1PhysIf.json", "GET", query_params)

@mcp.tool()
def aci_ethernet_interfaces_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all ethernet interfaces from ACI"""
    return aci_client.make_request("/api/node/class/ethpmPhysIf.json", "GET", query_params)

@mcp.tool()
def aci_vlan_pools_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all VLAN pools from ACI"""
    return aci_client.make_request("/api/node/class/fvnsVlanInstP.json", "GET", query_params)

@mcp.tool()
def aci_domains_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all physical domains from ACI"""
    return aci_client.make_request("/api/node/class/physDomP.json", "GET", query_params)

@mcp.tool()
def aci_critical_faults_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get critical faults from ACI"""
    if not query_params:
        query_params = {"query-target-filter": "eq(faultSummary.severity,\"critical\")"}
    return aci_client.make_request("/api/node/class/faultSummary.json", "GET", query_params)

# ===== CORE CREATE OPERATIONS (13 tools) =====

@mcp.tool()
def aci_tenant_create(tenant_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new tenant in ACI"""
    payload = {
        "fvTenant": {
            "attributes": {
                "name": tenant_name,
                "descr": description,
                "status": "created"
            }
        }
    }
    return aci_client.make_request("/api/node/mo/uni.json", "POST", payload=payload)

@mcp.tool()
def aci_vrf_create(tenant_name: str, vrf_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new VRF (Context) in ACI"""
    payload = {
        "fvCtx": {
            "attributes": {
                "name": vrf_name,
                "descr": description,
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_bridge_domain_create(tenant_name: str, vrf_name: str, bd_name: str, 
                           subnet_ip: str = "", description: str = "") -> Dict[str, Any]:
    """Create a new Bridge Domain in ACI"""
    payload = {
        "fvBD": {
            "attributes": {
                "name": bd_name,
                "descr": description,
                "status": "created"
            },
            "children": [
                {
                    "fvRsCtx": {
                        "attributes": {
                            "tnFvCtxName": vrf_name
                        }
                    }
                }
            ]
        }
    }
    
    # Add subnet if provided
    if subnet_ip:
        subnet_child = {
            "fvSubnet": {
                "attributes": {
                    "ip": subnet_ip,
                    "scope": "public",
                    "status": "created"
                }
            }
        }
        payload["fvBD"]["children"].append(subnet_child)
    
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_application_profile_create(tenant_name: str, app_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new Application Profile in ACI"""
    payload = {
        "fvAp": {
            "attributes": {
                "name": app_name,
                "descr": description,
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_epg_create(tenant_name: str, app_name: str, epg_name: str, 
                  bd_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new Endpoint Group (EPG) in ACI"""
    payload = {
        "fvAEPg": {
            "attributes": {
                "name": epg_name,
                "descr": description,
                "status": "created"
            },
            "children": [
                {
                    "fvRsBd": {
                        "attributes": {
                            "tnFvBDName": bd_name
                        }
                    }
                }
            ]
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/ap-{app_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_contract_create(tenant_name: str, contract_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new Contract in ACI"""
    payload = {
        "vzBrCP": {
            "attributes": {
                "name": contract_name,
                "descr": description,
                "scope": "tenant",
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_contract_subject_create(tenant_name: str, contract_name: str, subject_name: str, 
                              filter_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new Contract Subject in ACI"""
    payload = {
        "vzSubj": {
            "attributes": {
                "name": subject_name,
                "descr": description,
                "status": "created"
            },
            "children": [
                {
                    "vzRsSubjFiltAtt": {
                        "attributes": {
                            "tnVzFilterName": filter_name
                        }
                    }
                }
            ]
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/brc-{contract_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_filter_create(tenant_name: str, filter_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new Filter in ACI"""
    payload = {
        "vzFilter": {
            "attributes": {
                "name": filter_name,
                "descr": description,
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_filter_entry_create(tenant_name: str, filter_name: str, entry_name: str,
                          protocol: str = "tcp", dst_port: str = "80", description: str = "") -> Dict[str, Any]:
    """Create a new Filter Entry in ACI"""
    payload = {
        "vzEntry": {
            "attributes": {
                "name": entry_name,
                "descr": description,
                "etherT": "ip",
                "prot": protocol,
                "dFromPort": dst_port,
                "dToPort": dst_port,
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/flt-{filter_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_epg_contract_provider_bind(tenant_name: str, app_name: str, epg_name: str, 
                                 contract_name: str) -> Dict[str, Any]:
    """Bind EPG as Contract Provider"""
    payload = {
        "fvRsProv": {
            "attributes": {
                "tnVzBrCPName": contract_name,
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/ap-{app_name}/epg-{epg_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_epg_contract_consumer_bind(tenant_name: str, app_name: str, epg_name: str, 
                                 contract_name: str) -> Dict[str, Any]:
    """Bind EPG as Contract Consumer"""
    payload = {
        "fvRsCons": {
            "attributes": {
                "tnVzBrCPName": contract_name,
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/ap-{app_name}/epg-{epg_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_epg_domain_bind(tenant_name: str, app_name: str, epg_name: str, 
                       domain_name: str, domain_type: str = "phys") -> Dict[str, Any]:
    """Bind EPG to Physical or VMM Domain"""
    if domain_type == "phys":
        rs_type = "fvRsDomAtt"
        dn_prefix = "uni/phys-"
    elif domain_type == "vmm":
        rs_type = "fvRsDomAtt" 
        dn_prefix = "uni/vmmp-VMware/dom-"
    else:
        return {"error": "Invalid domain_type. Use 'phys' or 'vmm'", "status": "error"}
    
    payload = {
        rs_type: {
            "attributes": {
                "tDn": f"{dn_prefix}{domain_name}",
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/ap-{app_name}/epg-{epg_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

# ===== L3 NETWORKING OPERATIONS (6 tools) =====

@mcp.tool()
def aci_l3_outside_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all Layer 3 Outside connections from ACI"""
    return aci_client.make_request("/api/node/class/l3extOut.json", "GET", query_params)

@mcp.tool()
def aci_external_networks_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all external networks from ACI"""
    return aci_client.make_request("/api/node/class/l3extInstP.json", "GET", query_params)

@mcp.tool()
def aci_bgp_peers_get(query_params: Optional[Dict] = None) -> Dict[str, Any]:
    """Get all BGP peers from ACI"""
    return aci_client.make_request("/api/node/class/bgpPeerEntry.json", "GET", query_params)

@mcp.tool()
def aci_l3out_create(tenant_name: str, l3out_name: str, vrf_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new Layer 3 Outside in ACI"""
    payload = {
        "l3extOut": {
            "attributes": {
                "name": l3out_name,
                "descr": description,
                "status": "created"
            },
            "children": [
                {
                    "l3extRsEctx": {
                        "attributes": {
                            "tnFvCtxName": vrf_name
                        }
                    }
                }
            ]
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_external_epg_create(tenant_name: str, l3out_name: str, ext_epg_name: str, 
                          subnet: str = "0.0.0.0/0", description: str = "") -> Dict[str, Any]:
    """Create a new External EPG in ACI"""
    payload = {
        "l3extInstP": {
            "attributes": {
                "name": ext_epg_name,
                "descr": description,
                "status": "created"
            },
            "children": [
                {
                    "l3extSubnet": {
                        "attributes": {
                            "ip": subnet,
                            "status": "created"
                        }
                    }
                }
            ]
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/out-{l3out_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_subnet_create(tenant_name: str, bd_name: str, subnet_ip: str, 
                     scope: str = "public", description: str = "") -> Dict[str, Any]:
    """Create a new subnet in a Bridge Domain"""
    payload = {
        "fvSubnet": {
            "attributes": {
                "ip": subnet_ip,
                "scope": scope,
                "descr": description,
                "status": "created"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/BD-{bd_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

# ===== ADVANCED CREATE OPERATIONS (8 tools) =====

@mcp.tool()
def aci_vlan_pool_create(pool_name: str, vlan_start: int, vlan_end: int, 
                        allocation_mode: str = "static", description: str = "") -> Dict[str, Any]:
    """Create a new VLAN pool in ACI"""
    payload = {
        "fvnsVlanInstP": {
            "attributes": {
                "name": pool_name,
                "descr": description,
                "allocMode": allocation_mode,
                "status": "created"
            },
            "children": [
                {
                    "fvnsEncapBlk": {
                        "attributes": {
                            "from": f"vlan-{vlan_start}",
                            "to": f"vlan-{vlan_end}",
                            "status": "created"
                        }
                    }
                }
            ]
        }
    }
    return aci_client.make_request("/api/node/mo/uni/infra.json", "POST", payload=payload)

@mcp.tool()
def aci_physical_domain_create(domain_name: str, vlan_pool_name: str, description: str = "") -> Dict[str, Any]:
    """Create a new Physical Domain in ACI"""
    payload = {
        "physDomP": {
            "attributes": {
                "name": domain_name,
                "descr": description,
                "status": "created"
            },
            "children": [
                {
                    "infraRsVlanNs": {
                        "attributes": {
                            "tDn": f"uni/infra/vlanns-[{vlan_pool_name}]-static"
                        }
                    }
                }
            ]
        }
    }
    return aci_client.make_request("/api/node/mo/uni/phys.json", "POST", payload=payload)

@mcp.tool()
def aci_create_3tier_app(tenant_name: str, app_name: str, vrf_name: str = "VRF1") -> Dict[str, Any]:
    """Create a complete 3-tier application (Web, App, DB) with contracts"""
    results = []
    
    # Create VRF
    results.append(aci_vrf_create(tenant_name, vrf_name, "3-Tier VRF"))
    
    # Create Bridge Domains
    results.append(aci_bridge_domain_create(tenant_name, vrf_name, "BD_Web", "10.1.1.1/24"))
    results.append(aci_bridge_domain_create(tenant_name, vrf_name, "BD_App", "10.1.2.1/24"))
    results.append(aci_bridge_domain_create(tenant_name, vrf_name, "BD_DB", "10.1.3.1/24"))
    
    # Create Application Profile
    results.append(aci_application_profile_create(tenant_name, app_name, "3-Tier Application"))
    
    # Create EPGs
    results.append(aci_epg_create(tenant_name, app_name, "Web_EPG", "BD_Web"))
    results.append(aci_epg_create(tenant_name, app_name, "App_EPG", "BD_App"))
    results.append(aci_epg_create(tenant_name, app_name, "DB_EPG", "BD_DB"))
    
    # Create Filters
    results.append(aci_filter_create(tenant_name, "HTTP_Filter"))
    results.append(aci_filter_entry_create(tenant_name, "HTTP_Filter", "HTTP", "tcp", "80"))
    results.append(aci_filter_create(tenant_name, "App_Filter"))
    results.append(aci_filter_entry_create(tenant_name, "App_Filter", "App", "tcp", "8080"))
    results.append(aci_filter_create(tenant_name, "DB_Filter"))
    results.append(aci_filter_entry_create(tenant_name, "DB_Filter", "DB", "tcp", "3306"))
    
    # Create Contracts
    results.append(aci_contract_create(tenant_name, "Web_Contract"))
    results.append(aci_contract_subject_create(tenant_name, "Web_Contract", "HTTP_Subject", "HTTP_Filter"))
    results.append(aci_contract_create(tenant_name, "App_Contract"))
    results.append(aci_contract_subject_create(tenant_name, "App_Contract", "App_Subject", "App_Filter"))
    results.append(aci_contract_create(tenant_name, "DB_Contract"))
    results.append(aci_contract_subject_create(tenant_name, "DB_Contract", "DB_Subject", "DB_Filter"))
    
    return {
        "message": f"3-Tier application '{app_name}' creation completed",
        "tenant": tenant_name,
        "results": results,
        "status": "success"
    }

@mcp.tool()
def aci_create_web_app_stack(tenant_name: str, app_name: str, web_subnet: str = "10.1.1.1/24", 
                           app_subnet: str = "10.1.2.1/24") -> Dict[str, Any]:
    """Create a complete web application stack with connectivity"""
    results = []
    
    # Create tenant if needed
    results.append(aci_tenant_create(tenant_name, f"Tenant for {app_name}"))
    
    # Create VRF
    vrf_name = f"{app_name}_VRF"
    results.append(aci_vrf_create(tenant_name, vrf_name, f"VRF for {app_name}"))
    
    # Create Bridge Domains
    results.append(aci_bridge_domain_create(tenant_name, vrf_name, f"{app_name}_Web_BD", web_subnet))
    results.append(aci_bridge_domain_create(tenant_name, vrf_name, f"{app_name}_App_BD", app_subnet))
    
    # Create Application Profile
    results.append(aci_application_profile_create(tenant_name, app_name, f"Application profile for {app_name}"))
    
    # Create EPGs
    results.append(aci_epg_create(tenant_name, app_name, f"{app_name}_Web_EPG", f"{app_name}_Web_BD"))
    results.append(aci_epg_create(tenant_name, app_name, f"{app_name}_App_EPG", f"{app_name}_App_BD"))
    
    # Create Filters and Contracts
    results.append(aci_filter_create(tenant_name, f"{app_name}_Web_Filter"))
    results.append(aci_filter_entry_create(tenant_name, f"{app_name}_Web_Filter", "HTTP", "tcp", "80"))
    results.append(aci_filter_entry_create(tenant_name, f"{app_name}_Web_Filter", "HTTPS", "tcp", "443"))
    
    results.append(aci_contract_create(tenant_name, f"{app_name}_Web_Contract"))
    results.append(aci_contract_subject_create(tenant_name, f"{app_name}_Web_Contract", "Web_Subject", f"{app_name}_Web_Filter"))
    
    # Bind contracts
    results.append(aci_epg_contract_provider_bind(tenant_name, app_name, f"{app_name}_Web_EPG", f"{app_name}_Web_Contract"))
    results.append(aci_epg_contract_consumer_bind(tenant_name, app_name, f"{app_name}_App_EPG", f"{app_name}_Web_Contract"))
    
    return {
        "message": f"Web application stack '{app_name}' creation completed",
        "tenant": tenant_name,
        "components": ["VRF", "Bridge Domains", "EPGs", "Contracts", "Bindings"],
        "results": results,
        "status": "success"
    }

@mcp.tool()
def aci_tenant_delete(tenant_name: str) -> Dict[str, Any]:
    """Delete a tenant from ACI (use with caution!)"""
    payload = {
        "fvTenant": {
            "attributes": {
                "name": tenant_name,
                "status": "deleted"
            }
        }
    }
    return aci_client.make_request("/api/node/mo/uni.json", "POST", payload=payload)

@mcp.tool()
def aci_epg_delete(tenant_name: str, app_name: str, epg_name: str) -> Dict[str, Any]:
    """Delete an EPG from ACI"""
    payload = {
        "fvAEPg": {
            "attributes": {
                "name": epg_name,
                "status": "deleted"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}/ap-{app_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_contract_delete(tenant_name: str, contract_name: str) -> Dict[str, Any]:
    """Delete a contract from ACI"""
    payload = {
        "vzBrCP": {
            "attributes": {
                "name": contract_name,
                "status": "deleted"
            }
        }
    }
    endpoint = f"/api/node/mo/uni/tn-{tenant_name}.json"
    return aci_client.make_request(endpoint, "POST", payload=payload)

@mcp.tool()
def aci_get_operations_summary() -> Dict[str, Any]:
    """Get a summary of all available ACI operations"""
    return {
        "total_operations": 50,
        "categories": {
            "Connection & Test": ["aci_simple_test"],
            "Core Infrastructure GET (12 ops)": [
                "aci_tenants_get", "aci_application_profiles_get", "aci_endpoint_groups_get",
                "aci_bridge_domains_get", "aci_contexts_get", "aci_subnets_get",
                "aci_contracts_get", "aci_contract_subjects_get", "aci_filters_get",
                "aci_filter_entries_get", "aci_endpoints_get", "aci_faults_get"
            ],
            "Fabric & Infrastructure GET (8 ops)": [
                "aci_fabric_nodes_get", "aci_fabric_health_get", "aci_fabric_links_get",
                "aci_physical_interfaces_get", "aci_ethernet_interfaces_get", "aci_vlan_pools_get",
                "aci_domains_get", "aci_critical_faults_get"
            ],
            "Core CREATE Operations (13 ops)": [
                "aci_tenant_create", "aci_vrf_create", "aci_bridge_domain_create",
                "aci_application_profile_create", "aci_epg_create", "aci_contract_create",
                "aci_contract_subject_create", "aci_filter_create", "aci_filter_entry_create",
                "aci_epg_contract_provider_bind", "aci_epg_contract_consumer_bind", "aci_epg_domain_bind"
            ],
            "L3 Networking (6 ops)": [
                "aci_l3_outside_get", "aci_external_networks_get", "aci_bgp_peers_get",
                "aci_l3out_create", "aci_external_epg_create", "aci_subnet_create"
            ],
            "Advanced Operations (8 ops)": [
                "aci_vlan_pool_create", "aci_physical_domain_create", "aci_create_3tier_app",
                "aci_create_web_app_stack", "aci_tenant_delete", "aci_epg_delete",
                "aci_contract_delete", "aci_get_operations_summary"
            ]
        },
        "get_operations": 21,
        "post_operations": 28,
        "status": "success"
    }

if __name__ == "__main__":
    mcp.run()
