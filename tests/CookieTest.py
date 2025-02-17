import re
import unittest
import requests
import browser_cookie3

class CookieTest(unittest.TestCase):

    def testCookie(self):
        get_title = lambda html: re.findall('<title>(.*?)</title>', html, flags=re.DOTALL)[0].strip()
        cj = browser_cookie3.chrome(domain_name='github.com')
        r = requests.get('https://github.com/true2blue', cookies=cj, verify=False)
        title = get_title(r.content.decode('utf-8'))
        self.assertEqual(title, 'true2blue')

        cookie_str = ''
        for cookie in cj:
            cookie_str += f"{cookie.name}={cookie.value}; "
        print(cookie_str)

if __name__ == "__main__":
    unittest.main()