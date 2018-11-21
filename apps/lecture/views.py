from django.db.models import Q
from django_filters import rest_framework as filters

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Lecture, LectureTime, Category, Subcategory
from .serializers import LectureSerializer, CategorySerializer, SubcategorySerializer


def convert_time(time):
    hours = time[:2]
    minutes = time[2:4]
    return hours + ':' + minutes


def filter_lecture_time(queryset, start, end, day=None):
    # start query for 'start <= time < end'
    start_gte = Q(timetable__start__gte=start)
    start_lte = Q(timetable__start__lt=end)
    # end query for 'start < time <= end'
    end_gte = Q(timetable__end__gt=start)
    end_lte = Q(timetable__end__lte=end)

    if day is None:
        return queryset.exclude((start_gte & start_lte) | (end_gte & end_lte))
    return queryset.exclude(Q(timetable__day=day) & ((start_gte & start_lte) | (end_gte & end_lte)))


def filter_lecture(queryset, name, value):
    """
    Filter a queryset with a timetable of given lectures.
    """
    query = [int(x) for x in value.split(',')]
    base = queryset
    result = None

    for uuid in query:
        times = LectureTime.objects.filter(lecture=uuid)
        for time in times:
            if result is None:
                result = filter_lecture_time(base, time.start, time.end, day=time.day)
            else:
                result.union(filter_lecture_time(base, time.start, time.end, day=time.day))

    return result


def filter_timetable(queryset, name, value):
    """
    Filter a queryset with a timetable.
    """
    query = [x.strip() for x in value.split(',')]
    base = queryset
    result = None
    days = {
        'mon': 0,
        'tue': 1,
        'wed': 2,
        'thu': 3,
        'fri': 4
    }

    for time in query:
        time = time.split(':')
        if len(time) == 1:
            # Time query only contains one argument: filters whole day.
            if result is None:
                result = base.exclude(timetable__day=days[time[0]])
            else:
                result = result.union(base.exclude(timetable__day=days[time[0]]))
        elif len(time) == 2:
            # Time query only contains two arguments: filters whole timetable.
            if result is None:
                result = filter_lecture_time(base, convert_time(time[0]), convert_time(time[1]))
            else:
                result = result.union(filter_lecture_time(base, convert_time(time[0]), convert_time(time[1])))
        else:
            # Time query contains full condition: filters with day and timetable.
            if result is None:
                result = filter_lecture_time(base, convert_time(time[1]), convert_time(time[2]), day=days[time[0]])
            else:
                result = result.union(
                    filter_lecture_time(base, convert_time(time[1]), convert_time(time[2])), day=days[time[0]])

    return result


def filter_selected(queryset, name, value):
    """
    Filter a queryset with a lecture code.
    """
    query = [x.strip() for x in value.split(',')]
    base = queryset
    result = None

    for code in query:
        # Filter out lectures that has different code with our query.
        if result is None:
            result = base.filter(code=code)
        else:
            result = result.union(base.filter(code=code))

    # TODO: Distinct all timetables in result queryset.
    return result


class LectureSearchFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    professor = filters.CharFilter(field_name='professor', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', method='filter_category')
    subcategory = filters.CharFilter(field_name='subcategory', method='filter_subcategory')
    lecture = filters.CharFilter(field_name='lecture', method=filter_lecture)
    timetable = filters.CharFilter(field_name='timetable', method=filter_timetable)

    class Meta:
        model = Lecture
        fields = (
            'id',
            'code',
            'title',
            'point',
            'category',
            'subcategory',
            'professor',
            'lecture',
            'timetable',
        )

    def filter_category(self, queryset, name, value):
        category = Category.CATEGORIES.get(value, Category.NONE)
        return queryset.filter(category__category__icontains=category)

    def filter_subcategory(self, queryset, name, value):
        subcategory = Subcategory.SUBCATEGORIES.get(value, Subcategory.NONE)
        return queryset.filter(subcategory__subcategory__icontains=subcategory)


class LectureSearchAPIView(ListAPIView):
    """
    Search a lecture with URL parameters. Returns list of lectures.
    """
    serializer_class = LectureSerializer
    queryset = Lecture.objects.prefetch_related('timetable').all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LectureSearchFilter

    def list(self, request, *args, **kwargs):
        lectures = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(lectures)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(lectures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LectureQueryFilter(filters.FilterSet):
    timetable = filters.CharFilter(field_name='timetable', method=filter_timetable)
    fixed = filters.CharFilter(field_name='fixed', method=filter_lecture)
    selected = filters.CharFilter(field_name='selected', method=filter_selected)

    class Meta:
        model = Lecture
        fields = (
            # NOTE: Order of this list is IMPORTANT - timetable always comes first.
            'timetable',
            'fixed',
            'selected',
        )


class LectureQueryAPIView(ListAPIView):
    """
    Query a lectures with given URL parameters. Returns list of all the possible lectures.
    """
    serializer_class = LectureSerializer
    queryset = Lecture.objects.prefetch_related('timetable').all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LectureQueryFilter

    def list(self, request, *args, **kwargs):
        lectures = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(lectures)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(lectures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SubcategoryListAPIView(ListAPIView):
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.all()
