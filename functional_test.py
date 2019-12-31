from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import unittest


class NewVistorTest(unittest.TestCase):
    def setUp(self): # 테스트 시작 때 실행 된다
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3) # 페이지 로딩이 끝나고 테스트가 실행되는 것을 확실히 하기 위해서

    def tearDown(self):# 테스트 마지막에 실행 된다(에러가 발생해도 실행된다)
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
