import re
import requests
import os
import sys
import base64
import hashlib

SECRET_PASSWORD = "unlimitedyg22"


def line():
    try:
        cols = os.get_terminal_size()[0]
    except Exception:
        cols = 50
    print(cols * "-")


def show_banner():
    os.system('clear')
    print("\033[1;36m")
    print(" ██╗  ██╗███████╗████████╗ █████╗ ██████╗ ")
    print(" ██║ ██╔╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗")
    print(" █████╔╝ ███████╗   ██║   ███████║██████╔╝")
    print(" ██╔═██╗ ╚════██║   ██║   ██╔══██║██╔══██╗")
    print(" ██║  ██╗███████║   ██║   ██║  ██║██║  ██║")
    print(" ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝")
    print("\033[1;33m" + "=" * 50)
    print("\033[1;32m  ✦  Unlimited Tool v2  ✦")
    print("\033[1;36m  👑  Owner: @K_star3")
    print("\033[1;33m" + "=" * 50)


def decode_voucher(encoded_hash):
    try:
        key = hashlib.sha256(SECRET_PASSWORD.encode('utf-8')).digest()
        key_len = len(key)
        cipher_bytes = base64.b64decode(encoded_hash)
        data_bytes = bytearray()
        for i, byte in enumerate(cipher_bytes):
            data_bytes.append(byte ^ key[i % key_len])
        return data_bytes.decode('utf-8')
    except Exception as e:
        print("\033[1;31mError decoding voucher: " + str(e))
        sys.exit(1)


def select_plan():
    line()
    print("\033[1;33mSelect Internet Plan:")
    print("\033[1;32m  [1] Unlimited   \033[0m(expireTime: Unlimit)")
    print("\033[1;36m  [2] 1 Month     \033[0m(expireTime: 1mon)")
    print("\033[1;35m  [3] 1 Day       \033[0m(expireTime: 1day)")
    line()
    while True:
        choice = input("\033[1;00mEnter choice [1/2/3]: \033[1;32m").strip()
        if choice == '1':
            print("\033[1;32m✔ Plan: Unlimited selected")
            return 'unlimited'
        elif choice == '2':
            print("\033[1;36m✔ Plan: 1 Month selected")
            return '1mon'
        elif choice == '3':
            print("\033[1;35m✔ Plan: 1 Day selected")
            return '1day'
        else:
            print("\033[1;31m✘ Invalid choice. Enter 1, 2, or 3.")


def show_status_box(code_label, plan):
    if plan == 'unlimited':
        plan_name = 'VIP'
        expire_text = 'Unlimit'
        color = '\033[1;32m'
    elif plan == '1mon':
        plan_name = '1mon'
        expire_text = '1mon'
        color = '\033[1;36m'
    else:
        plan_name = '1day'
        expire_text = '1day'
        color = '\033[1;35m'

    line()
    print(color + "  " + code_label)
    print(color + "  \u25cf Normal")
    print()
    print(color + "  Internet Plan: " + plan_name)
    print(color + "  expireTime: " + expire_text)
    line()


