from . import models
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes(())
def signup(request):
    try:
        data = request.data
        data_username = data['username']
        data_password = data['password']
        data_email = data['email']
        newUser = models.MyUser.objects.create(username=data_username, email=data_email)
        newUser.set_password(data_password)
        newUser.save()
        return Response({"message": "Created Successfully!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes(())
def login(request):
    try:
        params = request.data
        user = authenticate(username=params['username'], password=params['password'], )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            tmp_response = {
                'access': token.key,
                'userid': token.user.id
            }
            return Response(tmp_response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Wrong username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes(())
def show_reports(request):
    try:
        patients = models.Patient.objects.filter()
        rsp = {}
        counter = 0
        for i in patients:
            rsp.update({'patient' + str(counter): {'pid': i.id,
                                                   'first_name': i.first_name,
                                                   'last_name': i.last_name,
                                                   'phone_number': i.phone_number,
                                                   'national_code': i.national_code,
                                                   'disease': i.disease}})
            counter = counter + 1
        return Response(rsp, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes(())
def add_patient(request):
    try:
        data = request.data
        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
        national_code = data['national_code']
        disease = data['disease']
        new_patient = models.Patient.objects.create(first_name=first_name, last_name=last_name,
                                                    phone_number=phone_number, national_code=national_code,
                                                    disease=disease)
        return Response({'flag': True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'flag': False}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes(())
def delete_patient(request, pk):
    try:
        patient = models.Patient.objects.get(national_code=pk)
        patient.delete()
        return Response({'flag': True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'flag': False}, status=status.HTTP_401_UNAUTHORIZED)