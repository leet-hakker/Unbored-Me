import json
import urllib
import urllib.request as requests
import random


def check_if_olid_valid(olid):
    r = requests.urlopen(f"https://openlibrary.org/books/{olid}.json")
    status = r.status
    if status != 200:
        print("Invalid thrown")
        return False

    data = r.read()
    j = json.loads(data.decode("utf-8"))

    # If the page has been deleted
    if j['type']['key'] == "/type/delete":
        print("Deleted thrown")
        return False

    return True


def gen_random_valid_olid():
    prefix = "OL"
    # 38852000 is closest approximation of how many books
    # exist in the openLibrary
    # TODO: find way to get exact number
    num_id = str(random.randrange(1, 38852000))
    suffix = "M"

    olid = prefix+num_id+suffix

    if not check_if_olid_valid(olid):
        return "OL7353617M"

    return olid


def get_author_name(author):
    r = requests.urlopen(f'https://openlibrary.org{author["key"]}.json')
    data = r.read()
    j = json.loads(data.decode("utf-8"))

    return j['name']


def retrieve_book_info(olid):
    # TODO: Covers are not robust, and sometimes fail to be found.
    cover_url = f'https://covers.openlibrary.org/b/olid/{olid}-M.jpg?default=false'
    book_info_url = f'https://openlibrary.org/books/{olid}.json'

    try:
        r = requests.urlopen(cover_url)
    except urllib.error.HTTPError:
        cover_url = 'https://openlibrary.org/images/icons/avatar_book-lg.png'

    # TODO: handle 500 errors.
    r = requests.urlopen(book_info_url)
    data = r.read()

    book_info = json.loads(data.decode("utf-8"))

    if 'authors' not in book_info.keys():
        authors = book_info['publishers']
        author_names = authors
    else:
        authors = book_info['authors']
        author_names = [get_author_name(author) for author in authors]

    condensed_info = {
                        'authors': author_names,
                        'title': book_info['title'],
                        'cover': cover_url,
                        'olid': olid,
                        'url': f'https://openlibrary.org/books/{olid}'
                     }

    return condensed_info


def get_random_book():
    olid = gen_random_valid_olid()

    return retrieve_book_info(olid)


def book_info_to_html(info):
    html = ""
    html += f"<a id=\"booklink\" href=\"{info['url']}\" target=\"_blank\">"
    html += f"<img id='bookcover' src=\"{info['cover']}\" alt=\"Cover of '{info['title']}'\" />"
    html += "</a>"
    html += "<h3 class='booktitle'>" + info['title'] + "</h3>"

    if len(info['authors']) > 1:
        html += "<h5>Authors: "
        html += ", ".join([author for author in authors])
        html += "</h5>"
    else:
        html += f"<h5 id='author'>Author: {info['authors'][0]}</h5>"

    html += f"<p id='olid'>OLID: {info['olid']}</p>"

    return html


def lambda_handler(event, context):
    olid = gen_random_valid_olid()
    openlib_data = retrieve_book_info(olid)
    html = book_info_to_html(openlib_data)

    return {
        "statusCode": 200,
        "body": html,
        "headers": {
            "content-type": "text/html"
            }
        }
