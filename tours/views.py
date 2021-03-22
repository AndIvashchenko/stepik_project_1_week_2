import random

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404

from tours.data import tours, title, subtitle, description, departures
# Create your views here.


def main_view(request):
    rand_tours = dict(random.sample(tours.items(), 6))
    return render(request, 'tours/index.html', {
        'title': title,
        'description': description,
        'subtitle': subtitle,
        'tours': rand_tours,
    })


def departure_view(request, departure):
    try:
        departure_active = departures[departure]
    except KeyError:
        raise Http404
    departure_tours = []
    numb_of_tours = 0
    for i in tours:
        if tours[i]['departure'] == departure:
            departure_tours.append(tours[i])
            departure_tours[numb_of_tours]['tour_id'] = i
            numb_of_tours += 1

    departure_tours.sort(key=lambda dictionary: dictionary['nights'])
    min_nights = departure_tours[0]['nights']
    max_nights = departure_tours[numb_of_tours - 1]['nights']

    departure_tours.sort(key=lambda dictionary: dictionary['price'])
    min_price = departure_tours[0]['price']
    max_price = departure_tours[numb_of_tours-1]['price']
    return render(request, 'tours/departure.html', {
        'departure': departure_active,
        'departure_tours': departure_tours,
        'numb_of_tours': numb_of_tours,
        'min_price': min_price,
        'max_price': max_price,
        'min_nights': min_nights,
        'max_nights': max_nights,
    })


def tour_view(request, tour_id):
    try:
        tour = tours[tour_id]
    except KeyError:
        raise Http404
    return render(request, 'tours/tour.html', {
        'tour': tour,
        'departure': departures[tour['departure']],
    })


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
