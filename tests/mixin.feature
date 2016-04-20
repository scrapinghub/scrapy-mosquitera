Feature: Pagination Mixin
    The Pagination Mixin.


Scenario: Check initial state
    Given an instance of the mixin
    Then it has initial attributes set


Scenario: Add identifier to request
    Given a request
    When I add an identifier to the request
    Then the identifier is present in the request


Scenario: Increase counter
    Given an instance of the mixin
    Given a response with id
    When I use the response to increase the counter
    Then the counter for the response is 1


Scenario: Decrease counter
    Given an instance of the mixin
    Given a response with id
    When I use the response to decrease the counter
    Then the counter for the response is -1


Scenario: Get response with attribute
    Given an instance of the mixin
    When I set the response for the pagination mixin
    Then getting response returns the same response


Scenario: Get response with exception
    Given an instance of the mixin
    Then getting response without response object raises exception


Scenario: Get response with different number of response arguments
    Given an instance of the mixin
    Then getting response with any response objects returns the first one


Scenario: Get response id from cache
    Given an instance of the mixin
    Given a response
    When there's some response id cache
    Then I get the response id from the cache


Scenario: Get response id from cache
    Given an instance of the mixin
    Given a response
    When there's no response id cache
    Then I get a new response id


Scenario: Register requests
    Given an instance of the mixin
    When I set the response for the pagination mixin
    And I register requests with a method returning <n_requests>
    Then every request is marked
    And the counter for the response is <n_requests>

    Examples:
    | n_requests |
    | 1 |
    | 20 |


Scenario: Deregister response
    Given an instance of the mixin
    When I set the response for the pagination mixin
    And I deregister response
    Then the counter for the response is -1


Scenario: Enqueue next page requests
    Given an instance of the mixin
    When I set the response for the pagination mixin
    And I enqueue a method returning <n_requests>
    Then the counter of nprs is <n_requests>

    Examples:
    | n_requests |
    | 1 |
    | 20 |


Scenario: Dequeue next page requests with no valid nprs
    Given an instance of the mixin
    When request registry has counters > 0
    Then at dequeuing it doesn't raise dont close spider


Scenario: Dequeue next page requests with valid nprs
    Given an instance of the mixin
    When request registry has some counters = 0
    And I mock crawler
    Then at dequeuing it raises dont close spider


Scenario: Call next page requests
    Given an instance of the mixin
    Given a response with nprs inside
    Then many requests are yielded from call next page requests
    And it has initial attributes set

