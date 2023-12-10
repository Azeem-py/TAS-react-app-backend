from rest_framework.response import Response
from rest_framework import views, viewsets, generics, status, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action, permission_classes
from django.shortcuts import get_object_or_404
from master_admin.models import BranchInfo
from .serializers import *
from auth_api.custom_permissions import *
from knox.auth import TokenAuthentication
from auth_api.models import CustomUser
from django.db.models import Q, Count, Subquery, Prefetch
from .processScheduleData import *
import logging

from .dueDateCalc import dueDateCalc

# Create your views here.

logger = logging.getLogger(__name__)


class ParentView(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, isBranchAdmin)

    def create(self, request):
        data = request.data
        serializer = ParentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = ParentInfo.objects.all()
        serializer = ParentSerializer(queryset, many=True)
        return Response(serializer.data)

    def getParentInfo(self, request, pk=None):
        queryset = ParentInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ParentSerializer(user)
        return Response(serializer.data)

    def validate_family_email(self, request, email=None):
        queryset = ParentInfo.objects.all()
        parent = get_object_or_404(queryset, email=email)
        serializer = ParentSerializer(parent)
        return Response(serializer.data)


class StudentView(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (permissions.IsAuthenticated, isBranchAdmin)

    def create(self, request):
        email = request.data["email"]
        email_exists = CustomUser.objects.filter(username=email).exists()

        if email_exists:
            return Response({"email": email_exists}, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = StudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = StudentInfo.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    @permission_classes(
        [
            isBranchAdmin,
        ]
    )
    @action(
        detail=True,
        methods=[
            "get",
        ],
    )
    def getStudentInfo(self, request, pk=None):
        queryset = StudentInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(user)
        parentID = serializer.data["parent"]
        parent = ParentInfo.objects.filter(id=parentID).values(
            "firstName", "lastName", "phoneNumber"
        )[0]

        parentName = f"{parent['firstName']} {parent['lastName']}"
        parentPhoneNumber = parent["phoneNumber"]

        data = serializer.data
        data["parentName"] = parentName
        data["parentPhoneNumber"] = parentPhoneNumber
        return Response(data, status=status.HTTP_200_OK)

    def addIndependentStudent(self, request):
        data = request.data.copy()
        [data.pop("school"), data.pop("grade")]

        data["isAdult"] = True

        serializer = ParentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # for students
        data = request.data.copy()
        data["parent"] = serializer.data["id"]
        data["isAdult"] = True

        serializer = StudentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def getParentChild(self, request, parentID=None):
        data = ""
        renderer = JSONRenderer()
        user = request.user

        if not parentID:
            if user.isParent:
                try:
                    parent = ParentInfo.objects.get(email=user)
                    parentID = parent.id
                except ParentInfo.DoesNotExist:
                    return Response(
                        {"error": "Parent not found for this user."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

        children = StudentInfo.objects.filter(parent=parentID).values(
            "id",
            "firstName",
            "lastName",
            "email",
            "grade",
            "profile_picture",
            "phoneNumber",
        )
        data = renderer.render(children)
        print(data)

        return Response(data, status=status.HTTP_200_OK)

    def getNames(self, request, branch=None):
        queryset = EmployeeInfo.objects.all()
        serializer_class = DyanamicFullNameSerializer(StudentInfo)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)


class StudentSearchAPIView(generics.ListAPIView):
    serializer_class = DyanamicFullNameSerializer(StudentInfo)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, notStudent]

    def get_queryset(self):
        query = self.request.query_params.get("query")
        branch_id = self.request.query_params.get("branch_id")
        if query:
            queryset = StudentInfo.objects.filter(
                Q(firstName__icontains=query) | Q(lastName__icontains=query)
            )
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        else:
            queryset = StudentInfo.objects.all()
        return queryset


class TutorSearchAPIView(generics.ListAPIView):
    serializer_class = DyanamicFullNameSerializer(EmployeeInfo)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, notStudent)

    def get_queryset(self):
        query = self.request.query_params.get("query")
        branch_id = self.request.query_params.get("branch_id")
        if query:
            queryset = EmployeeInfo.objects.filter(
                Q(firstName__icontains=query) | Q(lastName__icontains=query)
            )
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        else:
            queryset = EmployeeInfo.objects.all()
        return queryset


class ParentSearchAPIView(generics.ListAPIView):
    serializer_class = DyanamicFullNameSerializer(ParentInfo)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, notStudent)

    def get_queryset(self):
        query = self.request.query_params.get("query")
        branch_id = self.request.query_params.get("branch_id")
        if query:
            queryset = ParentInfo.objects.filter(
                Q(firstName__icontains=query) | Q(lastName__icontains=query)
            )
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        else:
            queryset = ParentInfo.objects.all()
        return queryset


