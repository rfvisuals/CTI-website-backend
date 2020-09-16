from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .serializers import OrganizationSerializer, LinkSerializer, FAQSerializer
from ..models import Organization, Link, FAQ


class OrganizationViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "name"


class LinkViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()


class FAQViewSet(ReadOnlyModelViewSet):
    """
    FAQ's are managed via the Django admin interface. The API provides a list
    of live FAQ's in the order of most viewed. This viewset also provides an
    endpoint for tracking when a user clicks on the question to view the answer.
    """
    serializer_class = FAQSerializer
    queryset = FAQ.objects.filter(live=True).all().order_by('-view_count', 'question')

    @action(detail=True, methods=['post'])
    def increment_count(self, request, pk=None):
        faq = FAQ.objects.filter(pk=pk).first()
        if faq:
            try:
                FAQ.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

            return Response("", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(f"FAQ {pk} not found", status=status.HTTP_404_NOT_FOUND)
