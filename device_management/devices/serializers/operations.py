from rest_framework import serializers
from devices.models import Reservation, Loan, Return


class ReservationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    device_serial = serializers.CharField(source='device.serial_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'user_username', 'device', 'device_name', 'device_serial',
            'reserved_from', 'reserved_until', 'status', 'status_display',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, attrs):
        if attrs.get('reserved_from') and attrs.get('reserved_until'):
            if attrs['reserved_from'] >= attrs['reserved_until']:
                raise serializers.ValidationError("Reserved until must be after reserved from")
        return attrs


class LoanSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    manager_username = serializers.CharField(source='manager.username', read_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    device_serial = serializers.CharField(source='device.serial_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Loan
        fields = [
            'id', 'user', 'user_username', 'device', 'device_name', 'device_serial',
            'manager', 'manager_username', 'loaned_at', 'due_date',
            'status', 'status_display', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['loaned_at', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        device = attrs.get('device')
        if device and not device.is_available():
            raise serializers.ValidationError("Device is not available for loan")
        return attrs


class ReturnSerializer(serializers.ModelSerializer):
    loan_device = serializers.CharField(source='loan.device.name', read_only=True)
    loan_user = serializers.CharField(source='loan.user.username', read_only=True)
    inspected_by_username = serializers.CharField(source='inspected_by.username', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    
    class Meta:
        model = Return
        fields = [
            'id', 'loan', 'loan_device', 'loan_user',
            'returned_at', 'condition', 'condition_display',
            'inspected_by', 'inspected_by_username', 'notes', 'created_at'
        ]
        read_only_fields = ['returned_at', 'created_at']