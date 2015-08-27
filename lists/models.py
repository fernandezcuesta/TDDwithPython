from django.db import models
from django.core.urlresolvers import reverse
# DONT FORGET TO MAKE THE MIGRATIONS AFTER MODIFYING THIS FILE !!! #############


class List(models.Model):
    author = models.TextField(default='John Doe')

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    def __str__(self):
        return "List id: %s by %s, %s item(s)" % (
            self.id,
            self.author,
            self.item_set.count()
        )


class Item(models.Model):
    text = models.TextField(default='')
    # Auto add timestamp for publish_date, and save to DB as NULL when missing
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    list = models.ForeignKey(List, default=None)

    class Meta:
        unique_together = ('list', 'text')
        ordering = ["-publish_date"]  # newer on top

    def __str__(self):
        return self.text
