#!/bin/bash
echo "Starting inventory backup - $(date)"
if [ -d "/etc/bluebanquise/inventory" ]; then
  tar cvzf /root/ansible_inventory_$(date "+%Y-%m-%d_%H-%S").tar.gz /etc/bluebanquise/inventory
  sync
  sleep 1s
  rm -Rf /etc/bluebanquise/inventory
fi
echo "End inventory backup - $(date)"
