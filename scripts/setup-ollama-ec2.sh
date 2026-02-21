#!/bin/bash
# Victor.I - EC2 User Data Script for Ollama Setup
# Use this when launching an EC2 instance for Ollama

set -e

echo "🤖 Installing Ollama on EC2..."

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
systemctl start ollama
systemctl enable ollama

# Pull the model
ollama pull llama3.2

echo "✅ Ollama installed and llama3.2 model ready!"
echo "Ollama is running on port 11434"
echo "Configure security group to allow inbound from App Runner/ECS on port 11434"
