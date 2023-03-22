#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib.request
import sys
import os
import math

apnic_file_url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
file_save_name = 'delegated-apnic-latest.txt'


# 回调方法，显示进度
def show_progress(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('下载进度：%.2f%%' % per, end='')


if __name__ == '__main__':

    ci_mode = False

    if '-ci' in sys.argv:
        ci_mode = True

    # 检测文件是否存在
    if os.path.exists(file_save_name) and not ci_mode:
        update_confirm = input('检测数据文件已存在，是否更新？ Y/N (Default:N)\n')
        if update_confirm.lower() == 'y':
            # 下载最新数据
            urllib.request.urlretrieve(
                url=apnic_file_url, filename=file_save_name, reporthook=show_progress)
    else:
        urllib.request.urlretrieve(
            url=apnic_file_url, filename=file_save_name, reporthook=show_progress)

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
    print('获取到有效记录%d条' % valid_record_num)

    if not ci_mode:
        country_to_extract = input('请输入需要提取的国家： (全部: ALL)\n').upper()
        record_extracted_num = 0

        # 导出到CSV文件
        # 格式：  ipv6,CN,192.168.1.1,32
        with open('output.csv', 'w') as output_csv:
            if country_to_extract.lower() == 'all':
                for record in record_dict_list:
                    output_csv.write(
                        record['net_address'] + '/' + str(int(math.log(int(record['net_size']), 2))) + '\n')
                    record_extracted_num += 1
            else:
                for record in record_dict_list:
                    if record['country'] == country_to_extract:
                        output_csv.write(
                            record['net_address'] + '/' + str(int(math.log(int(record['net_size']), 2))) + '\n')
                        record_extracted_num += 1
        print('保存了%d条记录' % record_extracted_num)
    else:
        try:
            os.mkdir('dist')
        except:
            pass
        for record in record_dict_list:
            with open(os.path.join('dist', f'{record["country"]}.list'), 'a+') as outptu_csv:
                outptu_csv.write(
                    record['net_address'] + '/' + str(int(math.log(int(record['net_size']), 2))) + '\n')
