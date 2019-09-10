#!/usr/bin/env python
# coding: utf-8



import os

proxy = "socks5h://127.0.0.1:1080"

os.environ['http_proxy'] = proxy 
os.environ['https_proxy'] = proxy


import requests
from bs4 import BeautifulSoup
import pprint
from urllib.parse import quote
import json
import copy
import glob
import logging
import time
from pathlib import Path

from spiders.categories import SH_GARBAGE_CLS_CAT
from config import google_search_base_url, google_image_tail
from config import headers


# final target is to get a name pattern with concated level x name, and sample name
# eg: lv0Name_lv1Name_sampleName_, 可回收物_废纸张_报纸
# DFS.

def levelx_processing(level_cat, cur_pattern=None, samples=[]):
    if cur_pattern:
        cur_pattern = cur_pattern
    else:
        cur_pattern = list()
    level_name = level_cat.get("zh_name", "unknown")
    sub_class_samples_list = []
    # samples = []
    cur_pattern.append(level_name)
    if "sub_class" in level_cat.keys():
        sub_level = level_cat['sub_class']
        for sl in sub_level:
            temp_cur_pattern = copy.deepcopy(cur_pattern)
            sub_class_samples = levelx_processing(sl, cur_pattern=temp_cur_pattern, samples=samples)
            if sub_class_samples:
                sub_class_samples_list.extend(sub_class_samples)
        # print(len(sub_class_samples_list))
    if "sample" in level_cat.keys():
        # print(cur_pattern)
        for sample_name in level_cat['sample']:
            temp_cur_pattern = copy.deepcopy(cur_pattern)
            temp_cur_pattern.append(sample_name)
            # print("-------------{}".format(temp_cur_pattern))
            samples.append(temp_cur_pattern)
        # print(len(samples))
        samples.extend(sub_class_samples_list)
        return samples


lv_names = []       
for i in SH_GARBAGE_CLS_CAT:
    x = levelx_processing(i)
    if x:
        lv_names.extend(x)


def google_target_images(query_kw):
    google_image_url = google_search_base_url+quote(str(query_kw).encode('utf8'))+google_image_tail
    res = requests.get(google_image_url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # rg_meta is the class name keyword to locate target divs
        # ou is the source image url
        # oh is the height
        # ow is the width
        # ity is the format
        soup.find_all("div",{"class":"rg_meta"})
        # print(soup.prettify())
        target_images = []
        for div in soup.find_all("div",{"class":"rg_meta"}):
            url, img_type = json.loads(div.text)['ou'], json.loads(div.text)['ity']
            target_images.append((url, img_type))
        return target_images
    else:
        raise Exception("Error when proceed requests.")


def google_download_target_images(image_url, image_format, save_file_prefix, save_path="./data"):
    res = requests.get(image_url, headers=headers)
    save_p = Path(save_path)
    save_p.mkdir(parents=True, exist_ok=True)
    if res.status_code == 200:
        try:
            raw_img = res.content
            count = len(list(save_p.glob(str(save_file_name)+"*"))) + 1
            if not image_format:
                save_suffix = "jpg"
            else:
                save_suffix = image_format
            
            file_path = save_p / str(str(save_file_prefix) + "_" + str(count) + "." + save_suffix)
            with open(file_path, "wb") as f:
                f.write(raw_img)
            time.sleep(0.6)
        except Exception as e:
            logging.warning("Exception as {}".format(e))
        
    else:
        raise Exception("Error when download image.")


count = 0
sleep_interval = 10
for i in lv_names[:]:
    query_sample = i[-1]
    save_file_name = "_".join(i)
    target_images = google_target_images(query_sample)
    logging.warning(len(target_images))
    for image_url, image_format in target_images[:]:
        google_download_target_images(image_url, image_format, save_file_name, save_path="../data")
        # Counter number of request, sleep 5 seconds every 50 requests.
        count += 1
        if count % sleep_interval == 0:
            time.sleep(3)


