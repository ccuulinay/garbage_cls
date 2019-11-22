#!/usr/bin/env python
# coding: utf-8



import os

proxy = "socks5h://127.0.0.1:1081"

os.environ['http_proxy'] = proxy 
os.environ['https_proxy'] = proxy


import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
import copy
import glob
import logging
import time
from pathlib import Path

from category import categories
from category import  categories_service
import importlib

from category.categories import SH_GARBAGE_CLS_CAT, GZ_GARBAGE_CLS_CAT
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
        sub_levels = level_cat['sub_class']
        for sl in sub_levels:
            temp_cur_pattern = copy.deepcopy(cur_pattern)
            sub_class_samples = levelx_processing(sl, cur_pattern=temp_cur_pattern, samples=samples)
            if sub_class_samples:
                sub_class_samples_list.extend(sub_class_samples)
        # print(len(sub_class_samples_list))
    if "sample" in level_cat.keys():
        for sample_name in level_cat['sample']:
            temp_cur_pattern = copy.deepcopy(cur_pattern)
            temp_cur_pattern.append(sample_name)
            # print("-------------{}".format(temp_cur_pattern))
            samples.append(temp_cur_pattern)
        # print(len(samples))
        if len(level_cat['sample']) == 0:
            samples.append(cur_pattern)
        samples.extend(sub_class_samples_list)
        return samples


def google_target_images(query_kw):
    logging.warning(query_kw)
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
            count = len(list(save_p.glob(str(save_file_prefix)+"*"))) + 1
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


def _proceed_download(lv, start_image, max_end_image, except_temp_file, save_path):
    count = 0
    sleep_interval = 10
    query_sample = lv[-1]
    save_file_name = "_".join(lv)
    target_images = google_target_images(query_sample)
    logging.warning(query_sample)
    logging.warning(len(target_images))
    temp_end_image = min(max_end_image, len(target_images))
    current_num = len(glob.glob(save_path + "/" + save_file_name + "*"))
    temp_start_image = max(start_image, current_num+1)
    for image_url, image_format in target_images[temp_start_image:temp_end_image]:
        try:
            google_download_target_images(image_url, image_format, save_file_name, save_path=save_path)
        except:
            with open(except_temp_file, "w") as f:
                f.write(save_file_name)
                current_num = len(glob.glob(save_path+"/"+save_file_name+"*"))
                f.write("\n")
                f.write(str(current_num))
        # Counter number of request, sleep few seconds every few requests.
        count += 1
        if count % sleep_interval == 0:
            time.sleep(3)
    with open(except_temp_file, "w") as f:
        f.write(save_file_name)
        current_num = len(glob.glob(save_path+"/"+save_file_name+"*"))
        f.write("\n")
        f.write(str(current_num))


# Below begin to work.

def ops():
    lv_names = []
    for i in SH_GARBAGE_CLS_CAT:
        x = levelx_processing(i)
        if x:
            lv_names.extend(x)



    save_path = "../data"
    except_temp_file = "./batch_temp_state.ind"

    if os.path.exists(except_temp_file):
        with open(except_temp_file, "r") as f:
            lasttime_save_file_name = f.readline()
            lasttime_download_num = f.readline()

        last_level = lasttime_save_file_name.replace("\n", "").split("_")
        last_level_index = lv_names.index(last_level)

        print(last_level_index)

    count = 0
    sleep_interval = 10

    if last_level_index and int(lasttime_download_num) >= 59:
        start_level = last_level_index + 1

    end_level = len(lv_names) + 1

    start_image = 0
    max_end_image = 60

    if last_level_index and int(lasttime_download_num) < 59:
        i = lv_names[last_level_index]
        query_sample = i[-1]
        save_file_name = "_".join(i)
        target_images = google_target_images(query_sample)
        temp_end_image = min(max_end_image, len(target_images))
        for image_url, image_format in target_images[int(lasttime_download_num):temp_end_image]:
            try:
                google_download_target_images(image_url, image_format, save_file_name, save_path=save_path)
            except:
                with open(except_temp_file, "w") as f:
                    f.write(save_file_name)
                    current_num = len(glob.glob(save_path + "/" + save_file_name + "*"))
                    f.write("\n")
                    f.write(str(current_num))
            # Counter number of request, sleep few seconds every few requests.
            count += 1
            if count % sleep_interval == 0:
                time.sleep(3)
        with open(except_temp_file, "w") as f:
            f.write(save_file_name)
            current_num = len(glob.glob(save_path + "/" + save_file_name + "*"))
            f.write("\n")
            f.write(str(current_num))

        start_level = last_level_index + 1

    for i in lv_names[start_level:end_level]:
        query_sample = i[-1]
        save_file_name = "_".join(i)
        target_images = google_target_images(query_sample)
        logging.warning(len(target_images))
        temp_end_image = min(max_end_image, len(target_images))
        for image_url, image_format in target_images[start_image:temp_end_image]:
            try:
                google_download_target_images(image_url, image_format, save_file_name, save_path=save_path)
            except:
                with open(except_temp_file, "w") as f:
                    f.write(save_file_name)
                    current_num = len(glob.glob(save_path + "/" + save_file_name + "*"))
                    f.write("\n")
                    f.write(str(current_num))
            # Counter number of request, sleep few seconds every few requests.
            count += 1
            if count % sleep_interval == 0:
                time.sleep(3)
        with open(except_temp_file, "w") as f:
            f.write(save_file_name)
            current_num = len(glob.glob(save_path + "/" + save_file_name + "*"))
            f.write("\n")
            f.write(str(current_num))


def ops_func():
    sh_names = categories_service.parse_cls_cats(SH_GARBAGE_CLS_CAT)
    gz_names = categories_service.parse_cls_cats(GZ_GARBAGE_CLS_CAT)

    _gz_lv = [t[:-1] for t in gz_names if t[-1] == 'SMLP']
    _sh_lv = [t[:-1] for t in sh_names if t[-1] == 'SMLP']

    for pattern, ops_lv in [("gz", _gz_lv), ("sh", _sh_lv)]:
        save_path = "./"+pattern+"/temp"
        except_temp_file = os.path.join(save_path, "./temp_state.ind")
        
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        if os.path.exists(except_temp_file):
            with open(except_temp_file, "r") as f:
                lasttime_save_file_name = f.readline()
                lasttime_download_num = f.readline()
            if lasttime_save_file_name:
                last_level = lasttime_save_file_name.replace("\n", "").split("_")
                last_level_index = ops_lv.index(last_level)

        start_level = 0
        end_level = len(ops_lv) + 1

        start_image = 0
        max_end_image = 60
        if last_level_index:
            if int(lasttime_download_num) < 59:
                _proceed_download(ops_lv[last_level_index], lasttime_download_num, max_end_image, except_temp_file, save_path)
                start_level = last_level_index + 1
            else:
                start_level = last_level_index + 1

        for lv in ops_lv[start_level: end_level]:
            _proceed_download(lv, start_image, max_end_image, except_temp_file, save_path)



if __name__ == "__main__":
    # ops()
    pass