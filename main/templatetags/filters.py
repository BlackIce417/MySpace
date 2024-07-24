import datetime
from django import template
from django.utils import timezone
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def custom_timesince_or_date(value):
	now = timezone.now()
	if isinstance(value, datetime.datetime):
		value = timezone.localtime(value)
	diff = now - value

	if diff.days >= 7:
		return value.strftime("%Y-%m-%d")
	elif diff.total_seconds() <= 60:
		return "Just Now"
	else:
		return timesince(value, now) + " ago"