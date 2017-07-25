from django.shortcuts import render, redirect
from django.http import Http404
from lms.envs.common import STATE_CHOICES
from django_countries import countries
from edxmako.shortcuts import render_to_response, render_to_string
from .models import AffiliateEntity, AffiliateMembership
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    affiliate_name = request.POST.get('affiliate_name')
    affiliate_city = request.POST.get('affiliate_city')
    affiliate_state = request.POST.get('affiliate_state')

    affiliates = AffiliateEntity.objects.all()

    return render_to_response('affiliates/index.html', {
        'affiliates': affiliates,
        'affiliate_name': affiliate_name,
        'affiliate_city': affiliate_city,
        'affiliate_state': affiliate_state
    })


def show(request, pk):
    affiliate = AffiliateEntity.objects.get(pk=pk)

    return render_to_response('affiliates/show.html', {
        'affiliate': affiliate
    })


def new(request):
    return render_to_response('affiliates/form.html', {
        'affiliate': AffiliateEntity(),
        'state_choices': STATE_CHOICES,
        'countries': countries
    })


def create(request):
    affiliate = AffiliateEntity()
    
    # delete image from POST since we pull it from FILES    
    request.POST.pop('image', None)
    
    setattr(affiliate, 'image', request.FILES['image'])

    for key in request.POST:
        if key == 'year_of_birth':
            setattr(affiliate, key, int(request.POST[key]))
        else:
            setattr(affiliate, key, request.POST[key])

    affiliate.save()

    return redirect('affiliates:show', pk=affiliate.pk)


def edit(request, pk):
    affiliate = AffiliateEntity.objects.get(pk=pk)

    
    if request.method == 'POST':
        # delete image from POST since we pull it from FILES
        request.POST.pop('image', None)
        
        if request.FILES and request.FILES['image']:
            setattr(affiliate, 'image', request.FILES['image'])
        
        for key in request.POST:
            if key == 'year_of_birth':
                setattr(affiliate, key, int(request.POST[key]))
            else:
                setattr(affiliate, key, request.POST[key])

        affiliate.save()
    
        return redirect('affiliates:show', pk=affiliate.pk)  
    
    return render_to_response('affiliates/form.html', {
        'affiliate': affiliate,
        'state_choices': STATE_CHOICES,
        'countries': countries
    })
    

def add_member(request, pk):
    params = {
        'affiliate': AffiliateEntity.objects.get(pk=pk),
        'member_id': request.POST.get('member_id'),
        'role': request.POST.get('role'),
    }

    membership = AffiliateMembership.objects.create(**params)

    return render_to_response('affiliates/form.html', {
        'affiliate': params['affiliate']
    })


def remove_member(request, pk):
    params = {
        'affiliate': AffiliateEntity.objects.get(pk=pk),
        'member_id': request.DELETE.get('member_id')
    }

    AffiliateMembership.objects.filter(**params).delete()

    return render_to_response('affiliates/form.html', {
        'affiliate': params['affiliate']
    })
