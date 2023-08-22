# -*- coding: utf-8 -*-
# aruth: https://gist.github.com/pengzhile/f1604bffc3bc567cfeb09b68453d72d8

import json
from datetime import datetime, timedelta

import requests


def get_chatgpt_balance(sess_key, org_id, verbose=True):
    api_prefix = 'https://ai.fakeopen.com'
    headers = {
        "Authorization": "Bearer " + sess_key,
        "Content-Type": "application/json"
    }

    print('==================== 以下为账号基本信息 ====================')
    print('会话密钥: {}'.format(sess_key))
    print('组织编号: {}'.format(org_id))
    print()

    url = '{}/dashboard/billing/subscription'.format(api_prefix)
    print('==================== 以下为账号订阅信息 ====================')
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        text = json.dumps(data, sort_keys=True, indent=4)
        print('账号类型:', data['plan']['id'])
        print('是否主账号:', data['primary'])
        print('是否绑卡:', data['has_payment_method'])
        verbose and print('账号订阅信息:', text)
        print()
    else:
        print('账号订阅信息获取失败！\n')

    print('==================== 以下为账号频控信息 ====================')
    url = '{}/dashboard/rate_limits'.format(api_prefix)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        text = json.dumps(data, sort_keys=True, indent=4)
        print('GPT-4权限：{}'.format('有' if 'gpt-4' in data else '无'))
        verbose and print('账号频控信息:', text)
        print()
    else:
        print('账号频控信息获取失败！\n')

    print('==================== 以下为账号额度信息 ====================')
    url = '{}/dashboard/billing/credit_grants'.format(api_prefix)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        text = json.dumps(data, sort_keys=True, indent=4)
        print('账号额度:', data['total_granted'])
        print('已用额度:', data['total_used'])
        print('账号余额:', data['total_available'])
        for grant in data['grants']['data']:
            expires_at = datetime.fromtimestamp(grant['expires_at']) + timedelta(hours=8)  # UTC+8
            print('  额度: {}/{}，过期：{}'.format(grant['used_amount'], grant['grant_amount'], expires_at))
        verbose and print('账号额度信息:', text)
        print()
    else:
        print('账号额度信息获取失败！\n')

    print('==================== 以下为组织成员信息 ====================')
    url = '{}/v1/organizations/{}/users'.format(api_prefix, org_id)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        text = json.dumps(data, sort_keys=True, indent=4)
        print('组织成员数量:', len(data['members']['data']))
        for member in data['members']['data']:
            print('  成员: {}({})'.format(member['user']['email'], member['user']['name']))
        verbose and print('组织成员信息:', text)
        print()
    else:
        print('组织成员信息获取失败！\n')

    print('==================== 以下为账号密钥信息 ====================')
    url = '{}/dashboard/user/api_keys'.format(api_prefix)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        text = json.dumps(data, sort_keys=True, indent=4)
        print('账号密钥数量:', len(data['data']))
        for key in data['data']:
            print('  密钥: {}({})'.format(key['sensitive_id'], key['name']))
        verbose and print('账号秘钥信息:', text)
    else:
        print('账号秘钥信息获取失败！')


def run():
    username = 'aiga47m78x2n7pddf0@popemail.cyou'
    password = 'aUjugSFNy'

    data = {
        'username': input('请输入账号: '),
        'password': input('请输入密码: '),
        'prompt': 'login',
    }
    resp = requests.post('https://ai.fakeopen.com/auth/platform/login', data=data)
    if resp.status_code == 200:
        data = resp.json()
        sess_key = data['login_info']['user']['session']['sensitive_id']
        org_id = data['login_info']['user']['orgs']['data'][0]['id']

        get_chatgpt_balance(sess_key, org_id, verbose=False)
    else:
        err_str = resp.text.replace('\n', '').replace('\r', '').strip()
        print('share token failed: {}'.format(err_str))


if __name__ == '__main__':
    run()