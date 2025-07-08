from gearcore.wishlist.models import Wishlist


class GoodsMixins:
    def get_wishlist(self, request):
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
            return Wishlist.objects.filter(**query_kwargs).first()
            # query_kwargs = {"session_key": request.session.session_key} # # noqa: ERA001
        return None
