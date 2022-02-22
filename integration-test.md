# Integration test

- Unit tests are great at verifying business logic, but it’s not enough to check
that logic in a vacuum

- Unit tests cover the domain model and the integration test covers the
controller quadrants.

[!code quadrants](./images/code-quadrants-testing.png)

- Check as many of the business scenarios edge cases(when business execution
    results in error) as possible with unit tests and use integration test to
cover one happy path per business scenario and any edge cases that can't be
tested in unit test.

- end to end tests are subset to integration test

- For integration test select the longest happy path in order to verify
interactions with all the out-of-process dependencies. If there is no one path
that goes through all such interactions write additional integration tests- as
many as needed to capture communications with every system.

- There is no need to test an edge case if an incorrect execution of that edge
case immediately fails the entire application.

- Its better to not write a test at all than to write a bad test. A test that
doesn't add significant value is a bad test.

- Fail fast principle: It stands for stopping the current operation as soon as
any unexpected error occurs. 

- preconditions are one example of Fail fast principle.

- two out of process dependencies- managed (on which I have full control) and
unmanaged(on which I don't have control)

## Resources

- 
