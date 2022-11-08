Units
*****

.. toctree::{% for item in unit_type_list %}
   units/{{ item | make_slug }}.rst{% endfor %}
   :maxdepth: 1

