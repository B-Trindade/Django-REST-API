"""
Views for the recipe APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.RecipeSerializer

    # queryset represents the objs available for this viewset
    # in this case, bc its a model viewset, it expects a model
    # the set of all objects inside the Recipe model is the target
    # queryset desired for this viewset.
    queryset = Recipe.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user ONLY."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
