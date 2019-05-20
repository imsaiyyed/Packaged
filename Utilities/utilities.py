# timeconverter.py
 
from datetime import datetime, timedelta, tzinfo
 
# Create tzinfo classes, instances of which you tie into a datetime object
class UTC(tzinfo):
  def utcoffset(self, *dt):
    return timedelta(hours=0)
 
  def tzname(self, dt):
    return "UTC"
 
  def dst(self, dt):
    pass
 
class India(tzinfo):
  def utcoffset(self, *dt):
    return timedelta(hours=5,minutes=30)
 
  def tzname(self, dt):
    return "India"
 
  def dst(self, dt):
    pass
 
# Transform functions
def local_to_utc(date_input):
  """date_input is a datetime object containing a tzinfo
 
  Returns a datetime object at UTC time.
  """
 
  tzoffset = date_input.tzinfo.utcoffset()
  date = (date_input - tzoffset).replace(tzinfo=UTC())
  return date
 
def utc_to_local(date_input):
  """date_input is a datetime object containing a tzinfo
 
  Returns a datetime object at Manila time.
  """
 
  india = India()
  tzoffset = india.utcoffset()
  date = (date_input + tzoffset).replace(tzinfo=india)
  return date

def datetimeconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleanr1 = re.compile('{.*?}')
  cleanr2 = re.compile('\n')

  cleantext = re.sub(cleanr, '', raw_html)
  cleantext=re.sub(cleanr1, '', cleantext)
  cleantext=re.sub(cleanr2, '', cleantext)

  return cleantext
res=utc_to_local(datetime.today())
