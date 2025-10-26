#!/usr/bin/env bash
set -euo pipefail

# Usage: sudo ./autogw.sh [iface]
# If iface is provided, script will try to find a gateway for that iface.
# If no iface provided, it probes the route to 8.8.8.8 to discover iface+gateway.

target_iface="${1:-}"

# helper to find gateway+iface by probing a route to a public IP
probe_route() {
  # ip route get prints something like:
  # 8.8.8.8 via 192.168.68.1 dev wlan1 src 192.168.68.102 ...
  ip route get 8.8.8.8 2>/dev/null || return 1
}

# find gateway+iface
if [[ -n "$target_iface" ]]; then
  # try to find a gateway for that interface from routing table
  gateway=$(ip route show | awk -v IF="$target_iface" '$0 ~ "dev "IF && $0 ~ /via/ {for(i=1;i<=NF;i++) if($i=="via") {print $(i+1); exit}}')
  iface="$target_iface"
  # fallback: probe route and check that probed iface matches requested iface
  if [[ -z "$gateway" ]]; then
    if probe_route >/dev/null 2>&1; then
      probed_gateway=$(ip route get 8.8.8.8 | awk '/via/ {for(i=1;i<=NF;i++) if($i=="via") print $(i+1)}')
      probed_iface=$(ip route get 8.8.8.8 | awk '/dev/ {for(i=1;i<=NF;i++) if($i=="dev") print $(i+1)}')
      if [[ "$probed_iface" == "$target_iface" ]]; then
        gateway="$probed_gateway"
      fi
    fi
  fi
else
  # auto-detect via probing a route to 8.8.8.8
  if ! probe_route >/dev/null 2>&1; then
    echo "Error: unable to probe route. Is networking up?" >&2
    exit 2
  fi
  gateway=$(ip route get 8.8.8.8 | awk '/via/ {for(i=1;i<=NF;i++) if($i=="via") print $(i+1)}')
  iface=$(ip route get 8.8.8.8 | awk '/dev/ {for(i=1;i<=NF;i++) if($i=="dev") print $(i+1)}')
fi

if [[ -z "${gateway:-}" || -z "${iface:-}" ]]; then
  echo "Failed to detect gateway and/or interface." >&2
  echo "Detected gateway: '${gateway:-}' interface: '${iface:-}'" >&2
  exit 3
fi

echo "Detected gateway: $gateway  interface: $iface"
echo "Removing existing default route (if any)..."
# safe delete: ignore failure if there is no default route
sudo ip route del default 2>/dev/null || true

echo "Adding default route via $gateway dev $iface ..."
sudo ip route add default via "$gateway" dev "$iface"

echo "Done. Current default route:"
ip route show default || true
