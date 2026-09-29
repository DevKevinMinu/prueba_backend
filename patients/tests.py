from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Patient, Treatment


class PatientAPITests(APITestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            identification="10000001",
            first_name="Juan",
            last_name="Gomez",
            birth_date="1998-05-20",
        )

    def test_create_patient(self):
        url = reverse("patient-list")

        data = {
            "identification": "10000002",
            "first_name": "Maria",
            "last_name": "Lopez",
            "birth_date": "1995-04-10",
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Patient.objects.count(),
            2
        )

        self.assertEqual(
            response.data["first_name"],
            "Maria"
        )

    def test_get_patients(self):
        url = reverse("patient-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_patient_with_patch(self):
        url = reverse(
            "patient-detail",
            kwargs={"pk": self.patient.id}
        )

        data = {
            "last_name": "Rodriguez"
        }

        response = self.client.patch(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.patient.refresh_from_db()

        self.assertEqual(
            self.patient.last_name,
            "Rodriguez"
        )

    def test_birth_date_cannot_be_in_future(self):
        url = reverse("patient-list")

        future_date = (
            date.today() + timedelta(days=1)
        ).isoformat()

        data = {
            "identification": "10000003",
            "first_name": "Pedro",
            "last_name": "Ramirez",
            "birth_date": future_date,
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "birth_date",
            response.data
        )

        self.assertEqual(
            Patient.objects.count(),
            1
        )

    def test_patient_not_found(self):
        url = reverse(
            "patient-detail",
            kwargs={"pk": 99999}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_put_patient_not_allowed(self):
        url = reverse(
            "patient-detail",
            kwargs={"pk": self.patient.id}
        )

        data = {
            "identification": self.patient.identification,
            "first_name": self.patient.first_name,
            "last_name": "NuevoApellido",
            "birth_date": str(self.patient.birth_date),
        }

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_identification_only_numbers(self):
        url = reverse("patient-list")

        data = {
            "identification": "ABC123",
            "first_name": "Pedro",
            "last_name": "Ramirez",
            "birth_date": "1995-04-10",
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "identification",
            response.data
        )

        self.assertEqual(
            Patient.objects.count(),
            1
        )


class TreatmentAPITests(APITestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            identification="20000001",
            first_name="Carlos",
            last_name="Perez",
            birth_date="1990-01-10",
        )

    def test_create_treatment(self):
        url = reverse("treatment-list")

        data = {
            "patient": self.patient.id,
            "name": "Fisioterapia",
            "start_date": "2026-09-21",
            "end_date": None,
            "status": "active",
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Treatment.objects.count(),
            1
        )

        self.assertEqual(
            response.data["status"],
            "active"
        )

    def test_update_treatment_with_patch(self):
        treatment = Treatment.objects.create(
            patient=self.patient,
            name="Fisioterapia",
            start_date="2026-09-21",
            end_date=None,
            status="active",
        )

        url = reverse(
            "treatment-detail",
            kwargs={"pk": treatment.id}
        )

        data = {
            "status": "completed",
            "end_date": "2026-09-25",
        }

        response = self.client.patch(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        treatment.refresh_from_db()

        self.assertEqual(
            treatment.status,
            "completed"
        )

        self.assertEqual(
            str(treatment.end_date),
            "2026-09-25"
        )

    def test_end_date_cannot_be_before_start_date(self):
        url = reverse("treatment-list")

        data = {
            "patient": self.patient.id,
            "name": "Tratamiento inválido",
            "start_date": "2026-09-21",
            "end_date": "2026-09-10",
            "status": "completed",
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "non_field_errors",
            response.data
        )

        self.assertEqual(
            Treatment.objects.count(),
            0
        )

    def test_get_active_treatments(self):
        treatment_1 = Treatment.objects.create(
            patient=self.patient,
            name="Fisioterapia",
            start_date="2026-09-21",
            end_date=None,
            status="active",
        )

        treatment_2 = Treatment.objects.create(
            patient=self.patient,
            name="Terapia ocupacional",
            start_date="2026-09-22",
            end_date=None,
            status="active",
        )

        url = reverse(
            "patient-active-treatment",
            kwargs={"pk": self.patient.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            response.data["has_active_treatment"]
        )

        self.assertEqual(
            len(response.data["treatments"]),
            2
        )

        treatment_ids = [
            treatment["id"]
            for treatment in response.data["treatments"]
        ]

        self.assertIn(
            treatment_1.id,
            treatment_ids
        )

        self.assertIn(
            treatment_2.id,
            treatment_ids
        )

    def test_patient_without_active_treatment(self):
        url = reverse(
            "patient-active-treatment",
            kwargs={"pk": self.patient.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            response.data["has_active_treatment"]
        )

        self.assertEqual(
            response.data["treatments"],
            []
        )

    def test_put_treatment_not_allowed(self):
        treatment = Treatment.objects.create(
            patient=self.patient,
            name="Fisioterapia",
            start_date="2026-09-21",
            end_date=None,
            status="active",
        )

        url = reverse(
            "treatment-detail",
            kwargs={"pk": treatment.id}
        )

        data = {
            "patient": self.patient.id,
            "name": "Nuevo tratamiento",
            "start_date": "2026-09-21",
            "end_date": None,
            "status": "active",
        }

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )