@orphan
Feature: Orhan relationship test
    @data_mart
    Scenario Outline: test orphan relationship data mart
        Given I have a data mart with a <fact_table> and a <dimension_id>
        And i have a <dimension_table> with a <dimension_id>
        When I count number of orphan relationships between <fact_table> and <dimension_table>
        Then I expect the number of rows to be <expected_rows>

        Examples:
        | fact_table | dimension_table | dimension_id | expected_rows |
        | orders     | customers       | customer_id  | 0             |


    @data_vault
    Scenario Outline: test non orphan relationship data vault
        Given I have a <hashKey> in a <hub>
        And I have a <satellite_or_link> with a <hashKey>
        When I count number of orphan relationships between <hub> and <satellite_or_link>
        Then I expect the number of rows to be <expected_rows>

        Examples:
        | hub           | satellite_or_link  | hashKey       | expected_rows |
        | customers_hub | customers_sat      | customer_hhk  | 0             |
        | products_hub  | products_link      | product_hhk   | 0             |
        | orders_hub    | orders_sat         | order_hhk     | 0             |


