include .env

start-ray:
	ray start --head --dashboard-host=0.0.0.0

connect-head:
	ssh -i ./crowd-computing.pem ubuntu@${HEAD_NODE_IP}