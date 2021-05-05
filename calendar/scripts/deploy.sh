#! /bin/bash

set -eux

echo "Deploying...";
sudo ansible-playbook -i scripts/inventory.ini scripts/deploy.yml
