{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello 
{% endblock %}

{% block body %}
User Token: {{token}}


This is a plain text message.
{% endblock %}