from django.core.paginator import Paginator


def paginator_create(request, list, count):
    paginator = Paginator(list, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
