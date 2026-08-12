#!/usr/bin/env bash
# Pi bootstrap: broker + venv + config + user systemd service.
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/4] mosquitto (the synapse)"
sudo apt-get install -y mosquitto
# LAN/tailnet only — the bus never faces the internet.
sudo tee /etc/mosquitto/conf.d/neuron.conf >/dev/null <<'EOF'
listener 1883 0.0.0.0
allow_anonymous true
EOF
sudo systemctl enable --now mosquitto

echo "[2/4] python venv"
python3 -m venv .venv
.venv/bin/pip install --quiet -r requirements.txt

echo "[3/4] config"
[ -f neuron.toml ] || cp neuron.toml.example neuron.toml

echo "[4/4] service (user unit — survives reboot with linger)"
mkdir -p ~/.config/systemd/user
cp systemd/neuron.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now neuron
sudo loginctl enable-linger "$USER"

echo
echo "neuron is awake. Try, from any body on the mesh:"
echo "  .venv/bin/python -m nrn.cli --config neuron.toml say ping"
