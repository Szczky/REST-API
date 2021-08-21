from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUrls(SimpleTestCase):

    def test_newUser_url(self):
        """Es kontrolliert, ob der URL Name passt"""
        path=resolve('/user/')
        self.assertEquals(path.url_name, 'newUser')


    def test_newKurs_url(self):
        """Es kontrolliert, ob der URL Name passt"""
        path=resolve('/kurs/')
        self.assertEquals(path.url_name, 'newKurs')


    def test_newLecturer_url(self):
        """Es kontrolliert, ob der URL Name passt"""
        path = resolve('/lecturer/')
        self.assertEquals(path.url_name, 'newLecturer')


    def test_newLearningItem_url(self):
        """Es kontrolliert, ob der URL Name passt"""
        path=resolve('/learning_item/')
        self.assertEquals(path.url_name, 'newLearningItem')


    def test_userUpdateDelete_url(self):
        """Es kontrolliert, ob der URL Name passt"""
        url = reverse('kb_service:userUpdateDelete', args=['U3'])
        self.assertEqual(url, '/user/U3')

    def test_lecturerUpdate_url(self):
        """Es kontrolliert, ob der URL Name passt"""
        url = reverse('kb_service:lecturerUpdate', args=['L3'])
        self.assertEqual(url, '/lecturer/L3')


    def test_learningItemUpdate_url(self):
        """Es kontrolliert, ob der URL Name passt"""
        url = reverse('kb_service:learningItemDelete', args=['LI1'])
        self.assertEqual(url, '/learning_item/LI1')



