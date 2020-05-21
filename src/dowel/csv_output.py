"""A `dowel.logger.LogOutput` for CSV files."""
import csv
import warnings

from dowel import TabularInput
from dowel.simple_outputs import FileOutput
from dowel.utils import colorize


class CsvOutput(FileOutput):
    """CSV file output for logger.

    :param file_name: The file this output should log to.
    """

    def __init__(self, file_name):
        super().__init__(file_name,
                         mode='w+')  # opens a new file for reading and writing
        self._writer = None
        self._fieldnames = None
        self._warned_once = set()
        self._disable_warnings = False

    @property
    def types_accepted(self):
        """Accept TabularInput objects only."""
        return (TabularInput, )

    def record(self, data, prefix=''):
        """Log tabular data to CSV."""
        if isinstance(data, TabularInput):
            datadict = data.as_primitive_dict

            if not datadict.keys() and not self._writer:
                return

            # If its the first call to record, then write header
            if not self._writer:
                self._fieldnames = set(datadict.keys())
                self._writer = csv.DictWriter(self._log_file,
                                              fieldnames=self._fieldnames,
                                              extrasaction='ignore')
                self._writer.writeheader()

            # If new keys are added, then add extra columns to the csv file
            if not self._fieldnames.issuperset(datadict.keys()):
                self.rewriteCSV(datadict.keys())

            # If any key is not present in the latest row,
            # add a blank key-value pair
            for key in self._fieldnames:
                if key not in datadict:
                    datadict[key] = ''
            self._writer.writerow(datadict)

            for k in datadict.keys():
                data.mark(k)
        else:
            raise ValueError('Unacceptable type.')

    def rewriteCSV(self, fieldnames):
        """Rewrite the CSV file to accommodate the extra fieldnames.

        This function will read the file, store the data,
        and rewrite it back to the file after adding the
        additional fields to all the entries.
        The value of this column will be blank in these cells

        :param fieldnames: The new set of fieldnames
        """
        # read data from file into a list
        self._log_file.seek(0)
        csv_reader = csv.DictReader(self._log_file)
        csvdata = [row for row in csv_reader]

        # clearing the file
        self._log_file.truncate(0)
        self._log_file.seek(0)

        # output data back to the file with extra fields
        for key in fieldnames:
            if key not in self._fieldnames:
                self._fieldnames.add(key)

        self._writer = csv.DictWriter(self._log_file,
                                      fieldnames=self._fieldnames,
                                      extrasaction='ignore')

        self._writer.writeheader()
        for row in csvdata:
            # There are keys which are not set in the current tabular record
            # Setting them to blank
            for curfield in self._fieldnames:
                if curfield not in row:
                    row[curfield] = ''

            self._writer.writerow(row)

    def _warn(self, msg):
        """Warns the user using warnings.warn.

        The stacklevel parameter needs to be 3 to ensure the call to logger.log
        is the one printed.
        """
        if not self._disable_warnings and msg not in self._warned_once:
            warnings.warn(colorize(msg, 'yellow'),
                          CsvOutputWarning,
                          stacklevel=3)
        self._warned_once.add(msg)
        return msg

    def disable_warnings(self):
        """Disable logger warnings for testing."""
        self._disable_warnings = True


class CsvOutputWarning(UserWarning):
    """Warning class for CsvOutput."""

    pass
