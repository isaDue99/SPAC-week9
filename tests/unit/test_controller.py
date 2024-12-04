# unit tests for controller.py with pytest

from ...Controller import Controller

class TestController:
    input_file = "input.xlsx"
    output_file = "output.xlsx"
    destination_folder = "destination"

    def test_set_url_file(self):
        c = Controller()
        c.set_url_file(self.input_file)
        assert c.url_file_name == self.input_file

    def test_set_report_file(self):
        c = Controller()
        c.set_report_file(self.output_file)
        assert c.report_file_name == self.output_file

    def test_set_destination(self):
        c = Controller()
        c.set_destination(self.destination_folder)
        assert c.destination == self.destination_folder

    # run() is so reliant on FileHandler that we'll save it for those tests