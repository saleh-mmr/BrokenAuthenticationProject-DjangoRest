from . import models
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
# from .Authentication import token_expire_handler
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as django_logout


@api_view(['POST'])
@permission_classes(())
def signup(request):
    try:
        data = request.data
        data_username = data['user']
        data_password = data['pass']
        data_confirm_password = data['cpassword']
        if data_confirm_password == data_password:
            newUser = models.MyUser.objects.create(username=data_username)
            newUser.set_password(data_password)
            newUser.save()
            if newUser:
                return Response({"message": "Created Successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something might be Wrong!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes(())
def login(request):
    try:
        params = request.data
        user = authenticate(request=request, username=params['username'], password=params['password'], )
        if user is not None:
            django_login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            # is_expired, token = token_expire_handler(token)
            tmp_response = {
                'access': token.key,
            }
            return Response(tmp_response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Wrong username or password"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes(())
def logout(request):
    try:
        django_logout(request)
        Token.objects.filter(key=request.headers.get('Authorization')[6:]).delete()
        return Response({"message": "Logout Successfully!"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "An error occurs in logout!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes(())
def user_info(request):
    try:
        user = request.user
        rsp = {'username': user.username}
        return Response(rsp, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


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
@permission_classes([IsAuthenticated])
def delete_patient(request, pk):
    try:
        patient = models.Patient.objects.get(national_code=pk)
        patient.delete()
        return Response({'flag': True, 'message': 'patient deleted'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'flag': False}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def is_admin(request):
    try:
        return Response({'flag': True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'flag': False}, status=status.HTTP_401_UNAUTHORIZED)
