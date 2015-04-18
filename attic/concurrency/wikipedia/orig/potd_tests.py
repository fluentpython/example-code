
import unittest

import potd

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.thumb_url = ("""http://upload.wikimedia.org/wikipedia/"""
            """commons/thumb/f/fe/Orthographic_projection_SW.jpg/350px"""
            """-Orthographic_projection_SW.jpg""")

    def test_buid_page_url(self):
        date = '2014-05-01'
        result = potd.build_page_url(date)
        self.assertEqual(result, 'http://en.wikipedia.org/wiki/Template:POTD/2014-05-01')

    def test_fetch_status_code(self):
        date = '2014-05-02'
        url = potd.build_page_url(date)
        response = potd.fetch(url)
        self.assertEqual(response.status_code, 200)

    def test_fetch_status_code_not_found(self):
        date = '2100-01-01'
        url = potd.build_page_url(date)
        response = potd.fetch(url)
        self.assertEqual(response.status_code, 404)

    def test_extract_image_url(self):
        image_url = potd.extract_image_url(HTML)
        self.assertEqual(image_url, self.thumb_url)

    def test_fetch_image_jpeg(self):
        response = potd.fetch(self.thumb_url)
        self.assertEqual(response.headers['content-type'], 'image/jpeg')

    def test_list_days_of_month(self):
        year = 2014
        month = 5
        days = potd.list_days_of_month(year, month)
        self.assertEqual(len(days), 31)
        self.assertEqual('2014-05-01', days[0])
        self.assertEqual('2014-05-31', days[-1])

    def test_list_days_of_february(self):
        year = 2014
        month = 2
        days = potd.list_days_of_month(year, month)
        self.assertEqual(len(days), 28)
        self.assertEqual('2014-02-01', days[0])
        self.assertEqual('2014-02-28', days[-1])

    def test_format_date(self):
        year = 2014
        month = 2
        day = 1
        a_date = '2014-02-01'
        date = potd.format_date(year, month, day)
        self.assertEqual(a_date, date)
        self.assertEqual(potd.format_date(2010, 11, 12), '2010-11-12')

    def test_build_save_path(self):
        date = '2014-06-04'
        path = potd.SAVE_DIR + date + '_350px-Orthographic_projection_SW.jpg'
        self.assertEqual(path, potd.build_save_path(date, self.thumb_url))


HTML = (
'''<td><a href="/wiki/File:Orthographic_projection_SW.jpg" class="image"
title="Orthographic projection"><img alt="Orthographic projection"
src="//upload.wikimedia.org/wikipedia/commons/thumb/f/fe/O'''
'''rthographic_projection_SW.jpg/350px-Orthographic_projection_SW.jpg"
width="350" height="350" srcset="//upload.wikimedia.org/wikipedia/comm'''
'''ons/thumb/f/fe/Orthographic_projection_SW.jpg/525px-
Orthographic_projection_SW.jpg 1.5x, //upload.wikimedia.org/wikipedia/
commons/thumb/f/fe/Orthographic_projection_SW.jpg/700px-
Orthographic_projection_SW.jpg 2x" data-file-width="2058" data-file-
height="2058"></a></td>
''')

if __name__ == '__main__':
    unittest.main()