def get_session_id(session_url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'referer': session_url,
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgemini.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTllMGRkYmQ5ZjIxNTItMGRmOTQxZjJlZmM2YjA4LTRjNjU3YjU4LTEzMjcxMDQtMTllMGRkYmQ5ZjNhNjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%7D'
    }
    try:
        response = requests.get(session_url, headers=headers)
        session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response.url).group(1)
        return session_id
    except requests.exceptions.ConnectionError:
        print("\033[1;31mConnection error. Check your internet.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("\033[1;31mRequest timed out.")
        sys.exit(1)
    except AttributeError:
        print("\033[1;31mFailed to extract session ID.")
        line()
        print("\033[1;33mResponse: " + response.text)
        sys.exit(1)


def login_voucher(session_id, voucher):
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 2
    }
    post_url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": "https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId=" + session_id,
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 Chrome/139.0.0.0 Mobile Safari/537.36",
    }
    try:
        with requests.post(post_url, json=data, headers=headers) as response:
            response_text = response.text
            if "Authentication failed" in response_text or "expired" in response_text or "Expired" in response_text:
                print("\033[1;33mVoucher code incorrect or expired")
                sys.exit(1)
            else:
                return re.search('token=(.*?)&', response_text).group(1)
    except AttributeError:
        print("\033[1;31mFailed to retrieve token.")
        line()
        print("\033[1;33mResponse: " + response_text)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("\033[1;31mConnection error.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("\033[1;31mRequest timed out.")
        sys.exit(1)


def one_click(token):
    headers = {
        'authority': 'portal-as.ruijienetworks.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,my;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://portal-as.ruijienetworks.com',
        'referer': 'https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId=7182e9a18cd04a1eb47868d3f7b69b44',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {'lang': 'en_US'}
    json_data = {'phoneNumber': '', 'sessionId': token}
    try:
        response = requests.post(
            'https://portal-as.ruijienetworks.com/api/auth/direct/',
            params=params, headers=headers, json=json_data,
        )
        return re.search('token=(.*?)&', response.text).group(1)
    except AttributeError:
        return None
    except requests.exceptions.ConnectionError:
        print("\033[1;31mConnection error.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("\033[1;31mRequest timed out.")
        sys.exit(1)


def do_auth(ip, token):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,my;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {'token': token, 'phoneNumber': ''}
    response = requests.get(
        'http://' + ip + ':2060/wifidog/auth',
        params=params, headers=headers
    ).url
    return response


def auth_unlimited(voucher, ip, session_url, encoded_voucher):
    for i in range(3):
        session_id = get_session_id(session_url)
        print("\033[1;32mFinal Inactive Session Id: " + session_id)
        line()
        token = login_voucher(session_id, voucher)
        if token:
            print("\033[1;00mFinal Active Session Id:\033[1;32m " + token)
            line()
            token = one_click(token)
            if token:
                do_auth(ip, token)
                show_status_box(encoded_voucher, 'unlimited')
                break
            else:
                print("\033[1;31mAttempt " + str(i + 1) + " failed")
                line()
        else:
            print("\033[1;31mFailed to Authenticate.")


def run(voucher, ip, token, session_url, plan, encoded_voucher):
    try:
        response = do_auth(ip, token)
        if "success" in response or 'www.baidu.com' in response or "www.ruijie.com/en-global" in response:
            print("\033[1;32m✔ Successfully Authenticated")
            line()
            if plan == 'unlimited':
                auth_unlimited(voucher, ip, session_url, encoded_voucher)
            else:
                show_status_box(encoded_voucher, plan)
        else:
            print("\033[1;31mFailed to Authenticate: " + response)
    except Exception as e:
        print("\033[1;31mAuth error: " + str(e))


def show_footer():
    line()
    print("\033[1;35m  📢  Tg  : https://t.me/King_Master_K")
    print("\033[1;36m  👑  Owner: @K_star3")
    print("\033[1;33m" + "=" * 50 + "\033[0m")


def main():
    show_banner()
    print("\033[1;36m--- Unlimited Tool v2 (Encoded Input) ---")

    # Step 1: Plan ရွေး
    plan = select_plan()
    line()

    # Step 2: Voucher
    encoded_voucher = input("\033[1;00mEnter Encoded Voucher Hash:\033[1;32m ").strip()
    if not encoded_voucher:
        print("\033[1;31mEncoded hash cannot be empty!")
        show_footer()
        return

    voucher = decode_voucher(encoded_voucher)
    print("\033[1;32m✔ Voucher decoded successfully")
    line()

    # Step 3: Session URL
    print("\033[1;33mThe Mac Address from Session URL must match the Connected WiFi Mac.")
    session_url = input("\033[1;00mEnter Session Url: \033[1;34m").strip()
    line()

    # Step 4: Gateway IP
    ip = input("\033[1;00mEnter Your WiFi Gateway: \033[1;34m").strip()
    line()

    if not session_url or not ip:
        print("\033[1;31mSession URL and IP are required.")
        show_footer()
        return

    session_id = get_session_id(session_url)
    token = login_voucher(session_id, voucher)

    if token:
        run(voucher, ip, token, session_url, plan, encoded_voucher)
    else:
        print("\033[1;31mFailed to retrieve initial token.")

    show_footer()


if __name__ == "__main__":
    main()
