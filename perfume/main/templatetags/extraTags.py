from django import template

register = template.Library()

@register.filter(name="myLocalize")
def myLocalize(value):
    return "{:,}".format(value).replace(","," ")

@register.filter(name="isDigit")
def isDigit(value):
    if str(value)[0].isdigit():
        return False
    else:
        return True

@register.filter(name="allButFirst")
def allButFirst(value):
    return value[1:]

@register.filter(name="exists")
def exists(value):
    if len(value)!=0:
        return True
    else:
        return False

@register.filter(name="getQuantityRow")
def getQuantityRow(value):
    row = []
    b = 1
    while b < len(value):
        row.append(b)
        b += 1
    return row

