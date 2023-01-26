
from flask import Flask
from model import connect_to_db
import json
import os

app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
API_KEY = os.environ['ZILLOW_KEY']
import requests


def fetch_images():
    """Request API to fetch images and output in a file"""
    url = "https://zillow-com1.p.rapidapi.com/images"

    headers = {
      "X-RapidAPI-Key": API_KEY,
      "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }
    
    # load data from data/properties.json and save it to a variable
    with open('data/test.json') as f:
      property_data = json.loads(f.read())

    # data = [] # or property_data
    # for i in range(0, 20):
    #   data.append(property_data[i])

    images_dict = {}

    for property in property_data:
      zpid = property["zpid"]
      querystring = {"zpid":zpid}
      res = requests.get( url, headers=headers, params=querystring)
      dataa = res.json()
      images_dict[zpid] = dataa['images']

    json_object = json.dumps(images_dict, indent=2)

    with open ("data/images1.json", "w") as outfile:
      outfile.write(json_object)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
