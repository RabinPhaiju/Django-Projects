1. Substitions

   - {{ zap }}
   - {{ zap|safe }
     }

2. Logic

   - {% if zap > 100 %} # space is required before and after of '>'|operator
     {% endif %}

3. Blocks

   - {% block content %}
   - {% endblock %}

4. Loop
   - {% for x in fruits %}
   - {{x}}
   - {{ x|length}} # filter
   - {% endfor %}
