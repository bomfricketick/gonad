{%- macro type_string() -%}
  varchar
{%- endmacro -%}

{%- macro type_datetime() -%}
  datetime2
{%- endmacro -%}


{%- macro quote(str, quote_left="[", quote_right="]") -%}
  {%- set quoted = quote_left ~ str ~ quote_right -%}
  {{ quoted }}
{%- endmacro -%}

{%- macro is_numeric_datatype(datatype) -%}
  {%- set is_numeric = datatype in ["decimal", "numeric", "bigint" "numeric", "smallint", "decimal", "int", "tinyint", "money", "float", "real"]  -%}
  {{ is_numeric }}
{%- endmacro -%}


{%- macro is_string_datatype(datatype) -%}
  {%- set is_string = datatype in ["varchar", "char", "text", "nchar", "nvarchar", "ntext", "binary", "varbinary", "image", "sysname"]  -%}
  {{ is_string }}
{%- endmacro -%}


{%- macro is_date_datatype(datatype) -%}
  {%- set is_date = datatype in ["date", "datetime", "datetime2", "smalldatetime", "time", "datetimeoffset"]  -%}
  {{ is_date  }}
{%- endmacro -%}


{%- macro is_boolean_datatype(datatype) -%}
  {%- set is_boolean = datatype in ["bit"]  -%}
  {{ is_boolean }}
{%- endmacro -%}


{%- macro is_countable_datatype(datatype) %}
    {%- set is_countable = datatype in ["bigint", "numeric", "smallint", "decimal", "int", "tinyint", "money", "float", "real", "varchar", "char", "text", "nchar", "nvarchar", "ntext", "binary", "varbinary", "image", "sysname", "date", "datetime", "datetime2", "smalldatetime", "time", "datetimeoffset"]  -%}
    {{ is_countable }}
{%- endmacro -%}




{# Macros for all measures done by the profiling #}
{%- macro row_count(column, data_type) -%}
  cast(count(*) as numeric)
{%- endmacro %}

{%- macro not_null_proportion(column, data_type) -%}
  round(sum(case when {{ quote(column) }} is null then 0 else 1 end) / cast(count(*) as numeric), 2)
{%- endmacro %}

{%- macro distinct_proportion(column, data_type) -%}
  round(count(distinct {%- if is_countable_datatype(data_type) == 'True' %} {{ quote(column) }} {%- else %} cast({{ quote(column) }} as varbinary) {%- endif -%} ) / cast(count(*) as numeric), 2)
{%- endmacro %}

{%- macro distinct_count(column, data_type) -%}
  count(distinct {%- if is_countable_datatype(data_type) == 'True' %} {{ quote(column) }} {%- else %} cast({{ quote(column) }} as varbinary) {%- endif -%} )
{%- endmacro %}

{%- macro is_unique(column, data_type) -%}
  case when count(distinct {%- if is_countable_datatype(data_type) == 'True' %} {{ quote(column) }} {%- else %} cast({{ quote(column) }} as varbinary) {%- endif -%} ) = count(*) THEN 1 ELSE 0 END
{%- endmacro %}

{%- macro min_value(column, data_type) -%}
  {%- if is_numeric_datatype(data_type)  == 'True' or is_date_datatype(data_type)  == 'True' -%} cast(min({{ quote(column) }}) as {{ type_string() }}) {%- else -%} null {%- endif %}
{%- endmacro %}

{%- macro max_value(column, data_type) -%}
  {%- if is_numeric_datatype(data_type)  == 'True' or is_date_datatype(data_type)  == 'True' -%} cast(max({{ quote(column) }}) as {{ type_string() }}) {%- else -%} null {%- endif %}
{%- endmacro %}

{%- macro avg_value(column, data_type) -%}
  {%- if is_numeric_datatype(data_type)  == 'True' -%} avg(cast({{ quote(column) }} as numeric)) {%- else -%} cast(null as numeric) {%- endif %}
{%- endmacro %}

{%- macro std_dev_population(column, data_type) -%}
  {%- if is_numeric_datatype(data_type)  == 'True' -%} stdevp({{ quote(column) }}) {%- else -%} cast(null as numeric) {%- endif %}
{%- endmacro %}

{%- macro std_dev_sample(column, data_type) -%}
  {%- if is_numeric_datatype(data_type)  == 'True' -%} stdevp({{ quote(column) }}) {%- else -%} cast(null as numeric) {%- endif %}
{%- endmacro %}

