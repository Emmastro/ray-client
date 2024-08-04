
Prep the server (1 worker and 1 head)

# Ray as of June 17 is comparible to Python 3.8 >= and <= 3.11

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt upgrade
    sudo apt install python3.11 python3.11-venv python3.11-dev -y
    sudo apt-get install -y build-essential curl pkg-config psmisc unzip
    git clone https://github.com/Emmastro/ray.git
    git checkout dev
    cd ray
    python3.11 -m venv venv # latest supported python version for ray is 3.11
    source venv/bin/activate
    pip install ray[default]==2.31.0 # version used for development.
    python python/ray/setup-dev.py -y

    cd python/ray/dashboard/client && npm ci && npm run build
    ray start --head --dashboard-host=0.0.0.0

    Open port 6379 for the head node to make the dashboard publicly available 


RuntimeError: Version mismatch: The cluster was started with:
    Ray: 2.24.0
    Python: 3.10.14
This process on node 192.168.0.79 was started with:
    Ray: 2.23.0
    Python: 3.11.9

Need to use the same ray version


pip install ray==2.24.0

ray start --head --dashboard-host=0.0.0.0

# Joining the cluster

RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER=1 ray start --address=ec2-52-22-46-66.compute-1.amazonaws.com:6379

The port ray uses for healthcheck should be open. Otherwise, get this error: 
Unexpected termination: health check failed due to missing too many heartbeats

# Setting up ray node for development:

clone the repo 
make a virtual environment
cd python/ray/dashboard/client && npm ci && npm run build

Mac issue for proxying the api to port 8265 on the frontend: need to replace localhost by 127.0.0.1.

   18  cd python/ray/dashboard/client
   24  npm install
   25  sudo apt install npm
   26  npm install
   28  npm start


# Open ports from client side: 

sudo apt-get install ufw

ufw allow 11200:11299/tcp

ufw allow 10002:19999/tcp

ufw allow proto tcp from 52.22.46.66 to any port 10002:19999
ufw allow proto tcp from 1.2.3.4 to any port 40000:40100

