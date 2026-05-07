#!/usr/bin/env bash
# ============================================================
# ACI MCP Server - Setup Script
# Prompts for APIC credentials, writes scripts/.env,
# installs Python dependencies, and prints run instructions.
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/scripts/.env"

echo ""
echo "=================================================="
echo "  ACI MCP Server - Environment Setup"
echo "=================================================="
echo ""

# ---- Prompt for APIC URL --------------------------------
read -rp "Enter APIC URL (e.g. https://10.x.x.x): " APIC_URL
if [[ -z "$APIC_URL" ]]; then
  echo "ERROR: APIC URL cannot be empty." >&2
  exit 1
fi

# ---- Prompt for username --------------------------------
read -rp "Enter APIC username: " APIC_USERNAME
if [[ -z "$APIC_USERNAME" ]]; then
  echo "ERROR: Username cannot be empty." >&2
  exit 1
fi

# ---- Prompt for password (hidden) -----------------------
read -rsp "Enter APIC password: " APIC_PASSWORD
echo ""
if [[ -z "$APIC_PASSWORD" ]]; then
  echo "ERROR: Password cannot be empty." >&2
  exit 1
fi

# ---- Write .env -----------------------------------------
cat > "$ENV_FILE" <<EOF
APIC_URL=${APIC_URL}
USERNAME=${APIC_USERNAME}
PASSWORD=${APIC_PASSWORD}
EOF

echo ""
echo "[✓] Configuration written to scripts/.env"

# ---- Install dependencies -------------------------------
echo ""
echo "[*] Installing Python dependencies from requirements.txt ..."
pip install -r "$SCRIPT_DIR/requirements.txt" --quiet

echo "[✓] Dependencies installed."

# ---- Done -----------------------------------------------
echo ""
echo "=================================================="
echo "  Setup complete! To start the MCP server run:"
echo ""
echo "    cd scripts"
echo "    python3 server.py"
echo ""
echo "  Or add it to VS Code mcp.json:"
echo "    \"command\": \"python3\","
echo "    \"args\": [\"$(pwd)/scripts/server.py\"]"
echo "=================================================="
echo ""
