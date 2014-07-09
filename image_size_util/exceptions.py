#-*- coding: utf-8

class Error(Exception):
    pass

class NotPngError(Error):
    pass

class NotGifError(Error):
    pass

class NotJpgError(Error):
    pass

class JpgDecodingError(Error):
    pass

