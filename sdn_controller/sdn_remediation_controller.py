"""
sdn_remediation_controller.py

Consumes an AI-generated fault alert (post NS-3/GNS3 validation), compiles
it into a concrete SDN policy, and pushes it via the OpenDaylight/ONOS
REST API. Designed to be invoked only after Layer 4's QoS/SLA feasibility
gate has approved the candidate action.
"""

import requests
from dataclasses import dataclass
from enum import Enum


class RemediationAction(Enum):
    REROUTE = "reroute"
    THROTTLE = "throttle"
    ISOLATE = "isolate"


@dataclass
class RemediationIntent:
    action: RemediationAction
    target_device_id: str
    target_interface: str | None = None
    alternate_path: list[str] | None = None
    throttle_rate_mbps: float | None = None
    predicted_fault_class: str = ""
    confidence: float = 0.0


class SDNController:
    def __init__(self, base_url: str, auth: tuple[str, str], controller: str = "onos"):
        self.base_url = base_url.rstrip("/")
        self.auth = auth
        self.controller = controller  # "onos" or "opendaylight"

    def _headers(self):
        return {"Content-Type": "application/json"}

    def reroute_flow(self, device_id: str, alternate_path: list[str]) -> dict:
        """Install a new flow rule directing traffic along a validated
        alternate path, bypassing the predicted-failing link/device."""
        payload = {
            "deviceId": device_id,
            "treatment": {"path": alternate_path},
            "priority": 40000,
            "isPermanent": True,
        }
        endpoint = f"{self.base_url}/onos/v1/flows/{device_id}" \
            if self.controller == "onos" \
            else f"{self.base_url}/restconf/config/opendaylight-inventory:nodes/node/{device_id}/flow-node-inventory:table/0/flow"
        resp = requests.post(endpoint, json=payload, auth=self.auth,
                              headers=self._headers(), timeout=5)
        resp.raise_for_status()
        return resp.json() if resp.content else {"status": "accepted"}

    def throttle_link(self, device_id: str, interface: str, rate_mbps: float) -> dict:
        """Apply a metered rate-limit to a degraded interface to relieve
        queue pressure while a permanent fix is planned/validated."""
        payload = {
            "deviceId": device_id,
            "port": interface,
            "meter": {"rate": rate_mbps, "unit": "MBPS", "burst": True},
        }
        endpoint = f"{self.base_url}/onos/v1/meters/{device_id}"
        resp = requests.post(endpoint, json=payload, auth=self.auth,
                              headers=self._headers(), timeout=5)
        resp.raise_for_status()
        return resp.json() if resp.content else {"status": "accepted"}

    def isolate_device(self, device_id: str) -> dict:
        """Administratively shut down all forwarding through a device
        predicted to be failing catastrophically (e.g., loop, security event)."""
        endpoint = f"{self.base_url}/onos/v1/devices/{device_id}/isolate"
        resp = requests.post(endpoint, auth=self.auth,
                              headers=self._headers(), timeout=5)
        resp.raise_for_status()
        return resp.json() if resp.content else {"status": "accepted"}

    def execute(self, intent: RemediationIntent) -> dict:
        if intent.action == RemediationAction.REROUTE:
            assert intent.alternate_path, "Reroute requires a validated alternate_path"
            return self.reroute_flow(intent.target_device_id, intent.alternate_path)
        elif intent.action == RemediationAction.THROTTLE:
            assert intent.throttle_rate_mbps, "Throttle requires a target rate"
            return self.throttle_link(intent.target_device_id,
                                       intent.target_interface, intent.throttle_rate_mbps)
        elif intent.action == RemediationAction.ISOLATE:
            return self.isolate_device(intent.target_device_id)
        raise ValueError(f"Unsupported action: {intent.action}")


def handle_validated_alert(intent: RemediationIntent, controller: SDNController) -> None:
    """Entry point invoked by Layer 4 once NS-3/GNS3 + SLA gate approves
    the candidate action."""
    print(f"[SDN] Executing {intent.action.value} on {intent.target_device_id} "
          f"(fault={intent.predicted_fault_class}, confidence={intent.confidence:.2f})")
    result = controller.execute(intent)
    print(f"[SDN] Controller response: {result}")


if __name__ == "__main__":
    # Example usage
    controller = SDNController(
        base_url="http://onos-controller.campus.local:8181",
        auth=("onos", "rocks"),
        controller="onos",
    )
    validated_intent = RemediationIntent(
        action=RemediationAction.REROUTE,
        target_device_id="sw-dist-14",
        alternate_path=["sw-dist-14", "sw-core-02", "sw-dist-09"],
        predicted_fault_class="congestion_collapse",
        confidence=0.94,
    )
    # handle_validated_alert(validated_intent, controller)
