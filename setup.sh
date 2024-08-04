sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
python3.11 -m venv env
source env/bin/activate
pip install ray[default]
sudo chmod -R a+rwx env
sudo apt-get install gdb # required for debugging or memory profiling from workers (all nodes as head is a worker too)
