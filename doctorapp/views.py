from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView

from medicify_project.models import * 
from medicify_project.serializers import *
from django.db.models import Q
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
                                 'medicine_preservation', 'medicine_min_stock', 'medicine_gst', 'medicine_content_name',
                                 'doctor_id']

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
                doctor_medicine = TbldoctorMedicines.objects.get(doctor_medicine_id=doctor_medicine_id)
                serializer = TbldoctorMedicinesSerializer(doctor_medicine)

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
                
                doctor_medicines_queryset = TbldoctorMedicines.objects.filter(doctor_id=doctor_id)

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
                    'message_data': updated_data,
                    'message_debug': debug if debug else []
                }
                return Response(res, status=status.HTTP_200_OK)

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
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        if request.method == 'POST':
            doctor_location_id = request.data.get('doctor_location_id')
            
            try:
                doctor_location = Tbldoctorlocations.objects.get(doctor_location_id=doctor_location_id)
                serializer = DoctorLocationSerializer(doctor_location)

                res = {
                    'message_code': 1000,
                    'message_text': 'Success',
                    'message_data': serializer.data,
                    'message_debug': [{"Debug": debug}] if debug != "" else []
                }
            except Tbldoctorlocations.DoesNotExist:
                res = {
                    'message_code': 900,
                    'message_text': 'Doctor location not found.',
                    'message_data': {},
                    'message_debug': [{"Debug": debug}] if debug != "" else []
                }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': 'Doctor location id is Required',
            'message_data': {},
            'message_debug': [{"Debug": debug}] if debug != "" else []
        }

    return Response(res, status=status.HTTP_404_NOT_FOUND if res['message_code'] == 900 else status.HTTP_200_OK)

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
            doctor = Tbldoctors.objects.get(doctor_id=doctor_id)
            serializer = DoctorSerializer(doctor)
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

    consultation_fee_data = data.get('consultation_fee', {})
    consultation_fee_data['doctor_id'] = doctor_id
    consultation_fee_data['location_id'] = location_id

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
