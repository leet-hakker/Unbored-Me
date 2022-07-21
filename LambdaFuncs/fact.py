import urllib.request as requests
import json


def get_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    r = requests.urlopen(url)
    data = r.read().decode("utf-8")
    j = json.loads(data)

    return j


def fact_to_html(data):
    html = "<!DOCTYPE html>"
    html += f"<p id='fact'>{data['text']}</p>"

    return html


def lambda_handler(event, context):
    fact = get_fact()
    html = fact_to_html(fact)

    return {
        'statusCode': 200,
        'headers': {
            'content-type': 'text/html'
        },
        'body': html
    }
