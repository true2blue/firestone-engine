import requests

url = "https://jy.xzsec.com/Search/GetDealData?validatekey=571645be-4931-4af4-b085-843b3b37e853"

payload = {'qqhs': '20',
'dwc': ''}
files=[

]
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
  'Connection': 'keep-alive',
  'Content-Length': '12',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'st_si=02728389784769; Yybdm=5407; Uid=7K%2faljTDCmSVVda6KP7wIQ%3d%3d; Khmc=%e6%9d%8e%e6%98%8e%e6%9d%b0; mobileimei=9f766f89-d811-4a3f-9453-54789a697b91; Uuid=a9624a3f72f24d0cb1e07df57fe8fc01; eastmoney_txzq_zjzh=NTQwNzYwMDgzOTE2fA%3D%3D; st_pvi=45875084067094; st_sp=2021-10-13%2023%3A06%3A26; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=2; st_psi=20241026162309492-11923323340385-2280138701; st_asi=delete',
  'Host': 'jy.xzsec.com',
  'Origin': 'https://jy.xzsec.com',
  'Referer': 'https://jy.xzsec.com/Search/Deal',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'gw_reqtimestamp': '1729942321550',
  'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

print(response.text)
