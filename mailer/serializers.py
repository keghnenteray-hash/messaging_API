from rest_framework import serializers
import re

class EmailSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        error_messages = { 'blank': 'Name field Cannot be Empty', 'max_length': 'Name must be under 100 characters' }
    )

    email = serializers.EmailField(
        error_messages = { 'blank': 'Email field Cannot bee Empty', 'invalid': 'Enter a valid email address(example@gmail.com)' }
    )

    subject = serializers.CharField(
        max_length=200,
        required=False,
        default = 'New Contact Form Submission',
    )

    message = serializers.CharField (
        min_length = 10,
        max_length = 5000,
        error_messages = { 
            'blank': 'Message field Cannot be Empty', 
            'min_length': 'Message must be at least 10 characters', 
            'max_length': 'Message must be under 5000 characters' 
        }
    )

    def validate_name(self, value):
        if re.search(r'<[^>]+>_-=%@#€', value):
            raise serializers.ValidationError('Name contains invalid Characters')
        return value.strip()
    
    def validate_message(self, value):
        return value.strip()