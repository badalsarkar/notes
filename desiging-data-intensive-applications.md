# Designing data intensive applications

## Reliable, Scalable and Maintainable Applications

- **Reliability**
  - The system is designed to be fault tolerant so that the fault doesn't lead to system failure. It's not possible to make the probability of fault to 0 and thus it is better to be tolerant of fault rather than trying to prevent the faults. It is important to know how to build fault tolerant systems from unreliable parts.
  - Faults
    - Hardware faults
      - Hardware failures are not preventable. But to avoid catastrophe when it happens, we need redundant hardware e.g. back up power, RAID configuration for hard disk.
      - To build a system that can tolerate the loss of entire system, software fault tolerance techniques should be used. This allows 0 downtime maintenance.
    - Software errors
    - Human error
    - How to make system reliable?
      - Apply software design that minimizes opportunities for error. Use abstraction
      - Decouple places where people can make error and places where they can cause failure. Use sandbox environment to try out new things.
      - Testing
      - Recovery plan
      - Monitoring
- **Scalability**
  - Define the load
    - The _load Parameter_ varies depending on the application e.g. request per second, read/write per second etc.
  - Define the current performance
    - How does the current system perform if load increases and resources remain the same?
    - If load is increased how much you need to increase the resources to keep performance unchanged?
    - Latency vs response time
      - Response time is the total time to get the result. It includes service time (time to process the request), network delays, queueing delays.
      - Latency is the duration that a request is waiting to be handled- awaiting service
    - Measure of latency: use percentile
  - Approaches for coping with load
    - The architecture of application varies depending on the load and type of application.
    - Mixing scale up and scale out strategy is useful.
    - Distributing stateless services is straightforward but not the stateful service.
    - There is no scalable architecture that is one size fits all. It will depend on the application and the load parameters.
- **Maintainability**
  - Designing software so that it will minimize pain during maintenance. We should avoid creating legacy software ourselves.
  - Three design principles for improved maintainability
    - Operability
      - Make it easy for the operations team to keep the system running smoothly
      - Keep in mind the following to design a operable system
        - Set up monitoring
        - Provide good support for automation and integration with other tools
        - Avoid dependency on individual machine ( allowing machine to be taken down for maintenance )
        - Providing good documentation and easy to understand operation model
        - Provide default behaviour but give administrator the freedom to override the defaults
        - Self healing where appropriate but give administrator manual control over the system
        - Exhibit predictable behaviour, minimize surprise
    - Simplicity
      - Complex system is hard to maintain and evolve
      - Complexity may arise from explosion of state space, tight coupling between modules, tangled dependencies, inconsistent naming and terminologies, hacks at solving performance problems and many more.
      - Accidental complexity is the complexity associated with the implementation not associated with the problem itself. Avoid accidental complexity.
      - How do we avoid complexity? - By using abstraction which hides implementation details.
    - Evolvability
      - Software changes frequently- requirements changes, request for new functionality comes, regulatory requirements changes.
      - Easy to understand software and good abstraction helps making changes to a software. Agile community suggests tools like TDD and refactoring for making rapid changes.

## Data Models and Query Language
