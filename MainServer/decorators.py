import functools
import builtins
from flask import request
import MainServer.exceptions as exceptions


def catch_errors(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result

        except Exception as e:
            status_code = e.status_code if hasattr(e, 'status_code') else 500
            return {'message': f'Error occurred during processing {func.__name__}',
                    'error_details': f'{type(e)} : {str(e)}'}, status_code

    return wrapped_func


def required_structure(structure):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request_data = request.json

            check_list(request_data, structure, 'request json body')

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def check_list(data_dict, structure, data_name):
    for field_struct in structure:

        match type(field_struct):
            case builtins.str:

                if type(data_dict) != builtins.dict:
                    raise exceptions.WrongFieldType(type(data_dict), data_name)

                if not data_dict.get(field_struct):
                    raise exceptions.RequiredFieldMissing(field_struct, data_name)

            case builtins.dict:
                field_name = list(field_struct.keys())[0]
                if not (field_value := data_dict.get(field_name)):
                    raise exceptions.RequiredFieldMissing(field_name, data_name)
                check_list(field_value, field_struct[field_name], f'field {field_name} in {data_name}')
