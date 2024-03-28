from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView

from medicify_project.models import * 
from medicify_project.serializers import *
from django.db.models import Q

from django.db import connection
from django.utils import timezone

# from .models import Tbldoctorlocations
# from .serializers import DoctorLocationSerializer
# from .models import Tbldoctors  # Import the correct model
# from .serializers import DoctorSerializer
# from .models import Tbldoctorlocationavailability
# from .serializers import DoctorLocationAvailabilitySerializer


######################### Doctor Medicines ############################
##################### insert  ##########
@api_view(['POST'])
def fi_insert_doctor_medicines(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            data = request.data
            data['isdeleted'] = 0  # Assuming isdeleted is a field in your model

            # Validations for required fields
            required_fields = ['medicine_code', 'medicine_name', 'medicine_form']
            missing_fields = [field for field in required_fields if not data.get(field)]

            if missing_fields:
                res = {
                    'message_code': 999,
                    'message_text': f"Missing required fields: {', '.join(missing_fields)}",
                    'message_data': {},
                    'message_debug': debug if debug else []
                }
            else:
                try:
                    # Creating a new instance of TbldoctorMedicines model
                    # doctor_medicine = TbldoctorMedicines(**data)

                    # # Saving the new instance to the database
                    # doctor_medicine.save()
                    doctorMedicinesSerializer = TbldoctorMedicinesSerializer(data=data)
                    if doctorMedicinesSerializer.is_valid():
                        instance = doctorMedicinesSerializer.save()
                        last_doctor_medicine_id = instance.doctor_medicine_id

                        res = {
                            'message_code': 1000,
                            'message_text': 'Success',
                            'message_data': last_doctor_medicine_id,
                            'message_debug': debug if debug else []
                        }
                    else:
                        res = {
                            'message_code': 2000,
                            'message_text': 'Validation Error',
                            'message_errors': doctorMedicinesSerializer.errors
                        } 
                except Exception as e:
                    res = {
                        'message_code': 999,
                        'message_text': f"Failed to insert doctor medicine. Error: {str(e)}",
                        'message_data': {},
                        'message_debug': debug if debug else []
                    }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_insert_doctor_medicines. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_200_OK)

##################### update  ##########
@api_view(['POST'])
def fi_update_doctor_medicines(request, doctor_medicine_id):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            data = request.data
            doctor_medicine_id = int(doctor_medicine_id)

            if not doctor_medicine_id:
                return Response({'message_code': 999, 'message_text': 'Doctor medicine id is required.'}, status=status.HTTP_200_OK)

            try:
                doctor_medicine = TbldoctorMedicines.objects.get(doctor_medicine_id=doctor_medicine_id)
            except TbldoctorMedicines.DoesNotExist:
                return Response({
                    'message_code': 999,
                    'message_text': f'Doctor medicine with id {doctor_medicine_id} does not exist.',
                    'message_debug': debug if debug else {}
                }, status=status.HTTP_200_OK)

            fields_to_update = ['medicine_code', 'medicine_name', 'medicine_form', 'medicine_frequency',
                                 'medicine_duration', 'medicine_dosages', 'medicine_manufacture', 'medicine_pack_size',
                                 'medicine_preservation', 'medicine_min_stock', 'medicine_gst', 'medicine_content_name','price']

            for field in fields_to_update:
                if data.get(field) is not None:
                    setattr(doctor_medicine, field, data.get(field, ''))

            doctor_medicine.save()

            serializer = TbldoctorMedicinesSerializer(doctor_medicine)

            res = {
                'message_code': 1000,
                'message_text': 'Success',
                'message_data': serializer.data,
                'message_debug': debug if debug else []
            }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_update_doctor_medicines. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_200_OK)
##################### Delete  ##########
@api_view(['DELETE'])
def fi_delete_doctor_medicines(request, doctor_medicine_id):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'DELETE':
            if not doctor_medicine_id:
                return Response({'message_code': 999, 'message_text': 'Doctor medicine id is required.'}, status=status.HTTP_200_OK)

            try:
                # Fetching the existing TbldoctorMedicines instance from the database
                doctor_medicine = TbldoctorMedicines.objects.get(doctor_medicine_id=doctor_medicine_id)
            except TbldoctorMedicines.DoesNotExist:
                return Response({
                    'message_code': 999,
                    'message_text': f'Doctor medicine with id {doctor_medicine_id} does not exist.',
                    'message_debug': debug if debug else {}
                }, status=status.HTTP_200_OK)

            # Soft delete logic
            doctor_medicine.isdeleted = 1
            doctor_medicine.deletedby = request.user.id  # Assuming you have a user object in your request
            doctor_medicine.deletedreason = "Soft delete reason"  # Provide a reason for the deletion if necessary
            doctor_medicine.save()

            res = {
                'message_code': 1000,
                'message_text': 'Success',
                'message_data': {'doctor_medicine_id': doctor_medicine.doctor_medicine_id},
                'message_debug': debug if debug else []
            }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_delete_doctor_medicines. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_200_OK)
