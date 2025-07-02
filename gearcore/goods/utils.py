from django.contrib.postgres.search import SearchHeadline
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank
from django.contrib.postgres.search import SearchVector

from gearcore.goods.models import Motorcycle


def q_search(query):
    min_length = 5
    if query.isdigit() and len(query) <= min_length:
        return Motorcycle.objects.filter(id=int(query))

    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = Motorcycle.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color:yellow;">',
            stop_sel="</span>",
        ),
    )

    return result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color:yellow;">',
            stop_sel="</span>",
        ),
    )
