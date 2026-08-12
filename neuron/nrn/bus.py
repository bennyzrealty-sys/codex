"""The synapse — a thin MQTT wrapper carrying Thoughts.

Topics:
  neuron/thoughts          every thought, broadcast; bodies filter locally
  neuron/presence/<name>   retained heartbeat so bodies know each other
"""
from __future__ import annotations

import logging
from typing import Callable

import paho.mqtt.client as mqtt

from .protocol import Thought

log = logging.getLogger("nrn.bus")

THOUGHTS = "neuron/thoughts"
PRESENCE = "neuron/presence"


class Bus:
    def __init__(self, name: str, host: str = "localhost", port: int = 1883):
        self.name = name
        self._on_thought: Callable[[Thought], None] | None = None
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2, client_id=f"nrn-{name}"
        )
        self.client.will_set(f"{PRESENCE}/{name}", "offline", retain=True)
        self.client.on_connect = self._connected
        self.client.on_message = self._message
        self.client.connect(host, port, keepalive=30)

    def _connected(self, client, userdata, flags, reason_code, properties):
        log.info("synapse up as %s (%s)", self.name, reason_code)
        client.subscribe(THOUGHTS)
        client.publish(f"{PRESENCE}/{self.name}", "online", retain=True)

    def _message(self, client, userdata, msg):
        try:
            t = Thought.from_json(msg.payload)
        except Exception as e:  # a malformed thought is noise, not a crash
            log.warning("unparseable thought dropped: %s", e)
            return
        if t.origin == self.name:
            return  # our own echo
        if self._on_thought:
            self._on_thought(t)

    def on_thought(self, fn: Callable[[Thought], None]) -> None:
        self._on_thought = fn

    def emit(self, t: Thought) -> None:
        self.client.publish(THOUGHTS, t.to_json())

    def run_forever(self) -> None:
        self.client.loop_forever()

    def run_background(self) -> None:
        self.client.loop_start()
