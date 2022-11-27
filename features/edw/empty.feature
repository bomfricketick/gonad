@empty
Feature: Empty table test
    Scenario Outline: Empty table test
        Given I have table <table_name>
        When I run query
        Then I shouldn't get row count of <not_expected_row_count>
        Examples:
            | table_name | not_expected_row_count |
            | empty      | 0                      |
            | not_empty  | 0                      |
