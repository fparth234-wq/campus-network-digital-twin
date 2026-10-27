"""
neo4j_client.py

Synchronizes normalized telemetry events (JSON-LD) into the Neo4j
Digital Twin graph with real-time cypher queries.
"""
from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)

class Neo4jTwinSynchronizer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def sync_telemetry_event(self, event: dict):
        """
        Takes a parsed JSON-LD telemetry event and updates the Neo4j graph.
        Targeting <= 50ms sync latency.
        """
        query = """
        // 1. Upsert the source device node
        MERGE (d:NetworkEntity {deviceId: $sourceDeviceId})
          ON CREATE SET d.role = $role, d.vendor = $vendor, d.firstSeen = $timestamp
          SET d.lastSeen = $timestamp

        // 2. Upsert the interface node
        MERGE (i:InterfaceEntity {deviceId: $sourceDeviceId, ifIndex: $ifIndex})
          ON CREATE SET i.ifName = $ifName
          SET i.utilizationPct = $utilizationPct,
              i.ifInErrors     = $ifInErrors,
              i.ifOutErrors    = $ifOutErrors,
              i.queueDepthPct  = $queueDepthPct,
              i.dropRatePps    = $dropRatePps,
              i.updatedAt      = $timestamp

        // 3. Ensure the interface is linked to its owning device
        MERGE (d)-[:HAS_INTERFACE]->(i)

        // 4. Upsert the adjacency edge (link)
        MERGE (adj:NetworkEntity {deviceId: $adjacentDeviceId})
        MERGE (i)-[l:LINKED_TO]->(adj)
          SET l.utilizationPct = $utilizationPct,
              l.dropRatePps     = $dropRatePps,
              l.lastUpdated      = $timestamp

        // 5. Append an immutable event record
        CREATE (:TelemetryEvent {
          eventId: $eventId,
          deviceId: $sourceDeviceId,
          ifIndex: $ifIndex,
          timestamp: $timestamp,
          utilizationPct: $utilizationPct,
          dropRatePps: $dropRatePps,
          sequenceNumber: $sequenceNumber
        })
        """
        
        # Extract fields from JSON-LD dict
        params = {
            "sourceDeviceId": event["sourceDevice"]["deviceId"],
            "role": event["sourceDevice"].get("role", "unknown"),
            "vendor": event["sourceDevice"].get("vendor", "unknown"),
            "timestamp": event["timestamp"],
            
            "ifIndex": event["interface"]["ifIndex"],
            "ifName": event["interface"].get("ifName", f"Interface-{event['interface']['ifIndex']}"),
            "adjacentDeviceId": event["interface"].get("adjacentDeviceId", "unknown"),
            
            "utilizationPct": event["metrics"]["utilizationPct"],
            "ifInErrors": event["metrics"]["ifInErrors"],
            "ifOutErrors": event["metrics"]["ifOutErrors"],
            "queueDepthPct": event["metrics"]["queueDepthPct"],
            "dropRatePps": event["metrics"]["dropRatePps"],
            
            "eventId": event["eventId"],
            "sequenceNumber": event.get("sequenceNumber", 0),
        }
        
        with self.driver.session() as session:
            session.run(query, **params)
            logger.debug(f"Synced telemetry event {event['eventId']} for device {params['sourceDeviceId']}")

if __name__ == "__main__":
    # Example usage
    event = {
        "@context": "https://ndt.campus-net.org/schema/v1",
        "@type": "TelemetryEvent",
        "eventId": "evt-2f9a1c7e-0af1",
        "timestamp": "2026-09-08T10:15:32.412Z",
        "sourceDevice": {
            "@type": "NetworkEntity",
            "deviceId": "sw-dist-14",
            "role": "distribution-switch",
            "vendor": "generic-ofswitch"
        },
        "interface": {
            "@type": "InterfaceEntity",
            "ifIndex": 24,
            "ifName": "GigabitEthernet0/24",
            "adjacentDeviceId": "sw-access-27"
        },
        "metrics": {
            "utilizationPct": 92.4,
            "ifInErrors": 148,
            "ifOutErrors": 3,
            "queueDepthPct": 87.1,
            "dropRatePps": 220.5,
            "rssiDbm": None
        },
        "telemetrySource": "SNMP",
        "sequenceNumber": 88213
    }
    
    # synchronizer = Neo4jTwinSynchronizer("bolt://localhost:7687", "neo4j", "password")
    # synchronizer.sync_telemetry_event(event)
    # synchronizer.close()
