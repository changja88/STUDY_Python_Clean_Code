import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class NewVistorTest(unittest.TestCase):
    def setUp(self):  # 테스트 시작 때 실행 된다
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3)  # 페이지 로딩이 끝나고 테스트가 실행되는 것을 확실히 하기 위해서

    def tearDown(self):  # 테스트 마지막에 실행 된다(에러가 발생해도 실행된다)
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_id('tr')
        self.assertIn('1: 공작깃털 사기', [row.text for row in rows])
        self.assertIn(
            '2: 공작깃털을 이용해서 그물 만들기',
            [row.text for row in rows]
        )

        self.fail('Finish the Test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
