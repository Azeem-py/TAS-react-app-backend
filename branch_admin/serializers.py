from rest_framework import serializers, validators
from .models import *
from auth_api.models import CustomUser


valid = {
    "required": True,
}


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentInfo

        fields = "__all__"

        extra_kwargs = {
            "firstName": valid,
            "lastName": valid,
            "branch": {"required": True},
            "country": {"required": True},
            "state": {"required": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        ParentInfo.objects.all(), "email has been used"
                    )
                ],
            },
            "address": {
                "required": True,
            },
            "phoneNumber": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        ParentInfo.objects.all(), "number has been used"
                    )
                ],
            },
            "homeNumber": {
                "allow_blank": True,
                "validators": [
                    validators.UniqueValidator(
                        ParentInfo.objects.all(), "number has been used"
                    )
                ],
            },
            "workNumber": {
                "allow_blank": True,
                "validators": [
                    validators.UniqueValidator(
                        ParentInfo.objects.all(), "number has been used"
                    )
                ],
            },
        }

    def create(self, validated_data):
        email = validated_data.get("email")
        lastName = validated_data.get("lastName")

        newParent = ParentInfo.objects.create(**validated_data)

        customUser = CustomUser.objects.create(
            username=email,
            isParent=True,
        )
        customUser.set_password(raw_password=lastName)
        customUser.save()
        newParent.save()
        return newParent


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo

        fields = "__all__"

        extra_kwargs = {
            "firstName": valid,
            "lastName": valid,
            "email": valid,
            "phoneNumber": valid,
        }

    def create(self, validated_data):
        newStudent = StudentInfo.objects.create(**validated_data)

        email, lastName, firstName, isAdult = [
            validated_data.get("email"),
            validated_data.get("lastName"),
            validated_data.get("firstName"),
            validated_data.get("isAdult"),
        ]

        if not isAdult:
            customUser = CustomUser.objects.create(username=email, isStudent=True)
            customUser.set_password(raw_password=lastName)
            customUser.save()

        newStudent.save()

        return newStudent


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeInfo

        fields = "__all__"

        extra_kwargs = {
            "firstName": valid,
            "lastName": valid,
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        EmployeeInfo.objects.all(),
                        "Email has been used by another tutor",
                    ),
                ],
            },
            "phoneNumber": valid,
            "availabilities": valid,
            "specialization": valid,
            "address": valid,
            "postalCode": valid,
            "dateOfBirth": valid,
            "gender": {
                "allow_blank": True,
                "required": False,
            },
            "socialSecurityNumber": valid,
            "accountNumber": valid,
            "routingNumber": valid,
        }

        def create(self, validated_data):
            newEmployee = EmployeeInfo.objects.create(**validated_data)

            newEmployee.save()
            return newEmployee


def DyanamicFullNameSerializer(model_class):
    class FullNameSerializer(serializers.ModelSerializer):
        full_name = serializers.SerializerMethodField()

        def get_full_name(self, obj):
            return f"{obj.firstName} {obj.lastName}"

        class Meta:
            model = model_class

            fields = ("id", "full_name", "profile_picture", "email")

    return FullNameSerializer


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassModel

        fields = "__all__"
        extra_kwargs = {
            "title": {
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        ClassModel.objects.all(), "Another class has this name already"
                    )
                ],
            },
            "section": {"required": True},
            "branch": {"required": True},
        }

    def create(self, validated_data):
        newClass = ClassModel.objects.create(**validated_data)
        newClass.save()

        return newClass


class ClassSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassModel

        fields = (
            "id",
            "title",
        )


class ClassScheduleSerializer(serializers.ModelSerializer):
    class_type = serializers.ChoiceField(choices=ClassSchedule.ClassType.choices)

    class Meta:
        model = ClassSchedule
        fields = "__all__"

    def create(self, validated_data):
        students_data = validated_data.pop(
            "students", []
        )  # the [] at the end here is so that in case students is empty it'll return a an empty string []
        newSchedule = ClassSchedule.objects.create(**validated_data)
        newSchedule.students.set(students_data)
        newSchedule.save()

        return newSchedule


class Calendarserializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = (
            "id",
            "class_title",
            "availablilityData",
            "startingDate",
            "endingDate",
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions

        fields = "__all__"
        extra_kwargs = {
            "transaction_type": valid,
            "amout": valid,
            "description": {"required": False},
        }

    def create(self, validated_data):
        new_transactions = Transactions.objects.create(
            amount=validated_data.get("amount"),
            type=validated_data.get("type"),
            description=validated_data.get("description"),
            transaction_type=validated_data.get("transaction_type"),
            family=validated_data.get("family"),
        )

        return new_transactions


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice

        fields = "__all__"

    def create(self, validated_data):
        class_schedule = validated_data.pop("class_schedule", [])
        new_invoice = Invoice.objects.create(**validated_data)
        new_invoice.class_schedule.set(class_schedule)

        return new_invoice


class InvoiceListSerializer(serializers.ModelSerializer):
    bearer_name = serializers.SerializerMethodField()

    def get_bearer_name(self, obj):
        if obj.student and obj.student.parent:
            parent = obj.student.parent
            fullname = f"{parent.firstName} {parent.lastName}"
            return fullname

        else:
            return None

    class Meta:
        model = Invoice

        fields = (
            "id",
            "issue_Date",
            "due_date",
            "class_schedules",
            "description",
            "branch",
            "bearer_name",
            "fee",
        )
