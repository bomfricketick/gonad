{%- import 'generic.sql' as generic -%}
with column_profile as (
{%- for item in items %}
    {%- set is_countable = generic.is_countable_datatype(item.data_type) %}
    select
         '{{ item.schema_name }}' as schema_name
        ,'{{ item.table_name }}' as table_name
        ,'{{ item.column_name }}' as column_name
        ,'{{ item.data_type }}' as data_type
        {% for measure in measures %}
            {%- set macro_name =  measure -%}
            ,{{ generic[macro_name](column=item.column_name, data_type=item.data_type ) }} as {{ measure }}
        {% endfor -%}
        ,cast(current_timestamp as {{ generic.type_datetime() }}) as profiled_at
        ,{{ loop.index }} as _column_position
    from "{{ item.schema_name }}"."{{ item.table_name }}"
    {%- if not loop.last %} union all {%- endif %}
{% endfor %}
)

select * from column_profile