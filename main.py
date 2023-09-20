# main.py

import os
import json
import http.client


# "/agencies.json?callback=call&geo_area=35.80176%2C-78.64347%7C35.78061%2C-78.68218&agencies=12"
url_agencies = "/agencies.json?callback=call&geo_area={0}&agencies={1}"
# "/arrival-estimates.json?agencies=12%2C16&routes=4000421%2C4000592%2C4005122&stops=4002123%2C4023414%2C4021521&callback=call"
url_arrival = "/arrival-estimates.json?agencies={0}&routes={1}&stops={2}&callback=call"
# "/stops.json?agencies=12%2C16&geo_area=35.80176%2C-78.64347%7C35.78061%2C-78.68218&callback=call"
url_stops = "/stops.json?agencies={0}&geo_area={1}&callback=call"

# constants
APIHOST = "transloc-api-1-2.p.rapidapi.com"
METHODS = {
    'get': "GET",
    'head': "HEAD",
    'post': "POST",
    'put': "PUT",
    'delete': "DELETE",
    'patch': "PATCH"
}


def set_api_headers(api_token: str, api_host: str) -> dict:
    """ doc string """
    headers = {
        'X-RapidAPI-Key': f"{api_token}",
        'X-RapidAPI-Host': f"{api_host}"
    }

    return headers


def get_http_data(http_method: str, api_host: str, input_url: str, http_headers: dict) -> bytes:
    """ doc string """
    http_connection = http.client.HTTPSConnection(api_host)
    http_connection.request(
        http_method,
        input_url,
        headers=http_headers
    )

    http_resource = http_connection.getresponse()
    http_data = http_resource.read()

    return http_data


def main() -> bytes:
    # retrieve api token from env var
    api_token = os.getenv('RAPIDAPIKEY')

    # get rapid api http headers
    headers = set_api_headers(api_token, APIHOST)

    # create url string - agency ID and geo area
    url = url_stops.format("16", r'35.80176%2C-78.64347%7C35.78061%2C-78.68218')

    # call funct to get http data
    data_bytes = get_http_data(
        METHODS['get'],
        APIHOST,
        url,
        headers
    )

    return data_bytes


if __name__ == '__main__':
    data = main()

    http_data_dict = json.loads(data.decode('utf-8'))
    
    # print name of first stop in sample
    if isinstance(http_data_dict, dict):
        print(http_data_dict['data'][0]['name'])
    else:
        print("ERROR: not a python dictionary.")
