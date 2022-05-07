from django import template

register = template.Library()

# @register.filter(name='pr')
# def pr(value):
#     print(value)
#     return "form"

# # register.filter('pri', pri)