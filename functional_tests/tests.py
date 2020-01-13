import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class NewVistorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):  # 테스트 시작 때 실행 된다
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3)  # 페이지 로딩이 끝나고 테스트가 실행되는 것을 확실히 하기 위해서

    def tearDown(self):  # 테스트 마지막에 실행 된다(에러가 발생해도 실행된다)
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(' 공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(' 공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 새로운 사용자 francis
        # edith의 리스트는 보이지 않는다
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('우유사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유사기')
        inputbox.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유사기', page_text)

        self.fail('Finish te Test!')

    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1080, 720)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=300
        )
