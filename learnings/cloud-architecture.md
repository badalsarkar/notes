# Cloud Architecture

## Notes

- Types of System Requirements
  - Functional
    - Unique aspect of the system
  - Non-Functional (Quality requirements)
    - Performance
    - Scalability
    - Availability
    - Reliability
  - System Constraints
- Software Architecture Pattern
  - Cloud computing pattern
    - IaaS
    - Pricing model - usage based
    - Multi region deployment
    - Multi zone
  - Disadvantage of cloud computing
    - The cost grows significantly
    - The infrastructure is out of our control. We don't get the latest hardware
- Scalability Pattern
  - Load balancing pattern
    - Request -> Load balancer dispatcher -> worker
    - Example: Load balancing HTTP request from front end to back end
    - For micro-service architecture, each service can be behind load balancer which will allow scaling each service individually
    - implementation
      - Using cloud load balancing service
      - Using message broker
        - Although the message broker's function is not load balancing, it can work for the right use case
        - The communication between publisher and consumer should be one directional and asynchronous. Meaning the publisher doesn't need any response from consumer.
        - This should be used for load balancing internal requests
      - implementation consideration
        -
