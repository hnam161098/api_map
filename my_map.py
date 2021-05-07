import requests
import json


def get_token(token_file):
    f = open(token_file, "rt")
    key = f.read()
    return key


def map(url, file):
    param = {
        "apiKey": get_token(file),
        "in": "circle:21.01595,105.82301;r=2000",
        "q": 'coffe',
        "limit": 50,
    }
    req = requests.get(url, params=param)
    data = req.json()
    result = {"type": "FeatureCollection",
              "features": []
              }
    for item in data["items"]:
        lat = item["position"]["lat"]
        lng = item["position"]["lng"]
        geojsonFeature = {
            "type": "Feature",
            "properties": {
                "name": item["title"],
                "location": item["address"]["label"],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]
            }
        }
        result["features"].append(geojsonFeature)

    with open("my_map.geojson", "wt", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return result


def main():
    url = "https://discover.search.hereapi.com/v1/discover"
    token_file = "token.txt"
    for i in map(url, token_file)["features"]:
        print(i)


if __name__ == "__main__":
    main()
