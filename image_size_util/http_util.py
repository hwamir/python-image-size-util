#-*- coding: utf-8
import httplib
import urlparse

class http_util(object):
    def __init__(self):
        self.url      = ""
        self.conn     = None
        self.type     = None
        self.response = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()
        self.url      = ""
        self.conn     = None
        self.type     = None
        self.response = None

    def request(self, image_url, page_url=""):
        if self.conn is not None:
            self.conn.close()

        parsed = urlparse.urlparse(image_url)
        self.conn = httplib.HTTPConnection(parsed[1])

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.60 Safari/537.1", "Referer": page_url}

        self.conn.request("GET", "".join(parsed[2:]), headers=headers)

        self.response = self.conn.getresponse()
        self.type = self.response.getheader("Content-Type")
        self.url    = image_url

    def get_image_type(self):
        ret = ""

        if self.type.find("image") >= 0:
            ret = self.type.replace("image/", "")

        return ret

    def read(self, len):
        if self.conn is not None and self.response is not None:
            return self.response.read(len)
        return None

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn     = None
            self.type     = None
            self.response = None
            self.url      = ""

if __name__ == "__main__":
    a = http_util()
    a.request("https://assets-cdn.github.com/images/modules/logos_page/Octocat.png")
