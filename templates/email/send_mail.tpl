{% extends "mail_templated/base.tpl" %}

{% block subject %}
Ticket 
{% endblock %}

{% block body %}
{{ text }}


{% endblock %}