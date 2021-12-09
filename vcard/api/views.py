import json
import string

from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup


def generate_data(service, location):
    url = "https://panoramafirm.pl/" + service + "/" + location
    request = requests.get(url)
    soup = BeautifulSoup(request.text)
    list = soup.find_all('li', attrs={'class': 'card top-link company-item py-2 container my-2'})
    return_list = []
    for element in list:
        dict = {}
        name = element.find('a', attrs={'class': 'company-name addax addax-cs_hl_hit_company_name_click'})
        dict['name'] = name.text.translate({ord(c): None for c in string.whitespace})
        address = element.find('div', attrs={'class': 'address'})
        dict['address'] = address.text.translate({ord(c): None for c in string.whitespace})
        phone = element.find('a', attrs={'class': 'icon-telephone addax addax-cs_hl_phonenumber_click'})
        dict['phone'] = phone.attrs['title'].translate({ord(c): None for c in string.whitespace})
        return_list.append(dict)

    return return_list


def generate_vcard(dict):
    vcf_file = dict['name'] + ".vcf"
    card = ['BEGIN:VCARD', 'VERSION:2.1',
            f'N:{dict["name"]}',
            f'TEL;WORK;VOICE:{dict["phone"]}',
            f'ADR;WORK;PREF:;;{dict["address"]}',
            ]
    write_vcard(vcf_file, card)
    return vcf_file


def write_vcard(f, vcard):
    with open(f, 'w') as f:
        f.writelines([l + '\n' for l in vcard])


def make_html_file(data):
    html = ""
    for element in data:
        file = generate_vcard(element)
        html += "<h1> " + element['name'] + "</h1>"
        html += "<h2> " + element['phone'] + "</h2>"
        html += "<h3> " + element['address'] + "</h3>"
        html += "<a href=\" " + file + "\" > Generate vcard </a>"
        html += "<br><br>"
    return html


@csrf_exempt
def vcard(request):
    body_unicode = request.body.decode()
    if body_unicode == "":
        return HttpResponseNotFound("Request body is empty")
    body = json.loads(body_unicode)
    print(body)
    service = body['service']
    location = body['location']
    data = generate_data(service, location)
    return HttpResponse(make_html_file(data))