class ClassSearchAPIView(generics.ListAPIView):
    serializer_class = ClassSearchSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, isBranchAdmin)

    def get_queryset(self):
        query = self.request.query_params.get("query")
        branch_id = self.request.query_params.get("branch_id")
        if query:
            queryset = ClassModel.objects.filter(Q(title__icontains=query))
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        else:
            queryset = ClassModel.objects.all()
        return queryset


class EmployeeView(viewsets.ViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsBranchAdmin)
    def create(self, request):
        data = request.data

        serializer = EmployeeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email, lastName = [data.get("email"), data.get("lastName")]
        new_user = CustomUser.objects.create(username=email, isTutor=True)
        new_user.set_password(raw_password=lastName)
        new_user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = EmployeeInfo.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

    def getEmployeeInfo(self, request, pk=None):
        queryset = EmployeeInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(user)
        return Response(serializer.data)

    def getNames(self, request, branch=None):
        queryset = EmployeeInfo.objects.all()
        serializer_class = DyanamicFullNameSerializer(EmployeeInfo)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)


class BranchListView(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, isBranchAdmin)

    def get_branch_list(self, request, branch=None, info=None):
        data = ""
        renderer = JSONRenderer()

        if info == "students":
            queryset = StudentInfo.objects.filter(branch=branch).values(
                "id", "firstName", "lastName", "email", "phoneNumber", "profile_picture"
            )
            data = renderer.render(queryset)

        elif info == "families":
            queryset = ParentInfo.objects.filter(branch=branch, isAdult=False).values(
                "id", "firstName", "lastName", "email", "phoneNumber", "profile_picture"
            )
            data = renderer.render(queryset)

        elif info == "employees":
            queryset = EmployeeInfo.objects.filter(branch=branch).values(
                "id",
                "firstName",
                "lastName",
                "email",
                "phoneNumber",
                "hireDate",
                "profile_picture",
            )
            data = renderer.render(queryset)

        return Response(data, status=status.HTTP_200_OK)


