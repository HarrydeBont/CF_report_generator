# from logger_utils import log_info, log_function_name, log_exception
# import logging

# Get a logger specific to this module
# logger = logging.getLogger(__name__) # creates a logger that is specific to the APIKeyHandler module. The __name__ variable in Python modules contains the name of the module, so each module gets its own logger.

global tester, max_attempts, developer
tester = False
developer = True
max_attempts = 5


def set_tester():
    """Sets the application to tester mode."""
    # log_function_name()
    global tester, max_attempts, developer
    tester = True
    developer = False
    max_attempts = 5
    

def set_developer():
    """
    Sets the application to developer mode.
    GitHub activated
    """
    # log_function_name()
    global tester, max_attempts, developer
    tester = False
    developer = True
    max_attempts = 5
   


def set_production():
    """Sets the application to production mode."""
    # log_function_name()
    global tester, max_attempts, developer
    tester = False
    developer = False
    max_attempts = 30

def get_program_mode():
    # log_function_name()
    global tester, max_attempts, developer
    return tester, developer, max_attempts

def get_developer():
    # log_function_name()
    global developer
    return developer
