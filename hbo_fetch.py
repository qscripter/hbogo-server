import requests
import dateutil.parser
from lxml import etree


def obj_from_element (element):
  obj = dict()
  obj['images'] = dict()
  obj['videos'] = dict()
  for child in element:
    if child.tag == "imageResponses":
      obj['images'][child.find('mediaSubType').text] = child.find('resourceUrl').text
    elif child.tag == "videoResponses":
      obj['images'][child.find('mediaSubType').text] = child.find('resourceUrl').text
    if len(child):
      obj[child.tag] = obj_from_element(child)
    else:
      obj[child.tag] = child.text
  return obj



  



class HboCatalog:

  @property
  def features(self):
      return self._features

  @features.setter
  def features(self, value):
      self._features = value

  def create_feature(self, root):
    feature = dict()
    feature['title'] = root.find('title').text
    feature['url'] = "http://www.hbogo.com/#movies/video&assetID=%s?videoMode=embeddedVideo?showSpecialFeatures=false/"%root.find('TKey').text
    feature['shortSummary'] = root.find('shortSummary').text
    feature['summary'] = root.find('summary').text
    feature['rating'] = root.find('ratingResponse').find('ratingDisplay').text
    feature['startDate'] = dateutil.parser.parse(root.find('startDate').text)
    feature['endDate'] = dateutil.parser.parse(root.find('endDate').text)
    feature['images'] = dict()
    for image in root.findall('imageResponses'):
      feature['images'][image.find('mediaSubType').text] = image.find('resourceUrl').text
    for video in root.findall('videoResponses'):
      if video.find('mediaSubType').text == "PRO12_VIDEO":
        for child in video:
          if child.tag == "runtime":
            feature['runtime'] = int(child.text)
          else:
            feature[child.tag] = child.text
    feature['genres'] = []
    for genre in root.findall('genres'):
      feature['genres'].append(genre.find('name').text)
    self._features.append(feature)


  def __init__ (self, url):
    r = requests.get(url)
    #shave xml declaration off beginning
    self._xml = r.text[55:]
    self._root = etree.fromstring(self._xml)
    self._features = []

    for child in self._root.find("body").find("productResponses").findall("featureResponse"):
      self.create_feature(child)






