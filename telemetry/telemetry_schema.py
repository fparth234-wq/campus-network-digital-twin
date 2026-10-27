"""
telemetry_schema.py

Defines standard schemas and parsing utilities for incoming telemetry.
"""
import json
from dataclasses import dataclass, asdict

@dataclass
class TelemetryEvent:
    event_id: str
    timestamp: str
    source_device_id: str
    source_role: str
    source_vendor: str
    if_index: int
    if_name: str
    adjacent_device_id: str
    utilization_pct: float
    if_in_errors: int
    if_out_errors: int
    queue_depth_pct: float
    drop_rate_pps: float
    sequence_number: int
    rssi_dbm: float = None

    def to_json_ld(self):
        return {
            "@context": "https://ndt.campus-net.org/schema/v1",
            "@type": "TelemetryEvent",
            "eventId": self.event_id,
            "timestamp": self.timestamp,
            "sourceDevice": {
                "@type": "NetworkEntity",
                "deviceId": self.source_device_id,
                "role": self.source_role,
                "vendor": self.source_vendor
            },
            "interface": {
                "@type": "InterfaceEntity",
                "ifIndex": self.if_index,
                "ifName": self.if_name,
                "adjacentDeviceId": self.adjacent_device_id
            },
            "metrics": {
                "utilizationPct": self.utilization_pct,
                "ifInErrors": self.if_in_errors,
                "ifOutErrors": self.if_out_errors,
                "queueDepthPct": self.queue_depth_pct,
                "dropRatePps": self.drop_rate_pps,
                "rssiDbm": self.rssi_dbm
            },
            "telemetrySource": "SNMP/NetFlow",
            "sequenceNumber": self.sequence_number
        }
