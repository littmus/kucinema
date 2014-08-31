# -*- coding:utf-8 -*-
from django.db import models
import watson


class Movie(models.Model):
    title = models.TextField()
    """
    genre
    running_time
    age_for
    director
    pic_url
    """

    class Meta:
        app_label = 'kucinema'

    def __unicode__(self):
        return self.title


class Schedule(models.Model):
    schedule = models.DateTimeField()
    movie = models.ForeignKey(Movie)

    THEATER_CHOCIES = (
        ('tr', 'trap'),
        ('tq', 'theque'),
    )

    theater = models.CharField(length=2, choices=THEATER_CHOCIES)

    class Meta:
        app_label = 'kucinema'

    def __unicode__(self):
        return '%s - %s' % (movie.title, self.schedule)

