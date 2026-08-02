#!/bin/bash
# AWS EC2 Automated Provisioning Script for Ubuntu 22.04 LTS
set -e

echo "=== Updating System Packages ==="
sudo apt-get update && sudo apt-get upgrade -y

echo "=== Installing Python, PostgreSQL Client, Nginx, and Certbot ==="
sudo apt-get install -y python3-pip python3-venv postgresql-client nginx certbot python3-certbot-nginx git curl

echo "=== Installing Docker & Docker Compose ==="
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

echo "=== Setting Up Application Virtual Environment ==="
cd /home/ubuntu/Energy-Prediction-Optimization-System
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Installing Systemd Services ==="
sudo cp deployment/fastapi.service /etc/systemd/system/
sudo cp deployment/streamlit.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable fastapi.service
sudo systemctl enable streamlit.service
sudo systemctl start fastapi.service
sudo systemctl start streamlit.service

echo "=== Configuring Nginx Proxy ==="
sudo cp deployment/nginx.conf /etc/nginx/sites-available/campus_energy
sudo ln -sf /etc/nginx/sites-available/campus_energy /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== Deployment Completed Successfully ==="
