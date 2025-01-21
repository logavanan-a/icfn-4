


from django.core.paginator import Paginator #import Paginator
from icfn_new.settings import PAGINATION_SIZE

# PAGE_SIZE = 6

def frontend_pagination(request, query_set):
    paginator = Paginator(query_set,PAGINATION_SIZE) #which data want to display and how much data in one page should show
    page_number = request.GET.get('page')  # get the value of the page that coming in the URL
    page_obj = paginator.get_page(page_number) # count of pages
    return page_obj
