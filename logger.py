import logging
import sys

def setup_logging(executable_name):
    # Create a logger object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set the level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the console handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create a file handler and set the level to debug
    file_handler = logging.FileHandler(f'{executable_name}.log')
    file_handler.setLevel(logging.DEBUG)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    
    return logger