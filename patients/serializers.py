from datetime import date

from rest_framework import serializers

from .models import Patient, Treatment


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "identification",
            "first_name",
            "last_name",
            "birth_date",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_birth_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "La fecha de nacimiento no puede ser futura."
            )

        return value

    def validate_identification(self, value):
        # La identificación debe estar compuesta únicamente
        # por caracteres numéricos.
        if not value.isdigit():
            raise serializers.ValidationError(
                "El número de identificación solo puede contener números."
            )

        return value


class TreatmentSerializer(serializers.ModelSerializer):
    filterset_fields = ["patient", "status", "name"]
    class Meta:
        model = Treatment
        fields = [
            "id",
            "patient",
            "name",
            "start_date",
            "end_date",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                "La fecha de finalización no puede ser anterior "
                "a la fecha de inicio."
            )

        return attrs