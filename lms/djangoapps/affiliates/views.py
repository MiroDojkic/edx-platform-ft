from django.shortcuts import render, redirect
from django.http import Http404
from lms.envs.common import STATE_CHOICES
from django_countries import countries
from edxmako.shortcuts import render_to_response, render_to_string
from .models import AffiliateEntity, AffiliateMembership
from django.contrib.auth.models import User
from lms.djangoapps.instructor.views.tools import get_student_from_identifier
from .decorators import only_program_director, only_staff

# Create your views here.
def index(request):
    affiliate_name = request.POST.get('affiliate_name', '')
    affiliate_city = request.POST.get('affiliate_city', '')
    affiliate_state = request.POST.get('affiliate_state', '')

    filters = {}
    if affiliate_name:
        filters['name__icontains'] = affiliate_name
    if affiliate_city:
        filters['city__icontains'] = affiliate_city
    if affiliate_state:
        filters['state'] = affiliate_state


    affiliates = AffiliateEntity.objects.filter(**filters)

    return render_to_response('affiliates/index.html', {
        'affiliates': affiliates,
        'affiliate_name': affiliate_name,
        'affiliate_city': affiliate_city,
        'affiliate_state': affiliate_state,
        'state_choices': STATE_CHOICES
    })


def show(request, slug):
    affiliate = AffiliateEntity.objects.get(slug=slug)

    return render_to_response('affiliates/show.html', {
        'affiliate': affiliate
    })


@only_program_director
def new(request):
    return render_to_response('affiliates/form.html', {
        'affiliate': AffiliateEntity(),
        'state_choices': STATE_CHOICES,
        'countries': countries,
        'role_choices': AffiliateMembership.role_choices
    })


@only_program_director
def create(request):
    affiliate = AffiliateEntity()
    post_data = request.POST.copy().dict()

    program_director_identifier = post_data.pop('member_identifier', None)

    # delete image from POST since we pull it from FILES
    post_data.pop('image', None)

    if request.FILES and request.FILES['image']:
        setattr(affiliate, 'image', request.FILES['image'])

    for key in post_data:
        if key == 'year_of_birth':
            setattr(affiliate, key, int(post_data[key]))
        else:
            setattr(affiliate, key, post_data[key])

    affiliate.save()

    # SurveyGizmo functionality to automatically add Program Director upon creation
    if program_director_identifier:
        member = get_student_from_identifier(program_director_identifier)
        AffiliateMembership.objects.create(affiliate=affiliate, member=member, role='staff')

    return redirect('affiliates:show', slug=affiliate.slug)


@only_staff
def edit(request, slug):
    affiliate = AffiliateEntity.objects.get(slug=slug)

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

        return redirect('affiliates:show', slug=affiliate.slug)

    return render_to_response('affiliates/form.html', {
        'affiliate': affiliate,
        'state_choices': STATE_CHOICES,
        'countries': countries,
        'role_choices': AffiliateMembership.role_choices,
        'is_program_director':request.user.is_staff or AffiliateMembership.objects.filter(member=request.user, affiliate=affiliate, role='staff').exists()
    })

@only_program_director
def delete(request, slug):
    AffiliateEntity.objects.get(slug=slug).delete()

    return redirect('affiliates:index')


@only_staff
def add_member(request, slug):
    member = get_student_from_identifier(request.POST.get('member_identifier'))
    params = {
        'affiliate': AffiliateEntity.objects.get(slug=slug),
        'member': member,
        'role': request.POST.get('role'),
    }

    membership = AffiliateMembership.objects.create(**params)

    return redirect('affiliates:edit', slug=slug)


@only_staff
def remove_member(request, slug, member_id):
    params = {
        'affiliate': AffiliateEntity.objects.get(slug=slug),
        'member_id': member_id
    }

    AffiliateMembership.objects.filter(**params).delete()

    return redirect('affiliates:edit', slug=slug)

