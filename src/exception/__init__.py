import os
import sys
import logging

## User define function to read errors in the system
def error_message_details(error: Exception, error_details: sys) ->str:
    """
    Extract detailed error information including 
    1. file name,
    2. line number,
    3. error message.

    parameters:
              1. error: The exception that occurred in the system.
              2. error_details: The sys module to access traceback details.
              3. -> str : Return a formatted error message as string.
    """
    # extract traceback details (exception information)
    _,_, exc_tab = error_details.exc_info()

    ##give us the filename where the exception is raise
    file_name=exc_tab.tb_frame.f_code.co_filename

    #create a formatted  error message with filename, line number, and error
    line_number=exc_tab.tb_lineno
    error_message=f'Error occurred in python file:[{file_name}] at line number: [{line_number}]: {str(error)}'

    ##log error
    logging.error(error_message)
    return error_message


class MyException(Exception):
    """
    Custom exceptional class for handlling errors in my fossil age prediction 
    software/application. 
    """
    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes the exception with a detailed error message.
        param:
            1. error_message - A string describing the error.
            2. error_detail - The sys module to sccess traceback details.
        """
        # call the base class(Exception) constructor with the error message
        super().__init__(error_message)
        self.error_message = error_message_details(error=error_message, error_details=error_detail)
        # return self.error_message
    
    def __str__(self)->str:
        """Returns the string representation formatted error message"""
        return self.error_message
