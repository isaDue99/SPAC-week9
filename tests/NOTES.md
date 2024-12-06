Notes on discoveries made while debugging this foreign/unknown codebase

# oddities

## bugs
- controller.py uses polar_file_handler.py by default, but requirements.txt is missing the xlsxwriter module imported there
- commandline setting a report file results in AttributeError due to a spelling mistake in the name of set_report_file()
- the output metadata spreadsheet doesn't reflect what files were actually downloaded
    - spreadsheet claims several files were downloaded when they are nowhere to be found in the downloaded files, and vice versa
    - of the 20 downloaded files, 11 are incorrectly marked in the metadata spreadsheet
    - BR50046 is missing from the list entirely (note: corresponding row in input file is lacking links entirely)
    - the BRnum column is ordered aplhabetically except for rows BR50048 and BR50049, which have switched places
- using polar_file_handler also outputs a weird metadata spreadsheet
    - 10 of the 20 rows in spreadsheet were incorrect
    - BR50046 was present in the list

## peculiar design
- program by default will only process 20 rows of the input file each time it's ran, and offers no commandline options to change this
- no instructions clarifying that input files should be located in a folder named /customer_data


# changes from initial fork of codebase (aside from tests)

- Controller.py:1: changed ```from Polar_File_Handler import FileHandler``` to ```from File_Handler import FileHandler``` since polar_file_handler is missing an import
    - changed this back and added xlxswriter to requirements.txt


# tests

## to run tests

from top of directory: 
```
python -m pytest
```

## unit
- [x] controller.py
- [x] downloader.py
- (SCRAPPED) file_handler.py (- FileHandler's 2 functions are too involved to unittest properly with the time available, somewhat covered by file_handler integration tests)
- (SCRAPPED) polar_file_handler.py (- same^)

## integration
- [x] file_handler importing downloader
- (SCRAPPED) controller importing file_handler (- run() in Controller is too simple to warrant tests of its own, is already covered by file_handler integration tests)