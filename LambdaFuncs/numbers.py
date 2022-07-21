import urllib.request as requests


def get_joke():
    url = "http://numbersapi.com/random/math"
    r = requests.urlopen(url)
    data = r.read().decode("utf-8")

    return data


def joke_to_html(text):
    text = text.replace('\n', '<br>')

    html = "<!DOCTYPE html>"
    html += "<p id='facttext'>"
    html += text
    html += "</p>"

    return html


def lambda_handler(event, context):
    joke = get_joke()
    html = joke_to_html(joke)

    return {
        'statusCode': 200,
        'headers': {
            'content-type': 'text/html'
        },
        'body': html
    }
