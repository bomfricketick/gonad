{%- import 'generic.sql' as generic -%}

{% for row in data -%}
    insert into dbo.{{ table }} (
        {%- for key, value in row.items() -%}
            {{ generic.quote(key) }}
            {%- if not loop.last %}, {% endif -%}
        {%- endfor -%}
    ) values (
    {% for value in row.items() -%}

        {%- if value[1] == None -%}
            NULL
        {%- else -%}

        {%- if value[0] == float %}
    {# {{ column }} #}
        {{ value[1] | float }}

        {%- endif -%}

        {%- endif -%}
        {%- if not loop.last %}, {% endif -%}
    {%- endfor -%}
    );
{% endfor -%}
