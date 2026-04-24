#!/bin/bash

# Exit on any error
set -e

# Colors for better readability
GREEN='\033[0,32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Docker Engine Installation...${NC}"

# Helper function for y/n prompts
ask_permission() {
    read -p "$1 (y/n): " choice
    case "$choice" in 
      y|Y ) return 0;;
      n|N ) return 1;;
      * ) echo "Invalid input. Skipping."; return 1;;
    esac
}

# 1. Update and install prerequisites
echo "Updating package index and installing prerequisites..."
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# 2. Add Docker’s official GPG key
echo "Setting up Docker GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Set up the repository
echo "Adding Docker repository to sources..."
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

# 4. Install Docker packages
if ask_permission "Proceed with installing Docker Engine, CLI, and Compose?"; then
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    echo -e "${GREEN}Docker installed successfully!${NC}"
else
    echo "Installation aborted."
    exit 0
fi

# 5. Post-install: Add user to docker group
if ask_permission "Add current user ($USER) to the 'docker' group? (Allows running docker without sudo)"; then
    sudo usermod -aG docker $USER
    echo -e "${GREEN}User added to docker group.${NC}"
    echo "IMPORTANT: You must log out and log back in for the group changes to take effect."
else
    echo "Skipping group addition. You will still need to use 'sudo' for docker commands."
fi

echo -e "${GREEN}Setup complete!${NC}"