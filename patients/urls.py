from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, TreatmentViewSet


router = DefaultRouter()

router.register(
    "patients",
    PatientViewSet,
    basename="patient"
)

router.register(
    "treatments",
    TreatmentViewSet,
    basename="treatment"
)

urlpatterns = router.urls