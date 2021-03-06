# -*- coding: utf-8 -*-
import unittest2 as unittest
import icalendar
import pytz
import datetime
import os

class TestEncoding(unittest.TestCase):

    def test_create_from_ical(self):
        directory = os.path.dirname(__file__)
        cal = icalendar.Calendar.from_ical(open(os.path.join(directory, 'encoding.ics'),'rb').read())

        self.assertEqual(cal['prodid'].to_ical(), "-//Plönë.org//NONSGML plone.app.event//EN")
        self.assertEqual(cal['X-WR-CALDESC'].to_ical(), "test non ascii: äöü ÄÖÜ €")

        event = cal.walk('VEVENT')[0]
        self.assertEqual(event['SUMMARY'].to_ical(), 'Non-ASCII Test: ÄÖÜ äöü €')
        self.assertEqual(event['DESCRIPTION'].to_ical(), 'icalendar should be able to handle non-ascii: €äüöÄÜÖ.')
        self.assertEqual(event['LOCATION'].to_ical(), 'Tribstrül')


    def test_create_to_ical(self):
        cal = icalendar.Calendar()

        cal.add('prodid', u"-//Plönë.org//NONSGML plone.app.event//EN")
        cal.add('version', u"2.0")
        cal.add('x-wr-calname', u"äöü ÄÖÜ €")
        cal.add('x-wr-caldesc', u"test non ascii: äöü ÄÖÜ €")
        cal.add('x-wr-relcalid', u"12345")

        event = icalendar.Event()
        event.add('dtstart', datetime.datetime(2010,10,10,10,00,00,tzinfo=pytz.utc))
        event.add('dtend',  datetime.datetime(2010,10,10,12,00,00,tzinfo=pytz.utc))
        event.add('created', datetime.datetime(2010,10,10,0,0,0,tzinfo=pytz.utc))
        event.add('uid', u'123456')
        event.add('summary', u'Non-ASCII Test: ÄÖÜ äöü €')
        event.add('description', u'icalendar should be able to de/serialize non-ascii.')
        event.add('location', u'Tribstrül')
        cal.add_component(event)

        ical_lines = cal.to_ical().splitlines()

        ## TODO FIX TESTS AND CODE TO SUPPORT UNICODE/UTF-8
        #self.assertTrue(u"-//Plönë.org//NONSGML plone.app.event//EN" in ical_lines)
