Feature: Date matchers
    The date matchers.


Scenario: Get datetime from datetime object
    Given a datetime object
    Then transforming datetime to datetime returns the same object


Scenario: Get datetime from a string with date format
    Given a string with date format
    Then transforming date string to datetime returns a valid datetime object


Scenario: Get datetime from date object
    Given a date object
    Then transforming date object to datetime returns a valid datetime object


Scenario: Get exception when transforming invalid date string
    Given a invalid date string
    Then transforming an invalid date string raises exception


Scenario: Has valid date
    Given target date <target_date>
    Given min date <min_date>
    Given max date <max_date>
    Then has valid date is <true_or_false>

    Examples:
    | target_date | min_date   | max_date   | true_or_false |
    | 2016-04-15  | 2016-04-01 | 2016-04-30 | True          |
    | 2016-04-15  | 2016-05-01 | 2016-04-30 | False         |
    | 2016-04-15  | 2016-04-15 | 2016-04-30 | True          |
    | 2016-04-15  | 2016-04-30 | 2016-04-30 | False         |


Scenario: Get minimum date
    Given a datetime object
    Given a parameter <param> with value the datetime object
    Then minimum date equal to datetime object is <true_or_false>

    Examples:
    | param    | true_or_false |
    | min_date | True          |
    | on       | True          |
    | after    | True          |
    | since    | True          |
    | any_arg  | False         |


Scenario: Get minimum date with invalid arg
    Given a datetime object
    Given a parameter <param> with value the datetime object
    Then minimum date is the default

    Examples:
    | param    |
    | any_arg  |


Scenario: Get maximum date
    Given a datetime object
    Given a parameter <param> with value the datetime object
    Then maximum date equal to datetime object is <true_or_false>

    Examples:
    | param    | true_or_false |
    | max_date | True          |
    | on       | True          |
    | before   | True          |
    | any_arg  | False         |


Scenario: Get maximum date with invalid arg
    Given a datetime object
    Given a parameter <param> with value the datetime object
    Then maximum date is the default

    Examples:
    | param    |
    | any_arg  |


Scenario: Date matches without data
    Given empty data
    Then date matches is <true_or_false>

    Examples:
    | true_or_false |
    | False         |


Scenario: Date matches without data
    Given empty data
    Then date in period matches is <true_or_false>

    Examples:
    | true_or_false |
    | False         |


Scenario: Date in period day
    Given target date <target_date>
    Given min date <min_date>
    Given max date <max_date>
    Then date in period day with <maximum> is <true_or_false>

    Examples:
    | target_date | min_date   | max_date   | maximum | true_or_false |
    | 2016-04-15  | 2016-04-01 | 2016-04-30 | True    | True          |
    | 2016-04-15  | 2016-04-01 | 2016-04-30 | False   | True          |
    | 2016-04-15  | 2016-04-30 | 2016-05-01 | True    | False         |
    | 2016-04-15  | 2016-04-30 | 2016-05-01 | False   | False         |
    | 2016-04-15  | 2016-04-15 | 2016-04-30 | True    | True          |
    | 2016-04-15  | 2016-04-15 | 2016-04-30 | False   | True          |
    | 2016-04-15  | 2016-04-30 | 2016-04-30 | True    | False         |
    | 2016-04-15  | 2016-04-30 | 2016-04-30 | False   | False         |
    | 2017-04-15  | 2016-04-30 | 2016-04-30 | False   | True          |


Scenario: Date in period week
    Given target date <target_date>
    Given min date <min_date>
    Given max date <max_date>
    Then date in period week with <maximum> is <true_or_false>

    Examples:
    | target_date | min_date   | max_date   | maximum | true_or_false |
    | 2016-05-02  | 2016-05-05 | 2016-05-20 | True    | True          |
    | 2016-04-25  | 2016-05-05 | 2016-05-20 | True    | False         |
    | 2017-05-02  | 2016-05-05 | 2016-05-20 | True    | False         |
    | 2017-05-02  | 2016-05-05 | 2016-05-20 | False   | True          |


Scenario: Date in period month

    Given target date <target_date>
    Given min date <min_date>
    Given max date <max_date>
    Then date in period month with <maximum> is <true_or_false>

    Examples:
    | target_date | min_date   | max_date   | maximum | true_or_false |
    | 2016-05-02  | 2016-05-01 | 2016-06-01 | True    | True          |
    | 2016-04-02  | 2016-05-01 | 2016-06-01 | True    | False         |
    | 2016-04-02  | 2016-04-21 | 2016-06-01 | True    | True          |
    | 2016-06-02  | 2016-04-21 | 2016-06-01 | True    | True          |
    | 2016-07-02  | 2016-04-21 | 2016-06-01 | True    | False         |


Scenario: Date in period year
    Given target date <target_date>
    Given min date <min_date>
    Given max date <max_date>
    Then date in period year with <maximum> is <true_or_false>

    Examples:
    | target_date | min_date   | max_date   | maximum | true_or_false |
    | 2016-05-02  | 2016-05-05 | 2016-05-20 | True    | True          |
    | 2015-04-25  | 2016-05-05 | 2016-05-20 | True    | False         |
    | 2017-05-02  | 2016-05-05 | 2016-05-20 | True    | False         |
    | 2017-05-02  | 2016-05-05 | 2016-05-20 | False   | True          |
