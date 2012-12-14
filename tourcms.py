"Python wrapper class for TourCMS Rest API"
from __future__ import print_function
import hmac
import hashlib
import datetime as dt
import urllib
import urllib2
try:
  import xmltodict
except ImportError:
  pass
import time
import base64


__author__ = 'Jonathan Harrington'
__version__ = '0.1'
__license__ = 'BSD'


class Connection(object):
  def __init__(self, marketp_id, private_key, result_type = "raw"):
    try:
      int(marketp_id)
    except ValueError:
      raise TypeError("Marketplace ID must be an Integer")
    self.marketp_id = int(marketp_id)
    self.private_key = private_key
    self.result_type = result_type
    self.base_url = "https://api.tourcms.com"
    
  def _generate_signature(self, path, verb, channel, outbound_time):
    string_to_sign = u"{}/{}/{}/{}{}".format(channel, self.marketp_id, verb, outbound_time, path)    
    dig = hmac.new(self.private_key, string_to_sign, hashlib.sha256)
    b64 = base64.b64encode(dig.digest())
    return urllib.quote_plus(b64)

  def _response_to_native(self, response):
    try:
      return xmltodict.parse(response)['response']
    except KeyError:
      return xmltodict.parse(response)
    except NameError:
      import sys
      print("XMLtodict not available, install it by running\n\t$ pip install xmltodict", file=sys.stderr)
      return response

  def _request(self, path, channel = 0, params = {}, verb = "GET"):
    url = self.base_url + path + "?" + urllib.urlencode(params)
    req_time = dt.datetime.utcnow()
    signature = self._generate_signature(
      path + "?" + urllib.urlencode(params), verb, channel, int(time.mktime(req_time.timetuple()))
    )    
    headers = {
      "Content-type": "text/xml", 
      "charset": "utf-8", 
      "Date": req_time.strftime("%a, %d %b %Y %H:%M:%S GMT"), 
      "Authorization": "TourCMS {}:{}:{}".format(channel, self.marketp_id, signature)
    }
    req = urllib2.Request(url)
    for key, value in headers.items():
      req.add_header(key, value)
    response = urllib2.urlopen(req).read()
    return response if self.result_type == "raw" else self._response_to_native(response)

  def api_rate_limit_status(self, channel = 0):
    return self._request("/api/rate_limit_status.xml", channel)
  
  def list_channels(self):
    return self._request("/p/channels/list.xml")
  
  def show_channel(self, channel):
    return self._request("/c/channel/show.xml", channel)
  
  def search_tours(self, params = {}, channel = 0):
    if channel == 0:
      return self._request("/p/tours/search.xml", 0, params)
    else:
      return self._request("/c/tours/search.xml", channel, params)
  
  def search_hotels_range(self, params = {}, tour = "", channel = 0):
    params.update({"single_tour_id": tour})
    if channel == 0:
      return self._request("/p/hotels/search_range.xml", 0, params)
    else:
      return self._request("/c/hotels/search_range.xml", channel, params)
    
  def search_hotels_specific(self, params = {}, tour = "", channel = 0):
    params.update({"single_tour_id": tour})
    if channel == 0:
      return self._request("/p/hotels/search-avail.xml", 0, params)
    else:
      return self._request("/c/hotels/search-avail.xml", channel, params)
  
  def list_tours(self, channel = 0):
    if channel == 0:
      return self._request("/p/tours/list.xml")
    else:
      return self._request("/c/tours/list.xml", channel)
  
  def list_tour_images(self, channel = 0):
    if channel == 0:
      return self._request("/p/tours/images/list.xml")
    else:
      return self._request("/c/tours/images/list.xml", channel)
  
  def show_tour(self, tour, channel):
    return self._request("/c/tour/show.xml", channel, {"id": tour})
  
  def show_tour_departures(self, tour, channel):
    return self._request("/c/tour/datesprices/dep/show.xml", channel, {"id": tour})
  
  def show_tour_freesale(self, tour, channel):
    return self._request("/c/tour/datesprices/freesale/show.xml", channel, {"id": tour})