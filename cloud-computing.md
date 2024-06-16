# Cloud Computing

**Sources**:

1. Cloud Computing: Concepts, Technology, Security & Architecture by Thomas Erl

## Notes

- Introduction
  - definition
    - Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a **shared pool of configurable computing resources** (e.g., networks, servers, storage, applications, and services) that can be **rapidly provisioned and released with minimal management effort or service provider interaction**. This cloud model is composed of five essential characteristics, three service models, and four deployment models. by NIST
  - Business driver for cloud
    - Cost reduction
      - Cost related to infrastructures
      - Cost related to operational overhead e.g. engineers, power supply, cooling, security etc.
    - Business agility
      - Means how responsive the business is to the change.
  - Technology that influenced cloud computing
    - Clustering:
      - A cluster is a group of IT resources that are interconnected and work together as a single system.
      - A general prerequisite for hardware clustering is that its component systems have reasonably identical hardware and operating system to provide similar performance level.
      - Components in a cluster are kept in synchronization through dedicated high-speed communication links.
    - Grid computing:
      - Its a platform where computing resources are organized in logical pools.
      - These pools are collectively coordinated to provide high performance distributed grid
      - Components are loosely coupled and distributed.
      - Computing resources are heterogeneous and geographically dispersed.
    - Capacity planning
      - Estimating the future need to IT resources
      - Over capacity can mean IT over spending
    - Virtualization
      - It means converting physical IT resource to a virtual resource
      - Most IT resources can be virtualized. Virtual server, storage, network, UPS.
      - Virtualization software is used to do Virtualization.
      - Virtualization software is commonly called hypervisor.
      - In the Virtualization process, hardware requirements can be simulated by emulation software.
    - Containerization:
      - A form of Virtualization technology
      - Provides virtual environment without the need of virtual machine
    - Serverless environment
      - No need to provision a server
      - It allows deployment of software package that already includes required server Components
  - Cloud computing terminologies
    - Cloud doesn't need to be on internet protocol. It can be based on any protocol that allow remote access to IT resources.
    - Container
    - On premises
    - Cloud producer and consumer
    - Scaling
      - Horizontal : Scaling out and scaling in
        - Allocating or releasing of resources of same type.
        - Common in cloud computing environment
      - Vertical : Scaling up and scaling down
        - Replacement of IT resources with higher or lower capacity resources
        - Less common in cloud computing as it requires downtime
