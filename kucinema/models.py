# -*- coding:utf-8 -*-

from django.db import models
#import watson


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    reservation = models.URLField(null=True)
    """
    genre
    running_time = models.IntegerField()
    age_for
    director
    pic_url = models.URLField(null=True)
    """
    intro = models.TextField(blank=True)

    class Meta:
        app_label = 'kucinema'

    def __unicode__(self):
        return self.title
    

class Schedule(models.Model):
    movie = models.ForeignKey(Movie)

    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    early = models.BooleanField(default=False)

    THEATER_CHOCIES = (
        ('tr', 'trap'),
        ('tq', 'theque'),
    )

    theater = models.CharField(max_length=2, choices=THEATER_CHOCIES)

    class Meta:
        app_label = 'kucinema'
        ordering = ['date', 'time_start']

    def __unicode__(self):
        return '%s - %s' % (self.movie.title, self.date)

