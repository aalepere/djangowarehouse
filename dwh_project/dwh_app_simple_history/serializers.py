from rest_framework import serializers

from dwh_app_simple_history.models import Person, PersonVehicle, Vehicle


class VehicleSerializer(serializers.Serializer):
    """
    Nested serializer within the JSON source; in this example all vehicles that belongs to the
    person are nested in the JON as a list of all active vehicles.
    """

    registration_plate = serializers.CharField(max_length=100)


class PersonVehicleSerializer(serializers.Serializer):
    """
    Serializer that will be used to deserialize the json to be then imported in the datawarehouse
    """

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    vehicles = VehicleSerializer(many=True)

    def save(self):
        """
        Overwrite the save function on the seriliazer to be able to control how we want to
        insert/update the data provided by the source in our datawarehouse.
        """

        # First update or create the person
        person_obj, created = Person.objects.update_or_create(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            defaults={"email": self.validated_data["email"]},
        )

        # Then create each Vehicle and link it to the person created before
        for vehicle in self.validated_data["vehicles"]:
            vehicle_obj = Vehicle.objects.create(registration_plate=vehicle["registration_plate"])
            personvehicle_obj = PersonVehicle.objects.update_or_create(
                vehicle=vehicle_obj, defaults={"person": person_obj}
            )
