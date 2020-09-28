from staticpages.models import TermsPage
from django.shortcuts import render

class LicenceMiddleware:

    # One-time configuration and initialization.
    def __init__(self, get_response):
        self.get_response = get_response


    # Code to be executed for each request before
    # the view (and later middleware) are called.
    def __call__(self, request):

        response = self.get_response(request)
        if request.user.is_superuser:
            return response
        else:
            if request.user.is_authenticated:
                latest_term = TermsPage.objects.latest('version_number')
                if request.user.accepted_eula_version == latest_term.version_number:
                    return response
                else:
                    return render(request, "users/accept_terms_view.html", {'term_object': latest_term})
            else:
                return response

            # if check_date:
            #     return response
            # else:
            #     return render(request, 'licence_expired.html')
