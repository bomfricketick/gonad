select schemas.name as schema_name
    , tables.name as table_name
    , columns.name as column_name
    , data_types.name as data_type
from sys.objects as tables
join sys.schemas as schemas on tables.schema_id = schemas.schema_id
join sys.columns as columns on tables.object_id = columns.object_id
join sys.types as data_types on columns.system_type_id = data_types.system_type_id
and columns.user_type_id = data_types.user_type_id
where 1=1
{%- if table_type %}
AND tables.type IN (
    {%- for type in table_type -%}
    '{{ type }}'
    {%- if not loop.last -%}
        {{ separator }}
    {%- endif -%}
    {%- endfor -%}
)
{%- endif %}
{%- if include_schemas %}
AND schemas.name IN (
    {%- for schema in include_schemas -%}
    '{{ schema }}'
    {%- if not loop.last -%}
        {{ separator }}
    {%- endif -%}
    {%- endfor -%}
)
{%- endif %}
{%- if exclude_schemas %}
AND schemas.name NOT IN (
    {%- for schema in exclude_schemas -%}
    '{{ schema }}'
    {%- if not loop.last -%}
        {{ separator }}
    {%- endif -%}
    {%- endfor -%}
)
{% endif %}
