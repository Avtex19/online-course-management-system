from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from common.enums import PaginationFields


class CustomPageNumberPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = PaginationFields.PAGE_SIZE.value
    max_page_size = 100
    page_query_param = PaginationFields.PAGE.value

    def get_paginated_response(self, data):
        return Response({
            PaginationFields.COUNT.value: self.page.paginator.count,
            PaginationFields.NEXT.value: self.get_next_link(),
            PaginationFields.PREVIOUS.value: self.get_previous_link(),
            PaginationFields.RESULTS.value: data,
            PaginationFields.PAGE_INFO.value: {
                PaginationFields.CURRENT_PAGE.value: self.page.number,
                PaginationFields.TOTAL_PAGES.value: self.page.paginator.num_pages,
                PaginationFields.PAGE_SIZE.value: self.get_page_size(self.request),
            }
        })
