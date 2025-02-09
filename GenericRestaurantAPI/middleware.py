from django.http import HttpResponseForbidden
from restaurantapi.models import Owner
class OwnerIdMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        owner_id = request.META.get('HTTP_OWNER_ID', None)
        print(request.META.get('User_Agent', None))
        if owner_id is None or owner_id == '':
            return HttpResponseForbidden('Missing Owner Id Header')
        ownerInstance = Owner.objects.get(pk=owner_id)
        if not ownerInstance:
            return HttpResponseForbidden('Owner with id: {0} not exists'.format(owner_id))
        request.ownerId = owner_id
        return self.get_response(request)
        