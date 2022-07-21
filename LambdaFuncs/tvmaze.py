import random
import urllib
import urllib.request as requests
import json


def get_random_show():
    # Another hardcoded implementation for the largest
    # show id. Could find the maximum every day or so,
    # but it's rude to send so many requests like that.
    # TODO: Exact, efficient way of finding max ID
    show_id = random.randrange(1, 63177)

    try:
        r = requests.urlopen(f'https://api.tvmaze.com/shows/{show_id}')
    except urllib.error.HTTPError:
        return get_random_show()
    data = r.read()
    j = json.loads(data)

    return j


def show_data_to_html(data):
    html = ""
    html += f"<a href=\"{data['url']}\" target=\"_blank\">"
    html += f"<h3 id='showtitle'>{data['name']}</h3>"
    html += "</a>"
    html += f"<img src='{data['image']['medium']}' alt=\"Image for '{data['name']}'\">"
    html += data['summary']

    return html


def lambda_handler(event, context):
    show_data = get_random_show()
    html = show_data_to_html(show_data)

    return {
        "statusCode": 200,
        "body": html,
        "headers": {
            "content-type": "text/html"
            }
        }
