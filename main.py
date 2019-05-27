#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib

import os

import math

apnic_file_url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
file_save_name = 'delegated-apnic-latest.txt'


# 回调方法，显示进度
def show_progress(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '下载进度：%.2f%%' % per


if __name__ == '__main__':
    # 检测文件是否存在
    if os.path.exists(file_save_name):
        update_confirm = raw_input('检测数据文件已存在，是否更新？ Y/N (Default:N)\n')
        if update_confirm.lower() == 'y':
            # 下载最新数据
            urllib.urlretrieve(url=apnic_file_url, filename=file_save_name, reporthook=show_progress)
    else:
        urllib.urlretrieve(url=apnic_file_url, filename=file_save_name, reporthook=show_progress)
  

    # 读取文件内容
    record_dict_list = []
    with open(file_save_name) as saved_file:
        valid_record_num = 0
        for line in saved_file.readlines():
            line_pattern = 'apnic\|(?P<country>\w{2})\|(?P<ip_version>ipv[4,6])\|(?P<net_address>[\d.:]+)\|' \
                           '(?P<net_size>\d+)\|\d+\|(assigned|allocated)'
            match_group = re.match(line_pattern, line)
            if match_group:
                valid_record_num += 1
                record_dict_list.append(match_group.groupdict())
    print '获取到有效记录%d条' % valid_record_num

    country_to_extract = raw_input('请输入需要提取的国家： (全部: ALL)\n').upper()
    record_extracted_num = 0

    # 导出到CSV文件
    # 格式：  ipv6,CN,192.168.1.1,32
    with open('output.csv', 'w') as output_csv:
        countries = []
        for record in record_dict_list:
            countries.append(record['country'])
        if country_to_extract in countries:
            for record in record_dict_list:
                if record['country'] == country_to_extract:
                    output_csv.write(
                        record['net_address'] + '/' + str(int(math.log(int(record['net_size']), 2))) + '\n')
                    record_extracted_num += 1
        elif country_to_extract.lower() == 'all':
            for record in record_dict_list:
                output_csv.write(record['net_address'] + '/' + str(int(math.log(int(record['net_size']), 2))) + '\n')
                record_extracted_num += 1
        else:
            print '未找到此国家的记录'
            exit(-1)
    print '保存了%d条记录' % record_extracted_num
