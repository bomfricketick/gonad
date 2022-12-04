@duplicate
Feature: Duplicate test
    @data_mart @dimension @scd1
    Scenario Outline: Test duplicates in scd1 dimensions
        Given I have table <dimension_table> with <dimension_column_id> column
        When I count the number of rows in <dimension_table> with <dimension_column_id> column
        Then I expect the number of rows to be <expected_rows>

        Examples:
            | dimension_table | dimension_column_id | expected_rows |
            | scd1.dim1       | id                  | 0             |
            | scd1.dim2       | id                  | 0             |
            | scd1.dim3       | id                  | 0             |
            | scd1.dim4       | id                  | 0             |
            | scd1.dim5       | id                  | 0             |
            | scd1.dim6       | id                  | 0             |
            | scd1.dim7       | id                  | 0             |



    Scenario Outline: Test duplicates in scd2 dimensions
        @data_mart @dimension @scd2
        Given I have table <dimension_table> with <dimension_column_id> column
        And I have table <dimension_table> with <dimension_column_effective_from> column
        When I count the number of rows in <dimension_table> with <dimension_column_id> column for <dimension_column_effective_from> column
        Then I expect the number of rows to be <expected_rows>

        Examples:
            | dimension_table | dimension_column_id | dimension_column_effective_from | expected_rows |
            | scd2.dim1       | id                  | effective_from                  | 0             |
            | scd2.dim2       | id                  | effective_from                  | 0             |
            | scd2.dim3       | id                  | effective_from                  | 0             |
            | scd2.dim4       | id                  | effective_from                  | 0             |
            | scd2.dim5       | id                  | effective_from                  | 0             |
            | scd2.dim6       | id                  | effective_from                  | 0             |
            | scd2.dim7       | id                  | effective_from                  | 0             |