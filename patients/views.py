from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient, Treatment
from .serializers import PatientSerializer, TreatmentSerializer


class PatientViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Patient.objects.all().order_by("id")
    serializer_class = PatientSerializer
    filterset_fields = ["identification", "last_name"]
    http_method_names = ["get", "post", "patch", "head", "options"]

    @action(
        detail=True,
        methods=["get"],
        url_path="active-treatment"
    )
    def active_treatment(self, request, pk=None):

    # Obtiene el paciente utilizando el ID recibido
    # en la URL.
        patient = self.get_object()

    # Obtiene TODOS los tratamientos activos
    # relacionados con ese paciente.
        treatments = patient.treatments.filter(
            status=Treatment.Status.ACTIVE
        )

    # Si el paciente no tiene tratamientos activos,
    # devolvemos una lista vacía.
        if not treatments.exists():
            return Response(
                {
                    "has_active_treatment": False,
                    "treatments": []
                },
                status=status.HTTP_200_OK
            )

    # many=True indica que vamos a serializar
    # varios objetos Treatment.
        serializer = TreatmentSerializer(
            treatments,
            many=True
        )

        return Response(
            {
                "has_active_treatment": True,
                "treatments": serializer.data
            },
            status=status.HTTP_200_OK
        )

class TreatmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Treatment.objects.all().order_by("id")
    serializer_class = TreatmentSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]