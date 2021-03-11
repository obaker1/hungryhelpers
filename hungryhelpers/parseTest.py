import unittest
from parserStudent import read_data


class ParseCSVTest(unittest.TestCase):

   def setUp(self):
       self.data = 'studentData.txt'

   # Test to read the headers
   def test_csv_read_data_headers(self):
       self.assertEqual(
           read_data(self.data)[0],
           ['ID', 'LastName', 'FirstName', 'Age', 'SchoolLocation']
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


if __name__ == '__main__':
   unittest.main()
