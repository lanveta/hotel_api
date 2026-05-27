from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.decorators import action

from .models import RoomCategory, Room, Booking, Amenity
from .serializers import RoomCategorySerializer, RoomSerializer, BookingSerializer, AmenitySerializer

class RoomCategoryViewSet(viewsets.ModelViewSet):
    """Представление для работы с категориями номеров.
    Поддерживает все CRUD-операции, включая массовое создание,
    обновление и удаление. GET-запросы кешируются на 15 минут.
    Фильтрация списка возможна по GET-параметру `name` (поиск по подстроке).
    """
    serializer_class = RoomCategorySerializer
    queryset = RoomCategory.objects.all()

    def get_queryset(self):
        """Фильтрация категорий номеров по названию."""
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одной или нескольких категорий номеров."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одной категории номеров или списка."""
        many = isinstance(request.data, list)
        if many:
            instances = [RoomCategory.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одной или нескольких категорий номеров."""
        many = isinstance(request.data, list)
        if many:
            instances = [RoomCategory.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одной категории номеров или списка через параметр ids."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            RoomCategory.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Массовое удаление категорий номеров по списку ID."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            RoomCategory.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Parameter "ids" is required'}, status=status.HTTP_400_BAD_REQUEST)


class RoomViewSet(viewsets.ModelViewSet):
    """Представление для работы с номерами.
    Поддерживает все CRUD-операции, включая массовые создание, обновление,
    удаление. GET-запросы кешируются. Можно фильтровать по категории и номеру комнаты.
    """
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get_queryset(self):
        """Фильтрация номеров по категории и номеру комнаты."""
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        room_number = self.request.query_params.get('room_number')
        if category_id:
            qs = qs.filter(category_id=category_id)
        if room_number:
            qs = qs.filter(room_number=room_number)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одного или нескольких номеров."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одного номера или списка."""
        many = isinstance(request.data, list)
        if many:
            instances = [Room.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одного или нескольких номеров."""
        many = isinstance(request.data, list)
        if many:
            instances = [Room.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одного номера или списка через параметр ids."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Room.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Массовое удаление номеров по списку ID."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Room.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Parameter "ids" is required'}, status=status.HTTP_400_BAD_REQUEST)


class BookingViewSet(viewsets.ModelViewSet):
    """Представление для работы с бронированиями.
    Поддерживает все CRUD-операции с массовыми действиями.
    GET-запросы кешируются, фильтрация по `room_id` и `guest_name`.
    """
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        """Фильтрация бронирований по номеру и имени гостя."""
        qs = super().get_queryset()
        room_id = self.request.query_params.get('room_id')
        guest_name = self.request.query_params.get('guest_name')
        if room_id:
            qs = qs.filter(room_id=room_id)
        if guest_name:
            qs = qs.filter(guest_name__icontains=guest_name)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одного или нескольких бронирований."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одного бронирования или списка."""
        many = isinstance(request.data, list)
        if many:
            instances = [Booking.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одного или нескольких бронирований."""
        many = isinstance(request.data, list)
        if many:
            instances = [Booking.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одного бронирования или списка через параметр ids."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Booking.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Массовое удаление бронирований по списку ID."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Booking.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Parameter "ids" is required'}, status=status.HTTP_400_BAD_REQUEST)
    

class AmenityViewSet(viewsets.ModelViewSet):
    """Представление для работы с удобствами.
    Поддерживает все CRUD-операции, включая массовые действия.
    GET-запросы кешируются.
    """
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()

    def get_queryset(self):
        """Получение всех удобств (без фильтрации)."""
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одного или нескольких удобств."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одного удобства или списка."""
        many = isinstance(request.data, list)
        if many:
            instances = [Amenity.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одного или нескольких удобств."""
        many = isinstance(request.data, list)
        if many:
            instances = [Amenity.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одного удобства или списка через параметр ids."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Amenity.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Массовое удаление удобств по списку ID."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Amenity.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Parameter "ids" is required'}, status=status.HTTP_400_BAD_REQUEST)