class TutorInBranch(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsBranchAdmin)

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the tutors in the branch
        as determined by the id portion of the URL.
        """
        branch_id = self.kwargs["id"]
        return EmployeeInfo.objects.filter(branch=branch_id)


class ParentInBranch(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsBranchAdmin)

    serializer_class = ParentSerializer

    def get_queryset(self):
        """
        This view should return a list of all the parent in the branch
        as determined by the id portion of the URL.
        """
        branch_id = self.kwargs["id"]
        return ParentInfo.objects.filter(branch=branch_id)


class StudentsUnderParent(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsBranchAdmin, IsParent)
    serializer_class = StudentSerializer

    def get_queryset(self):
        """
        This view should return a list of all the students under the parent
        as determined by the id portion of the URL.
        """
        parent_id = self.kwargs["id"]
        return StudentInfo.objects.filter(parent=parent_id)


class ClassView(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, isBranchAdmin)

    def create(self, request):
        serializer = ClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = ClassModel.objects.all()
        serializer = ClassSerializer(queryset, many=True)
        return Response(serializer.data)


class ClassScheduleView(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def create(self, request):
        new_data = request.data["availablilityData"]
        new_data = NewAvailaibilityData(new_data)
        students = request.data["students"]
        tutor = request.data["tutor"]
        tutor_availability = list(
            EmployeeInfo.objects.filter(id=tutor).values("availablilityData")
        )
        if tutor_availability:
            old_data = BigAvailabiltyData(tutor_availability)
            conflict = checkConflict(old_data, new_data, against=True)
            if conflict:
                key = list(conflict.keys())[0]
                if key:
                    fro, to = conflict[key][0], conflict[key][1]
                    return Response(
                        {
                            "conflict": f"The selected tutor is not available on {key} from {fro} to {to}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        tutor_query = ClassSchedule.objects.filter(tutor=tutor).values(
            "availablilityData"
        )
        tutor_query = list(tutor_query)

        if tutor_query:
            old_data = BigAvailabiltyData(tutor_query)
            print("old_data in tutor schedule", old_data)
            conflict = checkConflict(old_data, new_data, against=False)
            if conflict:
                key = list(conflict.keys())[0]
                print("key", key)
                if key:
                    fro, to = conflict[key][0], conflict[key][1]
                    return Response(
                        {
                            "conflict": f"The selected tutor will be having a class on {key} from {fro} to {to}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        for student in students:
            student_query = list(
                ClassSchedule.objects.filter(students=student).values(
                    "availablilityData"
                )
            )
            if student_query:
                old_data = BigAvailabiltyData(student_query)
                print("old_data in student", old_data)
                conflict = checkConflict(old_data, new_data, against=False)
                if conflict:
                    serializerClass = DyanamicFullNameSerializer(StudentInfo)
                    queryset = StudentInfo.objects.get(pk=student)
                    serializer = serializerClass(queryset)
                    name = serializer.data["full_name"]
                    key = list(conflict.keys())[0]
                    print("key", key)
                    if key:
                        fro, to = conflict[key][0], conflict[key][1]
                        return Response(
                            {
                                "conflict": f"{name} is not available on {key} from {fro} to {to}"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

        serializer = ClassScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data["students"])
        # creating an invoice for every student in the class
        students = serializer.data["students"]
        title = serializer.data["class_title"]
        schedule_id = serializer.data["id"]
        branch = BranchInfo.objects.get(id=request.data["branch"])
        instances = []  # this instance is to be used for creating a a bulk invoice
        for student in students:
            student_data = StudentInfo.objects.get(id=student)
            invoice_description = f"{title} for {student_data.firstName}"
            due_date = dueDateCalc()
            invoice = Invoice(
                student=student_data,
                description=invoice_description,
                due_date=due_date,
                branch=branch,
                fee=request.data["fee"],
            )
            invoice.save()
            invoice.class_schedules.add(schedule_id)
            instances.append(invoice)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def calendar(self, request, branch, month):
        tutor = self.request.query_params.get("tutor")
        student = self.request.query_params.get("student")

        # Start with an empty Q object
        filter_condition = Q()

        # Add conditions for branch and tutor if tutor is not None
        if tutor is not None:
            filter_condition &= Q(tutor=tutor)

        # Add conditions for students if student is not None
        if student is not None:
            filter_condition &= Q(students__id=student)

        user = request.user
        class_schedules = ClassSchedule.objects.filter(
            Q(
                startingDate__month__lte=month,
                endingDate__month__gte=month,
            )
            | Q(
                startingDate__month__lte=month,
                endingDate__month__gte=month,
            )
        )

        if user.isBranchAdmin:
            class_schedules = class_schedules.filter(branch=branch).filter(
                filter_condition
            )
        elif user.isParent:
            parent = ParentInfo.objects.get(email=user).id
            class_schedules = class_schedules.filter(
                students__parent__id=parent
            ).filter(filter_condition)

        elif user.isTutor:
            tutor = EmployeeInfo.objects.get(email=user).id
            class_schedules = class_schedules.filter(tutor=tutor).filter(
                filter_condition
            )
        elif user.isStudent:
            student = StudentInfo.objects.get(email=user).id
            class_schedules = class_schedules.filter(students__id=student)
        serializer = Calendarserializer(class_schedules, many=True)
        print(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    # this is used in the student proile to check the list of class which also included the name of the tutor and the date range for that class
    def student_schedule(self, request, student_id=None):
        try:
            student_id = int(student_id)
        except ValueError:
            return Response(
                {"detail": "Invalid student ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        student_schedules = ClassSchedule.objects.filter(students__id=student_id)
        tutor_data = list(
            student_schedules.values_list("tutor__firstName", "tutor__lastName")
        )

        serializer = ClassScheduleSerializer(student_schedules, many=True)

        name_index = 0  # this variable is for identifying the index of the tutor name
        for data in serializer.data:
            name = tutor_data[name_index]
            data["tutorName"] = f"{name[0]} {name[1]}"
            name_index += 1
        return Response(serializer.data, status=status.HTTP_200_OK)

    # this method is for displaying the data/info of a scheduled class in the modal on the calendar
    @action(detail=False, methods=["GET"])
    def classScheduleInfo(self, request, schedule_id=None):
        schedule = ClassSchedule.objects.get(id=schedule_id)
        ref_class = ClassModel.objects.get(id=schedule.referenceClass.id)
        schedule_data = ClassScheduleSerializer(schedule).data

        tutor_info = EmployeeInfo.objects.get(id=schedule.tutor.id)
        fullName = f"{tutor_info.firstName} {tutor_info.lastName}"
        schedule_data["tutor"] = fullName

        ref_class_data = ClassSerializer(ref_class).data

        whole_info = {"schedule": schedule_data, "ref_class": ref_class_data}
        return Response(whole_info)

    @action(detail=False, methods=["GET"])
    def tutorSchedule(self, request):
        user = request.user
        tutor = EmployeeInfo.objects.get(email=user).id
        print(tutor)
        scheduleQuery = ClassSchedule.objects.filter(tutor=tutor)
        print(scheduleQuery)

        serializer = ClassScheduleSerializer(scheduleQuery, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def studentSchedule(self, request):
        user = request.user
        student = StudentInfo.objects.get(email=user).id
        scheduleQuery = ClassSchedule.objects.filter(students__id=student)
        print(scheduleQuery)

        serializer = ClassScheduleSerializer(scheduleQuery, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def parentSchedule(self, request):
        user = request.user
        parent = ParentInfo.objects.get(email=user).id
        scheduleQuery = ClassSchedule.objects.filter(students__parent__id=parent)
        print(scheduleQuery)

        serializer = ClassScheduleSerializer(scheduleQuery, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


# this viewset can add student to class and can also retrieve list of all student and the class they are in classes
class StudentClassViewset(viewsets.ViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsBranchAdmin)
    def create(self, request):
        serializer = ClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = ClassModel.objects.all()
        serializer = ClassSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvoiceViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = InvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_invoice(self, request, branch):
        queryset = Invoice.objects.filter(branch=branch)
        serializer = InvoiceListSerializer(queryset, many=True)
        return Response(serializer.data)

    def family_invoice(self, request, parentID=None, filter=None):
        class_schedules = ""
        if filter == 1:
            class_schedules = (
                ClassSchedule.objects.filter(
                    invoice__class_schedule__students__parent__id=parentID
                )
                .distinct()
                .prefetch_related(
                    Prefetch(
                        "students",
                        queryset=StudentInfo.objects.filter(parent__id=parentID),
                    )
                )
            )
        serializer = ClassScheduleSerializer(class_schedules, many=True)
        print(serializer.data)
        return Response(serializer.data)

        # invoices = Invoice.objects.filter(
        #     class_schedule__students__parent=parentID
        # ).distinct()

        # serializer = InvoiceSerializer(invoices, many=True)
        # return Response(serializer.data)
