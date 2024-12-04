# integration tests for FileHandler classes in File_Handler.py and Polar_File_Handler.py
# since they have the same API we'll combine them in 1 parameterized test class

import os
import pytest
import pandas as pd
from ...File_Handler import FileHandler as fh
from ...Polar_File_Handler import FileHandler as pfh


@pytest.mark.parametrize('fh', [fh, pfh], ids=["File_Handler", "Polar_File_Handler"])
@pytest.mark.parametrize('tnum', [10]) # (right now default amount of threads is 10) # TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!! add 1 as option for thread_num
class TestFileHandler:
    input = os.path.join("customer_data", "GRI_2017_2020.xlsx")
    output = os.path.join("tests", "integration", "Metadata2017_2020.xlsx")
    dest = os.path.join("tests", "integration", "files")


    # helper functions for controlling what files we have downloaded and not
    def remove_dls(self):
        if os.path.exists(self.dest):
            for file in os.listdir(self.dest):
                os.remove(os.path.join("tests", "integration", "files", file))
            os.rmdir(self.dest)

    def remove_metadata(self):
        if os.path.exists(self.output):
            os.remove(self.output)

    def clean_slate(self):
        self.remove_dls()
        self.remove_metadata()


    # FileHandler's 2 functions return nothing so testing will need to consist of checking side effects

    def crossreference_metadata(self):
        meta = pd.read_excel(self.output)
        for row in meta.itertuples():
            if row.pdf_downloaded == "yes" and os.path.exists(os.path.join(self.dest, f"{row.BRnum}.pdf")):
                continue
            elif row.pdf_downloaded == "no" and not os.path.exists(os.path.join(self.dest, f"{row.BRnum}.pdf")):
                continue
            else:
                assert False, f"The downloaded pdf's ({row.BRnum}) existence did not correspond to its status ({row.pdf_downloaded}) in metadata file"

    # TODO mock out the excel input
    # TODO check contents of metadata with downloaded files

    # start_download
    def test_start_download_clean(self, fh, tnum):
        """
        Test start_download() from a clean slate (no previously downloaded files, no metadata file).
        Checking that files logged as downloaded in metadata file are actually present in downloads folder
        """
        self.clean_slate()

        fh = fh(tnum)
        fh.start_download(self.input, self.output, self.dest)

        # check side effects
        self.crossreference_metadata()


    def test_start_download_unclean(self, fh, tnum):
        """
        Test start_download() from an unclean slate (previously downloaded files, metadata file).
        Checking that files logged as downloaded in metadata file are actually present in downloads folder
        """
        self.clean_slate()

        fh = fh(tnum)
        fh.start_download(self.input, self.output, self.dest)
        fh.start_download(self.input, self.output, self.dest)
        
        # check side effects
        self.crossreference_metadata()
        # other stuff to check?

    
    # def test_start_download_no_meta(self, fh, tnum):
    #     fh = fh(tnum)
    #     fh.start_download(self.input, self.output, self.dest)
    #     self.remove_metadata()
    #     fh.start_download(self.input, self.output, self.dest)
    #     # (check side effects...)

    #     self.clean_slate()

    # def test_start_download_no_dls(self, fh, tnum):
    #     fh = fh(tnum)
    #     fh.start_download(self.input, self.output, self.dest)
    #     self.remove_dls()
    #     fh.start_download(self.input, self.output, self.dest)
    #     # (check side effects...)

    #     self.clean_slate()


    # download_thread