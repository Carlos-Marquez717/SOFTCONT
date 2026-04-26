from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate_queryset(request, queryset, per_page):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page")

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
