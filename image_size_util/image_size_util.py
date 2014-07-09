#-*- coding: utf-8
from http_util import http_util

from exceptions import (
    Error,
    NotPngError,
    NotGifError,
    NotJpgError,
    JpgDecodingError
)

def hex_to_int(hex_str):
    import binascii
    return int(binascii.hexlify(hex_str), 16)

def process_image(url, page_url=""):
    ret = (-1, -1)
    try:
        h_util = http_util()
        h_util.request(url, page_url)
        type = h_util.get_image_type()

        first_byte = h_util.read(1)
        if first_byte == "\x89":
            ret = process_png(h_util)
        elif first_byte == "G":
            ret = process_gif(h_util)
        elif first_byte == "\xff":
            ret = process_jpg(h_util)
        else:
            print "Type is not matched : %s(%s)" % (type, url)
    except Error:
        h_util.close()
        raise
    except Exception, msg:
        h_util.close()
        pass

    return ret

def process_png(fp):
    # PNG SIGNATURE CHECK
    png_type = fp.read(7)
    if png_type != "PNG\r\n\x1a\n":
        raise NotPngError()

    byte   = hex_to_int(fp.read(4).strip("\r"))
    type   = fp.read(4)
    width  = hex_to_int(fp.read(4).strip("\r"))
    height = hex_to_int(fp.read(4).strip("\r"))

    return (width, height)

def process_gif(fp):

    # GIF SIGNATURE CHECK
    signature = fp.read(2)
    version = fp.read(3)
    if signature != "IF" or version not in ("87a", "89a"):
        raise NotGifError()


    width  = hex_to_int(fp.read(1)) | (hex_to_int(fp.read(1)) << 8)
    height = hex_to_int(fp.read(1)) | (hex_to_int(fp.read(1)) << 8)

    return (width, height)

def process_jpg(fp):
    M_SOF0  = "\xc0"
    M_SOF1  = "\xc1"
    M_SOF2  = "\xc2"
    M_SOF3  = "\xc3"
    M_SOF5  = "\xc5"
    M_SOF6  = "\xc6"
    M_SOF7  = "\xc7"
    M_SOF9  = "\xc9"
    M_SOF10 = "\xca"
    M_SOF11 = "\xcb"
    M_SOF13 = "\xcd"
    M_SOF14 = "\xce"
    M_SOF15 = "\xcf"
    M_SOI   = "\xd8"
    M_EOI   = "\xd9"
    M_SOS   = "\xda"
    M_JFIF  = "\xe0"
    M_EXIF  = "\xe1"
    M_XMP   = "\x10\xe1"
    M_COM   = "\xfe"
    M_DQT   = "\xdB"
    M_DHT   = "\xc4"
    M_DRI   = "\xdd"
    M_IPTC  = "\xed"

    if fp.read(1) != M_SOI:
        raise NotJpgError()

    while True:
        prev = "\x00"

        for i in xrange(11):
            marker = fp.read(1)
            if (marker != "\xff" and prev == "\xff"): break
            prev = marker
        else:
            raise JpgDecodingError("Extraneous padding bytes before section %c" % marker)

        lh = fp.read(1)
        ll = fp.read(1)

        itemlen = (hex_to_int(lh) << 8) | hex_to_int(ll)
        if itemlen < 2:
            raise JpgDecodingError("itemlen is less than 2")

        data = fp.read(itemlen - 2)
        if marker == M_SOS:
            raise JpgDecodingError("PSEUDO_IMAGE_MARKER")
        elif marker == M_EOI:
            raise JpgDecodingError("No image in jpeg")
        elif marker == M_JFIF:
            if itemlen < 16:
                raise JpgDecodingError("Header missing JFIF marker")
        elif marker in(M_EXIF, M_IPTC, M_COM):
            continue
        elif marker in (M_SOF0, M_SOF1, M_SOF2, M_SOF3, M_SOF5, M_SOF6, M_SOF7, M_SOF9, M_SOF10, M_SOF11, M_SOF13, M_SOF14, M_SOF15):
            width  =  (hex_to_int(data[3]) << 8) | hex_to_int(data[4])
            height =  (hex_to_int(data[1]) << 8) | hex_to_int(data[2])
            break

    return (width, height)

if __name__ == "__main__":
    print process_image("https://assets-cdn.github.com/images/modules/logos_page/Octocat.png")
