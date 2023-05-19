"""
Serializers for the user API View.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers
# SERIALIZERS: used to convert objects to and from python objects
# - e.g., it takes a JSON input, validates it and converts it into
# - either a python object or a model in our database.

# SERIALIZERS-BASE-CLASSES: there are different serializer base classes
# - such as serializers.serializer or serializers.ModelSerializers.
# - ModelSerializers allow us to validate and saves things to a model
# - previously specified and defined in our serializer.


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
