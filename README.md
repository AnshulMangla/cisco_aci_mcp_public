<h1 align="center">Community MCP Server for Cisco ACI<br /><br /></h1>

<div align="center">
<img src="https://img.shields.io/badge/Cisco-ACI-049fd9?style=flat-square&logo=cisco&logoColor=white" alt="Cisco ACI">
<img src="https://img.shields.io/badge/MCP-Protocol-000000?style=flat-square&logo=anthropic&logoColor=white" alt="MCP">
<img src="https://img.shields.io/badge/FastMCP-Library-7B2CBF?style=flat-square&logo=python&logoColor=white" alt="FastMCP">
<img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
</div>

<br />

<div align="center">
A <strong>stand-alone MCP server</strong> built with <a href="https://github.com/jlowin/fastmcp"><strong>FastMCP</strong></a> that exposes <strong>50 ACI operations</strong> as MCP tools. Connect any <strong>MCP-compatible client</strong> and <strong>LLM</strong> to query, provision, and manage your Cisco ACI fabric through natural language.
</div>

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Available MCP Tools](#available-mcp-tools)
5. [Available Transport Options](#available-transport-options)
6. [Installation](#installation)
7. [Authentication](#authentication)
8. [Running the Server](#running-the-server)
9. [Usage Example: VS Code](#usage-example-vs-code)

---

## Overview

This MCP server acts as a lightweight middleware layer between **Cisco ACI (Application Centric Infrastructure)** and any **MCP-compatible client**. It allows an LLM to query the ACI fabric, inspect tenants, EPGs, bridge domains, faults, and fabric health — and to create or delete policy objects — all through structured MCP tools.

This is a community based project and is not officially supported by any Cisco Business or Technical entity.

The server communicates with the APIC REST API using cookie-based authentication and supports 50 operations covering the full ACI policy model.

---

## Features

- **Plug-and-play** — works with any MCP-compatible client (VS Code Copilot, Claude Desktop, N8N, etc.)
- **50 ACI operations** — GET and POST across tenants, EPGs, BDs, VRFs, contracts, fabric nodes, and more
- **Fabric health & faults** — query fault summaries, critical faults, and node health in one call
- **Auto re-authentication** — transparently refreshes the APIC session on token expiry
- **Composite operations** — single-tool commands to deploy a full 3-tier application or web stack
- **No hardcoded credentials** — all secrets sourced from a `.env` file
- **Fully type-hinted tools** for clarity and extensibility

---

## Requirements

- Python 3.13+
- Access to a Cisco APIC (on-premises or sandbox)
- An APIC user with read and/or write privileges

**Python dependencies** (`requirements.txt`):

| Package | Purpose |
|---------|---------|
| `fastmcp` | MCP server framework |
| `httpx` | Async-capable HTTP client for APIC API calls |
| `python-dotenv` | Load credentials from `.env` |
| `pydantic` | Data validation |
| `requests` | Supplementary HTTP support |

---

## Available MCP Tools

### Connection & Test (1 tool)

| Tool | Description |
|------|-------------|
| `aci_simple_test()` | Verify connectivity to the MCP server |

### Core Infrastructure — GET (12 tools)

| Tool | Description |
|------|-------------|
| `aci_tenants_get()` | List all tenants |
| `aci_application_profiles_get()` | List all application profiles |
| `aci_endpoint_groups_get()` | List all EPGs |
| `aci_bridge_domains_get()` | List all bridge domains |
| `aci_contexts_get()` | List all VRFs |
| `aci_subnets_get()` | List all subnets |
| `aci_contracts_get()` | List all contracts |
| `aci_contract_subjects_get()` | List all contract subjects |
| `aci_filters_get()` | List all filters |
| `aci_filter_entries_get()` | List all filter entries |
| `aci_endpoints_get()` | List all learned endpoints |
| `aci_faults_get()` | List all faults (fault summary) |

### Fabric & Infrastructure — GET (8 tools)

| Tool | Description |
|------|-------------|
| `aci_fabric_nodes_get()` | List all fabric nodes (leaves, spines, APICs) |
| `aci_fabric_health_get()` | Get overall fabric health score |
| `aci_fabric_links_get()` | List all fabric links |
| `aci_physical_interfaces_get()` | List all physical interfaces |
| `aci_ethernet_interfaces_get()` | List all ethernet interface states |
| `aci_vlan_pools_get()` | List all VLAN pools |
| `aci_domains_get()` | List all physical domains |
| `aci_critical_faults_get()` | List only critical-severity faults |

### Core Policy — CREATE (13 tools)

| Tool | Parameters | Description |
|------|-----------|-------------|
| `aci_tenant_create` | `tenant_name`, `description?` | Create a new tenant |
| `aci_vrf_create` | `tenant_name`, `vrf_name`, `description?` | Create a VRF |
| `aci_bridge_domain_create` | `tenant_name`, `vrf_name`, `bd_name`, `subnet_ip?` | Create a bridge domain |
| `aci_application_profile_create` | `tenant_name`, `app_name`, `description?` | Create an application profile |
| `aci_epg_create` | `tenant_name`, `app_name`, `epg_name`, `bd_name` | Create an EPG |
| `aci_contract_create` | `tenant_name`, `contract_name`, `description?` | Create a contract |
| `aci_contract_subject_create` | `tenant_name`, `contract_name`, `subject_name`, `filter_name` | Create a contract subject |
| `aci_filter_create` | `tenant_name`, `filter_name`, `description?` | Create a filter |
| `aci_filter_entry_create` | `tenant_name`, `filter_name`, `entry_name`, `protocol?`, `dst_port?` | Create a filter entry |
| `aci_epg_contract_provider_bind` | `tenant_name`, `app_name`, `epg_name`, `contract_name` | Bind EPG as contract provider |
| `aci_epg_contract_consumer_bind` | `tenant_name`, `app_name`, `epg_name`, `contract_name` | Bind EPG as contract consumer |
| `aci_epg_domain_bind` | `tenant_name`, `app_name`, `epg_name`, `domain_name`, `domain_type?` | Attach EPG to physical or VMM domain |
| `aci_subnet_create` | `tenant_name`, `bd_name`, `subnet_ip`, `scope?` | Add a subnet to a bridge domain |

### L3 Networking (6 tools)

| Tool | Description |
|------|-------------|
| `aci_l3_outside_get()` | List all L3Outs |
| `aci_external_networks_get()` | List all external EPGs |
| `aci_bgp_peers_get()` | List all BGP peers |
| `aci_l3out_create` | Create a new L3Out |
| `aci_external_epg_create` | Create an external EPG under an L3Out |

### Advanced / Composite Operations (8 tools)

| Tool | Description |
|------|-------------|
| `aci_vlan_pool_create` | Create a VLAN pool with encap block |
| `aci_physical_domain_create` | Create a physical domain and attach a VLAN pool |
| `aci_create_3tier_app` | Deploy a complete 3-tier app (Web/App/DB) with BDs, EPGs, filters, contracts |
| `aci_create_web_app_stack` | Deploy a web + app stack end-to-end |
| `aci_tenant_delete` | Delete a tenant (use with caution) |
| `aci_epg_delete` | Delete an EPG |
| `aci_contract_delete` | Delete a contract |
| `aci_get_operations_summary` | Return a structured list of all 50 operations |

---

## Available Transport Options

| Mode | Description |
|------|-------------|
| `stdio` | Standard I/O — for local clients managed by VS Code, Claude Desktop, etc. |

The server in `scripts/server.py` runs in **stdio** mode. VS Code manages the process lifecycle automatically via `mcp.json`.

---

## Installation

Clone the repository and run the interactive setup script:

```bash
git clone <your-repo-url>
cd aci_mcp_devnet_submission
./setup.sh
```

The `setup.sh` script will:
1. Prompt for your APIC URL, username, and password
2. Write the credentials to `scripts/.env`
3. Install all Python dependencies via `pip`
4. Print instructions for starting the server

Alternatively, set up manually:

```bash
cd aci_mcp_devnet_submission
pip install -r requirements.txt

# Create scripts/.env manually:
cat > scripts/.env <<EOF
APIC_URL=https://<your-apic-ip>/
USERNAME=<your-username>
PASSWORD=<your-password>
EOF
```

---

## Authentication

The server authenticates to the APIC using cookie-based session authentication (`aaaLogin`). Credentials are loaded from `scripts/.env` at startup.

**`scripts/.env` format:**

```bash
APIC_URL=https://10.x.x.x/
USERNAME=admin
PASSWORD=yourpassword
```

The server automatically re-authenticates when the APIC session token expires (HTTP 403), so long-running sessions stay connected without manual intervention.

> **Security note:** The `scripts/.env` file is listed in `.gitignore` — never commit real credentials to source control.

---

## Running the Server

### Method 1: Direct Python (recommended)

```bash
cd scripts
python3 server.py
```

### Method 2: Via setup.sh (first-time setup + run)

```bash
cd aci_mcp_devnet_submission
./setup.sh
# Follow prompts, then:
cd scripts && python3 server.py
```

### Method 3: FastMCP dev mode (auto-reload on file changes)

```bash
cd scripts
fastmcp dev server.py
```

---

## Usage Example: VS Code

**GitHub Copilot in VS Code 2** has a built-in MCP client. Add the ACI MCP server to your VS Code `mcp.json` to use it directly from the Copilot chat window.

### Step 1 — Add to mcp.json

Open your VS Code user `mcp.json` (`Cmd+Shift+P` → *Open MCP Servers Configuration*) and add:

```json
{
  "servers": {
    "my-aci-mcp-server": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/absolute/path/to/aci_mcp_devnet_submission/scripts/server.py"
      ]
    }
  }
}
```

> Replace `/absolute/path/to/` with the actual path on your machine.

### Step 2 — Start the Server

VS Code starts the server automatically when you open a Copilot chat session. You can also manually start/restart it from the MCP panel in the VS Code status bar.

### Step 3 — Chat with your ACI Fabric

Open **GitHub Copilot Chat** (`Cmd+Shift+I`) and try natural language prompts:

**📋 Query the fabric:**
```
Show me all faults in the fabric
```
```
List the top 10 tenants
```
```
What is the current fabric health score?
```

**🏗️ Provision policy:**
```
Create a new tenant called "MyApp_Tenant"
```
```
Deploy a 3-tier application called "ECommerceApp" in tenant "Prod_Tenant"
```
```
Add a subnet 192.168.10.1/24 to bridge domain "app_bd" in tenant "Prod_Tenant"
```

**🩺 Troubleshoot:**
```
Show me all critical faults
```
```
Get all BGP peers in the fabric
```
```
List all endpoints currently learned in the fabric
```

The LLM will automatically select the right MCP tool(s), call the APIC REST API, and return structured results in the chat window.

---


