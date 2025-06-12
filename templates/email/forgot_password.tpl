{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello 
{% endblock %}

{% block body %}
Click on the link below to change your password accout
http://127.0.0.1:8000{{url}}?token={{token}}


{% endblock %}