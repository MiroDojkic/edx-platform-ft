from django.http import HttpResponseNotFound
from functools import wraps
from .models import AffiliateMembership

def only_program_director(function):
    """Only allow access to global staff or affiliate staff user(Program Director)"""
    @wraps(function)
    def wrapped_view(request, pk, *args, **kwargs):
        """Wrapper for the view function."""
        if request.user.is_anonymous():
            return HttpResponseNotFound()
        elif request.user.is_staff:
            return function(request, pk, *args, **kwargs)
        else:
            has_pd_role_in_affiliate = AffiliateMembership.objects.filter(member=request.user, affiliate_id=pk, role='staff').exists()

            if has_pd_role_in_affiliate:
                return function(request, pk, *args, **kwargs)

    return wrapped_view
