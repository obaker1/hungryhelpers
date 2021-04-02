import unittest
from hungryhelpers.parserStudent import read_data


class ParseCSVTest(unittest.TestCase):

    def setUp(self):
        self.data = 'studentData.txt'

   # Test to read the headers
    def test_csv_read_data_headers(self):
        self.assertEqual(
            read_data(self.data)[0],
            ['ID', 'LastName', 'FirstName', 'Age', 'SchoolLocation','address', 'city', 'state', 'zip','grade']
       )

   # Test to read the student ID
    def test_csv_read_data_student_ID(self):
        self.assertEqual(read_data(self.data)[1][0], 'FR0RI64GK')

   # Test to read last name
    def test_csv_read_data_last_name(self):
        self.assertEqual(read_data(self.data)[1][1],'Wheeler')

   # Test to read first name
    def test_csv_read_data_first_name(self):
        self.assertEqual(read_data(self.data)[1][2], 'Koen')

   # Test to read age
    def test_csv_read_data_age(self):
        self.assertEqual(read_data(self.data)[1][3], '12')

   # Test to read school location
    def test_csv_read_school_location(self):
        self.assertEqual(read_data(self.data)[1][4], 'Arbutus Middle')

    # Test to read address
    def test_csv_read_student_address(self):
        self.assertEqual(read_data(self.data)[1][5], '1234 Lane Drive')

    def test_csv_read_city(self):
        self.assertEqual(read_data(self.data)[1][6], 'Catonsville')


    def test_csv_read_state(self):
        self.assertEqual(read_data(self.data)[1][7], 'MD')

    def test_csv_read_zip(self):
        self.assertEqual(read_data(self.data)[1][8], '21166')


    def test_csv_read_grade(self):
        self.assertEqual(read_data(self.data)[1][9], '7')


if __name__ == '__main__':
   unittest.main()
