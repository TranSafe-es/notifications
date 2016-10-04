from rest_framework import serializers
from rest_framework.validators import ValidationError


class EmailSendSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        pass

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_internal_value(self, data):
        email = data.get('email')
        message = data.get('message')

        # Perform the data validation.
        if not email:
            raise ValidationError({
                'message': 'This field is required.'
            })
        if not message:
            raise ValidationError({
                'message': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'email': email,
            'message': message
        }


class MessengerSendSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        pass

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_internal_value(self, data):
        profile_id = data.get('profile_id')
        message = data.get('message')

        # Perform the data validation.
        if not profile_id:
            raise ValidationError({
                'message': 'This field is required.'
            })
        if not message:
            raise ValidationError({
                'message': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'profile_id': profile_id,
            'message': message
        }


class SMSSendSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        pass

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_internal_value(self, data):
        number = data.get('number')
        message = data.get('message')

        # Perform the data validation.
        if not number:
            raise ValidationError({
                'message': 'This field is required.'
            })
        if not message:
            raise ValidationError({
                'message': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'number': number,
            'message': message
        }
