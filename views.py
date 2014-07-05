from django.http import HttpResponse
from ldap_profile.models import Profile, ProfileFormateur, ProfileEncadrant,\
    ProfileParticipant
from django.core.exceptions import FieldError, MultipleObjectsReturned
from django.template import RequestContext
from django.shortcuts import render_to_response


def hello(request):
    return HttpResponse("Hello world")


def _check_profile_result(profiles):
    if len(profiles) > 1:
        raise(MultipleObjectsReturned('Email must be unique'))
    else:
        return profiles[0]


# FIXME: Move this method in the Profile class
# FIXME: Do it with a single LDAP call instead of 2 as actually
def _get_profile(user):
    profile = Profile.objects.filter(email=user.email)
    profile = _check_profile_result(profile)
    profile_types = {
        'ou=formateur': ProfileFormateur,
        'ou=encadrant': ProfileEncadrant,
        'ou=participant': ProfileParticipant,
    }
    profile_object = None
    for profile_type in profile_types:
        if profile_type in profile.dn:
            profile_object = profile_types[profile_type]
            break
    if profile_object:
        profile = getattr(profile_object,
                          'objects').filter(email=user.email)
        profile = _check_profile_result(profile)
    else:
        raise(FieldError('Unknown profile type. Must be in {}'.
                         format(profile_type.keys())))
    return profile


def view_profile(request):
    profile = _get_profile(request.user)
    profile_list = [(field.name, [getattr(profile, field.name), ])
                    for field in profile._meta.fields]
    return render_to_response('profile.html', {
        'profile': profile_list, }, RequestContext(request))


def change_password(request):
    pass


def change_email(request):
    pass


def edit_profile(request):
    pass


# End
