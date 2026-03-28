import requests

url = "https://jy.xzsec.com/Search/GetDealData?validatekey=555e5ee0-cae8-4479-b7f3-210ea856f6a2"

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
  'Cookie': 'st_si=66907029635325; Yybdm=5407; Uid=7K%2faljTDCmSVVda6KP7wIQ%3d%3d; Khmc=%e6%9d%8e%e6%98%8e%e6%9d%b0; mobileimei=6f8a84c1-54a4-441f-b77f-9485087e4a1b; Uuid=733e0504e8a24edb81b4f6e08c3cd899; eastmoney_txzq_zjzh=NTQwNzYwMDgzOTE2fA%3D%3D; st_pvi=92498203726734; st_sp=2026-03-28%2014%3A04%3A21; st_inirUrl=https%3A%2F%2Fjy.xzsec.com%2FLogin; st_sn=2; st_psi=20260328140519744-11923323340385-7736090800; st_asi=delete',
  'Host': 'jy.xzsec.com',
  'Origin': 'https://jy.xzsec.com',
  'Referer': 'https://jy.xzsec.com/Search/Deal',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'gw_reqtimestamp': '1774680169636',
  'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

print(response.text)