##################### Get  ##########
@api_view(['POST'])
def fi_get_all_doctor_medicines(request):
    debug = ""
    res = {'message_code': 999, 'message_text': "Failure", 'message_data': {'Functional part is commented.'}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            data = request.data

            doctor_medicine_id = data.get('doctor_medicine_id', '')
            if not doctor_medicine_id:
                return Response({'message_code': 999, 'message_text': 'Doctor medicine id is required.'}, status=status.HTTP_200_OK)

            try:
                # Fetching the existing TbldoctorMedicines instance from the database
                doctor_medicine = TbldoctorMedicines.objects.filter(doctor_medicine_id=doctor_medicine_id)
                serializer = TbldoctorMedicinesSerializer(doctor_medicine, many=True)

                return Response({
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': serializer.data,
                    'message_debug': debug if debug else []
                }, status=status.HTTP_200_OK)
            except TbldoctorMedicines.DoesNotExist:
                return Response({
                    'message_code': 999,
                    'message_text': f'Doctor medicine with id {doctor_medicine_id} not found.',
                    'message_data': { },
                    'message_debug': debug if debug else []
                }, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_get_all_doctor_medicines. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_200_OK)


#########################get all doctor medicine bydoctorid and medicinename##########################
@api_view(['POST'])
def fi_get_all_doctor_medicine_bydoctorid_medicinename(request):
    debug = ""
    res = {'message_code': 999, 'message_text': "Failure", 'message_data': {'Functional part is commented.'}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            data = request.data

            doctor_id = data.get('doctor_id', '')
            medicine_name = data.get('medicine_name', '')
            if not doctor_id:
                return Response({'message_code': 999, 'message_text': 'Doctor id is required.'}, status=status.HTTP_200_OK)
            try:
                
                doctor_medicines_queryset = TbldoctorMedicines.objects.filter(doctor_id=doctor_id,isdeleted=0)

                if medicine_name:
                    doctor_medicines_queryset = doctor_medicines_queryset.filter(medicine_name__icontains=medicine_name)

                serializer = TbldoctorMedicinesSerializer(doctor_medicines_queryset, many=True)


                return Response({
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': serializer.data,
                    'message_debug': debug if debug else []
                }, status=status.HTTP_200_OK)
            except TbldoctorMedicines.DoesNotExist:
                return Response({
                    'message_code': 999,
                    'message_text': f'Doctor medicine with id  not found.',
                    'message_data': { },
                    'message_debug': debug if debug else []
                }, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_get_all_doctor_medicines. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_200_OK)


######################### Doctor Medicines ############################
##################### insert  ##########
@api_view(['POST'])
def fi_insert_doctor_location(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': [], 'message_debug': debug}

    try:
        serializer = DoctorLocationSerializer(data=request.data)
        print("Request Data:", request.data)

        if serializer.is_valid():
            doctor_location = serializer.save()
            serialized_data = DoctorLocationSerializer(doctor_location).data
            res = {
                'message_code': 1000,
                'message_text': 'Success',
                'message_data': serialized_data,
                'message_debug': [{"Debug": debug}] if debug != "" else []
            }
        else:
            debug = f"Serializer errors: {serializer.errors}"
            res = {
                'message_code': 999,
                'message_text': 'Invalid data provided.',
                'message_data': {},
                'message_debug': [{"Debug": debug}] if debug != "" else []
            }
    except Exception as e:
        debug = f"Error: {str(e)}"
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_insert_doctor_location. {debug}',
            'message_data': [],
            'message_debug': [{"Debug": debug}] if debug != "" else []
        }

    return Response(res, status=status.HTTP_200_OK)

##################### update  ##########
@api_view(['POST'])
def fi_update_doctor_location(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        doctor_location_id = request.data.get('doctor_location_id')
        if doctor_location_id:
            try:
                doctor_location = Tbldoctorlocations.objects.get(doctor_location_id=doctor_location_id)
            except Tbldoctorlocations.DoesNotExist:
                res = {
                    'message_code': 999,
                    'message_text': 'Doctor location not found.',
                    'message_data': {},
                    'message_debug': debug if debug else {}
                }
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            serializer = DoctorLocationSerializer(doctor_location, data=request.data, partial=True)
            if serializer.is_valid():
                updated_data = serializer.validated_data  # Get the validated data after a successful update
                serializer.save()
                res = {
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': doctor_location_id,
                    'message_debug': debug if debug else []
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                res = {
                    'message_code': 999,
                    'message_text': serializer.errors,
                    'message_data': {},
                    'message_debug': debug if debug else []
                }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_update_doctor_location. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_400_BAD_REQUEST)

##################### Delete  ##########
@api_view(['DELETE'])
def fi_delete_doctor_location(request, doctor_location_id):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        doctor_location = Tbldoctorlocations.objects.get(doctor_location_id=doctor_location_id)
        doctor_location.isdeleted = True
        doctor_location.save()
        # doctor_location.delete()

        res = {
            'message_code': 1000,
            'message_text': 'Success',
            'message_data': {'Doctor location deleted successfully.'},
            'message_debug': [{"Debug": debug}] if debug else []
        }
    except Tbldoctorlocations.DoesNotExist:
        res = {
            'message_code': 900,
            'message_text': 'Doctor location not found.',
            'message_data': {},
            'message_debug': [{"Debug": debug}] if debug else []
        }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_delete_doctor_location. Error: {str(e)}',
            'message_data': {},
            'message_debug': [{"Debug": debug}] if debug else []
        }

    return Response(res, status=status.HTTP_404_NOT_FOUND if res['message_code'] == 900 else status.HTTP_200_OK)
##################### Get  ##########


@api_view(['POST'])
def fi_get_all_doctor_location(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': [], 'message_debug': debug}
    

    doctor_location_id = request.data.get('doctor_location_id', '')
    
    if not doctor_location_id:
        res = {'message_code': 999, 'message_text': 'doctor location id is required.'}
    else:
        try:
            
            doctor_location = Tbldoctorlocations.objects.filter(
                Q(doctor_location_id=doctor_location_id,isdeleted=0)
            )

            # Serialize the data
            serializer = DoctorLocationSerializer(doctor_location, many=True)
            result = serializer.data
            # last_query = connection.queries[-1]['sql']
            # print(last_query)
            if result:
                res = {
                    'message_code': 1000,
                    'message_text': "Doctor location retrieved successfully.",
                    'message_data': result,
                    'message_debug': [{"Debug": debug}] if debug != "" else []
                }
            else:
                res = {
                    'message_code': 999,
                    'message_text': "Doctor location not found.",
                    'message_data': [],
                    'message_debug': [{"Debug": debug}] if debug != "" else []
                }

        except Exception as e:
            res = {'message_code': 999, 'message_text': f"Error: {str(e)}"}

    return Response(res, status=status.HTTP_200_OK)


############################# Doctor ##################################
######################## Insert ############################
@api_view(['POST'])
def fi_insert_doctor(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        data = request.data.copy()  # Create a copy of the data to avoid modifying the original request data
        
        # Convert the date of birth to epoch time
        date_of_birth_str = data.get('doctor_dateofbirth', '')
        if date_of_birth_str:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
            epoch_time = int(date_of_birth.timestamp())
            data['doctor_dateofbirth'] = epoch_time

        serializer = DoctorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            res = {
                'message_code': 1000,
                'message_text': 'Success',
                'message_data': serializer.data,
                'message_debug': debug if debug else []
            }
        else:
            errors = {field: serializer.errors[field][0] for field in serializer.errors}
            res = {
                'message_code': 999,
                'message_text': errors,
                'message_data': {},
                'message_debug': debug if debug else []
            }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_insert_doctor. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_200_OK if res['message_code'] == 1000 else status.HTTP_400_BAD_REQUEST)

######################## Delete ############################
@api_view(['DELETE'])
def fi_delete_doctor(request, doctor_id):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        doctor = Tbldoctors.objects.get(pk=doctor_id)  # Use the correct model
        doctor.isdeleted = True  # Update the field name
        doctor.save()

        if doctor.isdeleted:
            response_data = {
                'message': f'Doctor ID {doctor_id} deleted successfully.',
            }
            res = {
                'message_code': 1000,
                'message_text': 'Success',
                'message_data': response_data,
                'message_debug': debug if debug else []
            }
        else:
            res = {
                'message_code': 999,
                'message_text': 'Doctor Id not found.',
                'message_data': {},
                'message_debug': debug if debug else []
            }
    except Tbldoctors.DoesNotExist:  # Use the correct model
        res = {
            'message_code': 999,
            'message_text': 'Doctor Id not found.',
            'message_data': {},
            'message_debug': debug if debug else []
        }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in fi_delete_doctor. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_404_NOT_FOUND if res['message_code'] == 999 else status.HTTP_200_OK)


################################## Doctor location Availability ##########################################
######################## Insert ############################
@api_view(['POST'])
def insert_doctor_location_availability(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            
            data = request.data
            data['isdeleted',]=0
            serializer = DoctorLocationAvailabilitySerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                res = {
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': serializer.data,
                    'message_debug': debug if debug else []
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                errors = {field: serializer.errors[field][0] for field in serializer.errors}
                error_message = 'Invalid data provided. Please check the following fields:'
                for field, message in errors.items():
                    error_message += f'\n- {field}: {message}'

                res = {
                    'message_code': 999,
                    'message_text': error_message,
                    'message_data': {},
                    'message_debug': debug if debug else []
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in insert_doctor_location_availability. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_400_BAD_REQUEST)

######################## Update ############################
@api_view(['POST'])
def update_doctor_location_availability(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            data = request.data
            doctor_location_availability_id = data.get('Doctor_Location_Availability_Id', None)

            if doctor_location_availability_id is not None:
                try:
                    instance = Tbldoctorlocationavailability.objects.get(doctor_location_availability_id=doctor_location_availability_id, isdeleted=False)
                    serializer = DoctorLocationAvailabilitySerializer(instance, data=data, partial=True)

                    if serializer.is_valid():
                        updated_instance = serializer.save()
                        updated_data = {}

                        for field in serializer.fields:
                            if field in serializer.validated_data:
                                updated_data[field] = updated_instance.__getattribute__(field)

                        res = {
                            'message_code': 1000,
                            'message_text': 'Success',
                            'message_data': updated_data,
                            'message_debug': debug if debug else []
                        }
                        return Response(res, status=status.HTTP_200_OK)
                    else:
                        res['message_text'] = 'Invalid data provided.'
                        return Response(res, status=status.HTTP_400_BAD_REQUEST)
                except Tbldoctorlocationavailability.DoesNotExist:
                    res['message_text'] = 'Doctor location availability not found.'
                    return Response(res, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in update_doctor_location_availability. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_400_BAD_REQUEST)


######################## Delete ############################
@api_view(['DELETE'])
def delete_doctor_location_availability(request, doctor_location_availability_id):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'DELETE':
            try:
                instance = Tbldoctorlocationavailability.objects.get(doctor_location_availability_id=doctor_location_availability_id, isdeleted=False)
                instance.isdeleted = True
                instance.save()
                res = {
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': [{'Doctor_Location_Availability_Id': doctor_location_availability_id}],
                    'message_debug': debug if debug else []
                }
                return Response(res, status=status.HTTP_200_OK)
            except Tbldoctorlocationavailability.DoesNotExist:
                res['message_text'] = 'Doctor location availability not found.'
                return Response(res, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in delete_doctor_location_availability. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_404_NOT_FOUND if res['message_code'] == 999 else status.HTTP_200_OK)


######################## Get ############################
@api_view(['POST'])
def get_all_doctor_location_availability(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            data = request.data
            doctor_location_availability_id = data.get('Doctor_Location_Availability_Id', None)

            if doctor_location_availability_id is not None:
                try:
                    instance = Tbldoctorlocationavailability.objects.get(doctor_location_availability_id=doctor_location_availability_id, isdeleted=False)
                    serializer = DoctorLocationAvailabilitySerializer(instance)
                    res = {
                        'message_code': 1000,
                        'message_text': 'Success',
                        'message_data': serializer.data,
                        'message_debug': debug if debug else []
                    }
                    return Response(res, status=status.HTTP_200_OK)
                except Tbldoctorlocationavailability.DoesNotExist:
                    res['message_text'] = 'Doctor location availability id not found.'
                    return Response(res, status=status.HTTP_404_NOT_FOUND)
            else:
                queryset = Tbldoctorlocationavailability.objects.filter(isdeleted=False)
                serializer = DoctorLocationAvailabilitySerializer(queryset, many=True)
                res = {
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': serializer.data,
                    'message_debug': debug if debug else []
                }
                return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in get_all_doctor_location_availability. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_doctor_by_id(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_id = request.data.get('doctor_id', None)

    if not doctor_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor ID is required.'}
    else:
        try:
            doctor = Tbldoctors.objects.filter(doctor_id=doctor_id)
            serializer = DoctorSerializer(doctor, many=True)
            result = serializer.data

            response_data = {
                'message_code': 1000,
                'message_text': 'Doctor details are fetched successfully',
                'message_data': result,
                'message_debug': debug
            }

        except Tbldoctors.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Doctor not found.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def update_doctor_details(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_id = request.data.get('doctor_id', None)
    updated_data = request.data.get('updated_data', {})

    if not doctor_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor ID is required.'}
    elif not updated_data:
        response_data = {'message_code': 999, 'message_text': 'Updated data is required.'}
    else:
        try:
            doctor = Tbldoctors.objects.get(doctor_id=doctor_id)
            # Convert the date string to epoch timestamp
            date_of_birth_str = updated_data.get('doctor_dateofbirth', '')
            if date_of_birth_str:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
                epoch_time = int(date_of_birth.timestamp())
                updated_data['doctor_dateofbirth'] = epoch_time

            serializer = DoctorSerializer(doctor, data=updated_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                result = serializer.data
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Doctor details updated successfully',
                    'message_data': result,
                    'message_debug': debug
                }
            else:
                response_data = {'message_code': 999, 'message_text': 'Invalid data provided.', 'message_debug': serializer.errors}

        except Tbldoctors.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Doctor not found.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def insert_ConsultMedic_Fees(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    data = request.data
    doctor_id = data.get('doctor_id')
    location_id = data.get('location_id')

    
    avg_time_per_patient = data.get('avg_time_per_patient')
    price = data.get('price')
    title = data.get('title')

    consultation_fee_data = data.get('consultation_fee', {})
    consultation_fee_data['doctor_id'] = doctor_id
    consultation_fee_data['location_id'] = location_id

    consultation_fee_data['avg_time_per_patient'] = avg_time_per_patient
    consultation_fee_data['price'] = price
    consultation_fee_data['title'] = title

    medical_services_fee_data = data.get('medical_services_fee', {})
    medical_services_fee_data['doctor_id'] = doctor_id
    medical_services_fee_data['location_id'] = location_id

    consultation_fee_serializer = ConsultationFeeSerializer(data=consultation_fee_data)
    medical_services_fee_serializer = MedicalServicesFeeSerializer(data=medical_services_fee_data)

    if consultation_fee_serializer.is_valid() and medical_services_fee_serializer.is_valid():
        consultaion=consultation_fee_serializer.save()
        medicalservice=medical_services_fee_serializer.save()
        response_data['message_code']= 1000
        response_data['message_text'] = 'Data successfully saved!'
        response_data['message_data']={'consultation_fee_id':consultaion.consultation_fee_id,'medical_service_fee_id':medicalservice.medical_service_fee_id}
    else:
        errors = {
            'consultation_fee_errors': consultation_fee_serializer.errors,
            'medical_services_fee_errors': medical_services_fee_serializer.errors
        }
        response_data['message_text'] = 'Failed to save data. Please check the errors.'
        response_data['errors'] = errors

    return Response(response_data, status=status.HTTP_200_OK)




# @api_view(["POST"])
# def get_doctor_profileby_token(request):
#     debug = []
#     response_data = {
#         'message_code': 999,
#         'message_text': 'Functional part is commented.',
#         'message_data': [],
#         'message_debug': debug
#     }

#     doctor_login_token = request.data.get('doctor_login_token', None)

#     if not doctor_login_token:
#         response_data = {'message_code': 999, 'message_text': 'Doctor login token is required.'}
#     else:
#         try:
#             doctor = Tbldoctors.objects.filter(doctor_login_token=doctor_login_token)
#             serializer = DoctorSerializer(doctor, many=True)
#             result = serializer.data
#             if result:
#                 response_data = {
#                     'message_code': 1000,
#                     'message_text': 'Doctor details are fetched successfully',
#                     'message_data': result,
#                     'message_debug': debug
#                 }
#             else:
#                  response_data = {
#                     'message_code': 999,
#                     'message_text': 'no doctor token match.',
#                     'message_data': [],
#                     'message_debug': debug
#                 }

#         except Tbldoctors.DoesNotExist:
#             response_data = {'message_code': 999, 'message_text': 'no doctor token match.', 'message_debug': debug}

#     return Response(response_data, status=status.HTTP_200_OK)


############################################ Lab Investigations


@api_view(['POST'])
def fi_get_labinvestigations_by_id(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': [], 'message_debug': debug}
        

    investigation_id = request.data.get('investigation_id', '')

    if not investigation_id:
        res = {'message_code': 999, 'message_text': 'investigation id is required.'}
    else:
        try:
            
            # Fetch data using Django ORM
            lab_investigation = Tbllabinvestigations.objects.filter(
                Q(investigation_id=investigation_id,isdeleted=0)
            )

            # Serialize the data
            serializer = TbllabinvestigationsSerializer(lab_investigation, many=True)
            result = serializer.data

            if result:
                res = {
                    'message_code': 1000,
                    'message_text': "Lab investigations retrieved successfully.",
                    'message_data': result,
                    'message_debug': [{"Debug": debug}] if debug != "" else []
                }
            else:
                res = {
                    'message_code': 999,
                    'message_text': "Lab investigations for this investigation id not found.",
                    'message_data': [],
                    'message_debug': [{"Debug": debug}] if debug != "" else []
                }

        except Exception as e:
            res = {'message_code': 999, 'message_text': f"Error: {str(e)}"}

    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def fi_insert_labinvestigations(request):
    
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': [], 'message_debug': debug}
     
    # Extract data from request
    doctor_id = request.data.get('doctor_id', '')
    investigation_category = request.data.get('investigation_category', '')
    investigation_name = request.data.get('investigation_name', '')

    # Validate appointment_id
    if not doctor_id:
        res = {'message_code': 999,'message_text': 'Doctor id is required'}
    elif not investigation_category:
        res = {'message_code': 999,'message_text': 'Investigation category is required'}
    elif not investigation_name:
        res = {'message_code': 999,'message_text': 'Investigation name is required'}
    else:
        try:
            
            investigation_data = {
                'doctor_id':doctor_id,
                'investigation_category':investigation_category,
                'investigation_name':investigation_name
            }

            labinvestigationSerializer = TbllabinvestigationsSerializer(data=investigation_data)
            if labinvestigationSerializer.is_valid():
                instance = labinvestigationSerializer.save()
                last_investigation_id = instance.investigation_id

                res = {
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': [{'last_investigation_id': last_investigation_id}],
                    'message_debug': debug if debug else []
                }
            else:
                res = {
                    'message_code': 2000,
                    'message_text': 'Validation Error',
                    'message_errors': labinvestigationSerializer.errors
                }


        except Tbllabinvestigations.DoesNotExist:
            res = {'message_code': 999, 'message_text': 'Tbllabinvestigations not found'}

        except Exception as e:
            res = {'message_code': 999, 'message_text': f'Error: {str(e)}'}

    return Response(res, status=status.HTTP_200_OK)

@api_view(['POST'])
def fi_update_labinvestigations(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': [], 'message_debug': debug}
     
    investigation_id = request.data.get('investigation_id', '')
    doctor_id = request.data.get('doctor_id', '')
    investigation_category = request.data.get('investigation_category', '')
    investigation_name = request.data.get('investigation_name', '')

    # Validate appointment_id
    if not investigation_id:
        res = {'message_code': 999,'message_text': 'Investigation id is required'}
    elif not doctor_id:
        res = {'message_code': 999,'message_text': 'Doctor id is required'}
    elif not investigation_category:
        res = {'message_code': 999,'message_text': 'Investigation category is required'}
    elif not investigation_name:
        res = {'message_code': 999,'message_text': 'Investigation name is required'}
    else:

        try:
            if investigation_id:
                try:
                # Get MedicineInstructions instance
                    investigation_data = {
                            'doctor_id':doctor_id,
                            'investigation_category':investigation_category,
                            'investigation_name':investigation_name
                        }
                    lab_investigation = Tbllabinvestigations.objects.get(investigation_id=investigation_id)


                    serializer = TbllabinvestigationsSerializer(lab_investigation, data=investigation_data, partial=True)
                    if serializer.is_valid():
                        updated_data = serializer.validated_data  # Get the validated data after a successful update
                        serializer.save()

                        res = {
                                'message_code': 1000,
                                'message_text': 'Success',
                                'message_data': {'investigation_id': investigation_id},
                                'message_debug': debug if debug else []
                            }
                    else:
                            res = {
                                'message_code': 2000,
                                'message_text': 'Validation Error',
                                'message_errors': serializer.errors
                            }

                    
                except Tbllabinvestigations.DoesNotExist:
                    res = {'message_code': 999, 'message_text': 'Tbllabinvestigations not found'}

        except Exception as e:
            res = {'message_code': 999, 'message_text': f'Error: {str(e)}',
                   'message_data': [],
                   'message_debug': [] if debug == "" else [{'Debug': debug}]}
    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def fi_delete_labinvestigations(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': [], 'message_debug': debug}
    
    investigation_id = request.data.get('investigation_id', '')

    if not investigation_id:
        res = {'message_code': 999, 'message_text': 'investigation id is required.'}
    else:
        try:
                    investigation_data = {
                            'isdeleted':1
                        }
                    lab_investigation = Tbllabinvestigations.objects.get(investigation_id=investigation_id)


                    serializer = TbllabinvestigationsSerializer(lab_investigation, data=investigation_data, partial=True)
                    if serializer.is_valid():
                        updated_data = serializer.validated_data  # Get the validated data after a successful update
                        serializer.save()

                        res = {
                                'message_code': 1000,
                                'message_text': 'Success',
                                'message_data': {'investigation_id': investigation_id},
                                'message_debug': debug if debug else []
                            }
                    else:
                            res = {
                                'message_code': 2000,
                                'message_text': 'Validation Error',
                                'message_errors': serializer.errors
                            }
        except Exception as e:
            res = {'message_code': 999, 'message_text': f"Error: {str(e)}"}

    return Response(res, status=status.HTTP_200_OK)

####################################new apis#############################################
@api_view(['POST'])
def get_consultation_fee_details(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    consultation_fee_id = request.data.get('consultation_fee_id', None)

    if not consultation_fee_id:
        response_data = {'message_code': 999, 'message_text': 'Consultation Fee ID is required.'}
    else:
        try:
            consultation_fee = ConsultationFee.objects.get(consultation_fee_id=consultation_fee_id, is_deleted=0)
            serializer = ConsultationFeeSerializer(consultation_fee)
            result = serializer.data

            response_data = {
                'message_code': 1000,
                'message_text': 'Consultation Fee details are fetched successfully',
                'message_data': result,
                'message_debug': debug
            }

        except ConsultationFee.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Consultation Fee not found.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_medical_service_fee_details(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    medical_service_fee_id = request.data.get('medical_service_fee_id', None)

    if not medical_service_fee_id:
        response_data = {'message_code': 999, 'message_text': 'Medical Service Fee ID is required.'}
    else:
        try:
            medical_service_fee = MedicalServicesFee.objects.get(medical_service_fee_id=medical_service_fee_id, is_deleted=0)
            serializer = MedicalServicesFeeSerializer(medical_service_fee)
            result = serializer.data

            response_data = {
                'message_code': 1000,
                'message_text': 'Medical Service Fee details are fetched successfully',
                'message_data': result,
                'message_debug': debug
            }

        except MedicalServicesFee.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Medical Service Fee not found.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_consultation_fee_details(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    consultation_fee_id = request.data.get('consultation_fee_id', None)

    if not consultation_fee_id:
        response_data = {'message_code': 999, 'message_text': 'Consultation Fee ID is required in the request body.'}
    else:
        try:
            consultation_fee = ConsultationFee.objects.get(consultation_fee_id=consultation_fee_id, is_deleted=0)
            serializer = ConsultationFeeSerializer(consultation_fee, data=request.data, partial=True)

            if serializer.is_valid():
                updated_instance = serializer.save()
                updated_data = {}

                for field in serializer.fields:
                    if field in serializer.validated_data:
                        updated_data[field] = updated_instance.__getattribute__(field)

                response_data = {
                    'message_code': 1000,
                    'message_text': 'Consultation Fee details are updated successfully',
                    'message_data': updated_data,
                    'message_debug': debug
                }
            else:
                response_data['message_text'] = 'Invalid data provided.'

        except ConsultationFee.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Consultation Fee not found.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_medical_service_fee_details(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    medical_service_fee_id = request.data.get('medical_service_fee_id', None)

    if not medical_service_fee_id:
        response_data = {'message_code': 999, 'message_text': 'Medical Service Fee ID is required in the request body.'}
    else:
        try:
            medical_service_fee = MedicalServicesFee.objects.get(medical_service_fee_id=medical_service_fee_id, is_deleted=0)
            serializer = MedicalServicesFeeSerializer(medical_service_fee, data=request.data, partial=True)

            if serializer.is_valid():
                updated_instance = serializer.save()
                updated_data = {}

                for field in serializer.fields:
                    if field in serializer.validated_data:
                        updated_data[field] = updated_instance.__getattribute__(field)

                response_data = {
                    'message_code': 1000,
                    'message_text': 'Medical Service Fee details are updated successfully',
                    'message_data': updated_data,
                    'message_debug': debug
                }
            else:
                response_data['message_text'] = 'Invalid data provided.'

        except MedicalServicesFee.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Medical Service Fee not found.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_doctor_location_availability(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            data = request.data
            doctor_id = data.get('doctor_id', None)
            availability_day = data.get('availability_day', None)

            if doctor_id is not None and availability_day is not None:
                queryset = Tbldoctorlocationavailability.objects.filter(doctor_id=doctor_id, availability_day=availability_day, isdeleted=0)
                serializer = DoctorLocationAvailabilitySerializer(queryset, many=True)

                if not serializer.data:
                    res['message_text'] = 'Doctor availability not found for the given parameters.'
                    return Response(res, status=status.HTTP_404_NOT_FOUND)

                res = {
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': serializer.data,
                    'message_debug': debug if debug else []
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                res['message_text'] = 'Doctor ID and availability day are required parameters.'
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in get_doctor_location_availability. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def insert_doctor_leave(request):
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': []
    }

    doctor_leave_data = request.data

    # Convert date strings to epoch timestamps
    doctor_leave_data['leave_date'] = convert_to_epoch(doctor_leave_data.get('leave_date'))
    doctor_leave_data['updated_date'] = convert_to_epoch(datetime.today().strftime('%Y-%m-%d'))
    # print(doctor_leave_data['updated_date'])

    doctor_leave_serializer = TbldoctorleaveSerializer(data=doctor_leave_data)

    if doctor_leave_serializer.is_valid():
        doctor_leave_instance = doctor_leave_serializer.save()
        response_data['message_code'] = 1000
        response_data['message_text'] = 'Data successfully saved!'
        response_data['message_data'] = {'doctor_leave_id': doctor_leave_instance.doctor_leave_id}
    else:
        errors = {
            'doctor_leave_errors': doctor_leave_serializer.errors,
        }
        response_data['message_text'] = 'Failed to save data. Please check the errors.'
        response_data['errors'] = errors

    return Response(response_data, status=status.HTTP_200_OK)

def convert_to_epoch(date_str):
    # Convert date string to epoch timestamp
    try:
        date_object = datetime.strptime(date_str, '%Y-%m-%d')
        epoch_timestamp = int(date_object.timestamp())
        return epoch_timestamp
    except ValueError:
        return None
    

####################Get Doctor Leave details by doctor id#############
@api_view(["POST"])
def get_doctor_leave_details(request):
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': []
    }

    try:
        # Get doctor ID from request data
        doctor_id = request.data.get('doctor_id')

        # Get doctor leave details by doctor ID
        doctor_leave_objects = Tbldoctorleave.objects.filter(doctor_id=doctor_id)

        # Serialize the data
        doctor_leave_serializer = TbldoctorleaveSerializer(doctor_leave_objects, many=True)

        # Convert epoch values to date format
        for entry in doctor_leave_serializer.data:
            entry['leave_date'] = datetime.fromtimestamp(entry['leave_date']).strftime("%Y-%m-%d")
            entry['updated_date'] = datetime.fromtimestamp(entry['updated_date']).strftime("%Y-%m-%d")

        response_data['message_code'] = 1000
        response_data['message_text'] = 'Doctor leave details retrieved successfully.'
        response_data['message_data'] = doctor_leave_serializer.data

    except Tbldoctorleave.DoesNotExist:
        response_data['message_text'] = 'Doctor leave details not found.'

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def update_doctor_leave(request):
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': []
    }

    try:
        # Extract data from the request body
        leave_date = request.data.get('leave_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        order = request.data.get('order')

        # Convert leave date to epoch value
        leave_date_epoch = int(datetime.strptime(leave_date, "%Y-%m-%d").timestamp())

        # Get doctor leave objects for the given date
        doctor_leave_objects = Tbldoctorleave.objects.filter(leave_date=leave_date_epoch, order=order)

        if not doctor_leave_objects.exists():
            response_data['message_text'] = 'No doctor leave details found for the given date.'
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Update doctor leave details
        for doctor_leave in doctor_leave_objects:
            # You can update any specific fields here
            doctor_leave.start_time = start_time if start_time is not None else doctor_leave.start_time
            doctor_leave.end_time = end_time if end_time is not None else doctor_leave.end_time
            doctor_leave.updated_date = int(timezone.now().timestamp())

            # Save the updated object
            doctor_leave.save()

        response_data['message_code'] = 1000
        response_data['message_text'] = 'Doctor leave details updated successfully.'
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        response_data['message_text'] = str(e)
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def get_doctor_profileby_token(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_login_token = request.data.get('doctor_login_token', None)

    if not doctor_login_token:
        response_data = {'message_code': 999, 'message_text': 'Doctor login token is required.'}
    else:
        try:
            doctor = Tbldoctors.objects.get(doctor_login_token=doctor_login_token)
            serializer = DoctorSerializer(doctor)
            result = serializer.data

            response_data = {
                'message_code': 1000,
                'message_text': 'Doctor details are fetched successfully',
                'message_data': result,
                'message_debug': debug
            }

        except Tbldoctors.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'no doctor token match.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_doctor_related_info(request):
    doctor_id = request.data.get('doctor_id', None)

    if not doctor_id:
        return Response({'message': 'Doctor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the last inserted doctor's related information
        doctor_location = Tbldoctorlocations.objects.filter(doctor_id=doctor_id).values('doctor_location_id').first()
        doctor_availability = Tbldoctorlocationavailability.objects.filter(doctor_id=doctor_id).values('doctor_location_availability_id').first()
        medical_service_fee = MedicalServicesFee.objects.filter(doctor_id=doctor_id).values('medical_service_fee_id').first()
        consultation_fee = ConsultationFee.objects.filter(doctor_id=doctor_id).values('consultation_fee_id').first()

        # Get the last inserted availability ID, consultation fee ID, and medical service fee ID
        doctor_location_id=doctor_location['doctor_location_id']
        last_availability_id = doctor_availability['doctor_location_availability_id']+20 if doctor_availability else None
        last_medical_service_fee_id = medical_service_fee['medical_service_fee_id']+2 if medical_service_fee else None
        last_consultation_fee_id = consultation_fee['consultation_fee_id']+2 if consultation_fee else None

        response_data = {
            'doctor_location_id':doctor_location_id,
            'last_availability_id': last_availability_id,
            'last_medical_service_fee_id': last_medical_service_fee_id,
            'last_consultation_fee_id': last_consultation_fee_id,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Tbldoctors.DoesNotExist:
        return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)


