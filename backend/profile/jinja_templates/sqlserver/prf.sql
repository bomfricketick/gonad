{%- import 'generic.sql' as generic -%}

{%- for item in items %}
    select {{ item.column_name}}
    , {{ item.data_type  }}
    {%- if generic.is_date_datatype(item.data_type) == 'True' %}
    , TRUE
    {%- else %}
    , FALSE
    {%- endif %}
    , {{ generic.is_date_datatype(item.data_type)}}

{% endfor %}
