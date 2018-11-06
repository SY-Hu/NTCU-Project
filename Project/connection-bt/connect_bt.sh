#!/bin/sh

echo "Bluetooth Connect Support Program"
pulseaudio --start 
sleep 1
echo 'agent on\ndefault-agent\nscan on\ndiscoverable on'|bluetoothctl
