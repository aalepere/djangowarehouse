from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dwh_app_simple_history.serializers import PersonVehicleSerializer


@api_view(["POST"])
def PersonVehicle(request):
    """
    This view will be called through a POST request to add or update the information provided in
    the request
    """

    # Deserialize the information provided in the request
    ser = PersonVehicleSerializer(data=request.data)

    # Validate the information provided
    ser.is_valid(raise_exception=True)

    # Save the information in the datawarehouse
    ser.save()

    return Response({"All good, everything has been saved"})
