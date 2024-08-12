# Contributor Client Setup Guide

## Overview

This guide will walk you through the process of setting up your environment to contribute computational resources to the Ray-based crowd-computing platform. As a contributor, you'll configure a Python virtual environment, install the necessary dependencies, open the required network ports, and join the Ray cluster. This setup allows your system to perform distributed computations as part of a larger research initiative.

## Prerequisites

Operating System: Linux (Ubuntu recommended)
Python Version: 3.11 (compatible with Ray as of the latest development version)
Ray Version: Ensure compatibility with the Ray version used by the head node.
Setup Instructions

1. Preparing the Server
Before joining the cluster, the head node and worker nodes must be prepared with the necessary software and configurations.

Install Python 3.11 and Essential Tools

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt upgrade
sudo apt install python3.11 python3.11-venv python3.11-dev -y
sudo apt-get install -y build-essential curl pkg-config psmisc unzip
```
Clone the Ray Repository

```bash
git clone https://github.com/Emmastro/ray.git
cd ray
git checkout dev
```

Create and Activate a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```


2. Joining the Ray Cluster
Ensure Ray Version Compatibility

Make sure that the Ray version on your local machine matches the version running on the head node. For example, if the head node is running Ray 2.24.0, you should install the same version:

```bash
pip install ray==2.24.0
```
Start Ray and Join the Cluster

```
bash
ray start --address=<head_node_public_ip>:6379
```

Note: Ensure that the port used by Ray for health checks is open. Otherwise, you may encounter the error: "Unexpected termination: health check failed due to missing too many heartbeats."

3. Open Required Ports on the Client Side
To ensure your machine can communicate with the Ray cluster, you need to open the necessary network ports.

Install UFW (Uncomplicated Firewall)

```bash
sudo apt-get install ufw
```

Open the Required Ports

Example:
```bash
ufw allow 11200:11299/tcp
ufw allow 10002:19999/tcp
ufw allow proto tcp from <head_node_public_ip> to any port 10002:19999
```

4. Troubleshooting

Mac Issues with Proxying API

If you're running the dashboard client on a Mac and encountering issues with proxying the API to port 8265, replace localhost with 127.0.0.1 in your configurations.
