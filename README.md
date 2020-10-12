# cloud-storage-test
Python Script for testing object cloud storages inside Kubernetes
Hi! To use this script, you need to:
1. Clone this repo, place your input files along with the script.
2. Then build an image, push it and refer it in deployment.yaml.
3. SSH into a pod created, go to /mnt and run the script.
4. Run the script like: python3 filegen_v3.2.2.py
Please type python3 filegen_v3.2.2.py -h if you need help.
