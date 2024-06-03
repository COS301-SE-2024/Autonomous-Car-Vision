from django.test import TestCase
from testApp.models import User

# Create your tests here.
class UserTestCase(TestCase):
    # Set up function
    def createUserTest(self):
            User.objects.Create(uid="99999999999", uname="Bob", uemail="bob@thebuilder.com")

    def testcase1(self):
        pass

    def testcase2(self):
        pass

    def testcase3(self):
        pass