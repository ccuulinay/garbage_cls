proxies = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080"
    # "all_proxy": "socks5h://127.0.0.1:1080",
}

google_search_base_url = "https://www.google.com/search?q="
google_image_tail = "&source=lnms&tbm=isch"

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

level0_label_encoding_dict = {0: '可回收物', 2: '有害垃圾', 3: '湿垃圾', 1: '干垃圾'}