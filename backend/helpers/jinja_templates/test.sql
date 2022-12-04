
test
{% for key, value in macro.macro.items() %}
 {{ key }} = '{{ value }}'
{%- endfor %}
