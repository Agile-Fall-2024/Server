from rest_framework import filters


class IsAuthorFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        my = bool(request.query_params.get('my', None))
        if my:
            return queryset.filter(author=request.user)
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'my',
                'required': False,
                'in': 'query',
                'description': 'if true, filter objects that user is the author',
                'allowEmptyValue': True,
                'schema': {
                    'type': 'boolean',
                },
            },
        ]


def parse_int_or_none(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


class PriceFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        min_price = parse_int_or_none(request.query_params.get('min_price', None))
        max_price = parse_int_or_none(request.query_params.get('max_price', None))
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'min_price',
                'required': False,
                'in': 'query',
                'description': 'indicated minimum price',
                'schema': {
                    'type': 'integer',
                },
            },
            {
                'name': 'max_price',
                'required': False,
                'in': 'query',
                'description': 'indicated maximum price',
                'schema': {
                    'type': 'integer',
                },
            },
        ]

class CategoryFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        category = parse_int_or_none(request.query_params.get('category', None))
        if category:
            return queryset.filter(category=category)
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'category',
                'required': False,
                'in': 'query',
                'description': 'category filter',
                'schema': {
                    'type': 'integer',
                },
            },
        ]