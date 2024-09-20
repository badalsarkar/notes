# Kubernetes

chatgpt: https://chatgpt.com/c/344f62c5-90ff-42c1-860a-7654a33622e8
gimini: https://gemini.google.com/app/d5b2e491d4eba5e8

- Components
- Deployment
  - manages pod
  - checks the health of the pod and restarts pod's container if it terminates
- Pod
  - A collection of containe grouped together for the purpose of administration and networking
  - Has IP address
  - It contains one or more container and volume
  - Volume connects to PV using PVC
- Service
  - It is a load balancer
  - It exposes containers so that they can be accessed by clients
- PV (persistent volume)
  - It is the storage which can be cloud or local storage
  - Pods are not aware of it. Rather Pods connect to PV using PVC (persistent volume claim)
