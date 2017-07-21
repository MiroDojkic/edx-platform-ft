from django.shortcuts import render, redirect
from django.http import Http404
from lms.envs.common import STATE_CHOICES
from django_countries import countries
from edxmako.shortcuts import render_to_response, render_to_string
from .models import AffiliateEntity

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
    # courses = CustomCourseForEdX.objects.filter(coach=affiliate, enrollment_type=CustomCourseForEdX.PUBLIC, id=F('original_ccx_id'))

    return render_to_response('affiliates/show.html', {
        'affiliate': affiliate,
        'courses': []
    })

def new(request):
    return render_to_response('affiliates/form.html', {
        'affiliate': AffiliateEntity(),
        'state_choices': STATE_CHOICES,
        'countries': countries
    })

def create(request):
    affiliate = AffiliateEntity()
    
    for key in request.POST:
        if key == 'year_of_birth':
            setattr(affiliate, key, int(request.POST[key]))
        else:
            setattr(affiliate, key, request.POST[key])

    affiliate.save()

    url = reverse("affiliates_show", kwargs={'pk': affiliate.pk})
    return redirect(url)

def edit(request, pk):
    affiliate = AffiliateEntity.objects.get(pk=pk)

    # TODO implement interceptor
    allow_access = True

    # TODO: throw 403
    if not allow_access:
        raise Http404

    if request.method == 'POST':
        for key in request.POST:
            if key == 'year_of_birth':
                setattr(affiliate, key, int(request.POST[key]))
            else:
                setattr(affiliate, key, request.POST[key])

        affiliate.save()

        url = reverse("affiliates_show", kwargs={'pk': affiliate.pk})
        return redirect(url)
        
    
    return render_to_response('affiliates/form.html', {
        'affiliate': affiliate,
        'state_choices': STATE_CHOICES,
        'countries': countries
    })
    