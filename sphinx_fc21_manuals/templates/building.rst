{{ building.name | title }}
***************************



.. image:: ../../../../../data/tilesets/{% if building.genus == "Improvement" or building.genus == "Special" %}buildings{% else %}wonders{% endif %}/{{ building.graphic[2:100] }}.png


* :strong:`Name:` {{ building.name }}
* :strong:`helptext:` {{ building.helptext | clean_string }}
* :strong:`Type:` {{ building.genus }}
* :strong:`Build Cost (Shields):` {{ building.build_cost }}
* :strong:`Upkeep Per Turn (Gold):` {{ building.upkeep }}
* :strong:`Sabotage Cost (Gold):` {{ building.sabotage }}
* :strong:`Requirement(s):`

  {{ building.reqs | list_to_obullet }}

{% if building.obsolete_by %}* :strong:`Obsoleted By:`

  {{ building.obsolete_by | list_to_obullet }}{% endif %}

* :strong:`Rule Name:` {{ building.rule_name }}
{% if building.sound %}* :strong:`Sound:` {{ building.sound }}{% endif %}
{% if building.sound_alt %}* :strong:`Sound Alternate:` {{ building.sound_alt }}{% endif %}
