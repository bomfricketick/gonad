@integrity
Feature: Integrity check
    @Satelite
    Scenario Outline: Satelite to Hub integrity check
        Given I have <Satelite> with reference to <Hub>
        When I run the integrity check
        Then I expect the number of rows to be <expected_rows>

        Examples:
        | Satelite  | Hub   | expected_rows |
        | Satelite1 | Hub1  | 0             |
        | Satelite2 | Hub2  | 0             |

    @Link
    Scenario Outline: Link to Hub integrity check
        Given I have <Link> with reference to <Hub>
        When I run the integrity check
        Then I expect the number of rows to be <expected_rows>

        Examples:
        | Link  | Hub   | expected_rows |
        | Link1 | Hub1  | 0             |
        | Link2 | Hub2  | 0             |