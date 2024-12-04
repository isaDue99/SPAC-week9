# integration test for controller.py with pytest

import argparse
from ...Controller import Controller

class TestController:
    input_file = "input.xlsx"
    output_file = "output.xlsx"
    destination_folder = "destination"

    # (tests of run() reserved for integration tests)

    # run with and without threads?