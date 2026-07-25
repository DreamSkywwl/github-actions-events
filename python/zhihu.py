from toolsNetWork import safe_request

print('----------')
url = 'https://www.zhihu.com/api/v3/moments/zhihssgpr/activities?limit=5&desktop=true&ws_qiangzhisafe=0'
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-api-version": "3.0.40",
    "x-requested-with": "fetch",
    "x-zse-93": "101_3_3.0",
    "x-zse-96": "2.0_Ui0mSN0Wtahkjs=sv1OxR7H=MqiUpKgJZMSAgNWsgbpx21Z2mo1er8tP74LgjkBI",
    "cookie": "_zap=54cb4ec5-7b7d-430d-b74a-7701f9d0a9fb; d_c0=eUUUy49RdxuPThAzhlWTgNJcei_rIJURzs0=|1764643803; q_c1=3b425f990f1547e486f561ce97b4af9b|1764643803000|1764643803000; edu_user_uuid=edu-v1|a533f1cb-e4ac-4ed4-a193-c72e42486666; z_c0=2|1:0|10:1777250996|4:z_c0|92:Mi4xZ2psaEFBQUFBQUI1UlJUTGoxRjNHeVlBQUFCZ0FsVk5mSjNNYWdETGVxMzNsMkZVc0c4UmhmLWlDZUw3VlY4Um1B|f3ba5fbcbaa610a5a16ef253c22593f1d6a90d0aeef2d3b733648ac615ca57e6; __zse_ck=005_6xSLt=4X19iPUh9iLqir3Ne6CkUpSh1/2gWp2cmqY5Vyxs/IJSWGB4wNmpJMNHKaGjoXHi/UBmEFW8z=6s9nvKNYyzKlZjSKLSPC1QDbvt3Q4wxDYXvb22Jff7abnlQK-KUzXk5TUgFaPU54Hoil4E+GhFow4FgGDC9oBo++z69nBtGRY7a0jCooy3i9pVApwPg2IMRo9xuJYVZj1S1RJpUB4nPjO84u/sRJm6rG7tVD18UqrgbSwKSl5Qj0tQC5k; _xsrf=2a6268d3-37d1-4ed7-853b-9b0fabcaf945; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1778719659,1778806004,1779064563,1779155197; HMACCOUNT=C5F69ABBF3B5B997; SESSIONID=8WD3ExskGkYeh5GpxbAV3CO0AFoFRCcO1UvEaXylzvq; JOID=VlkcBUw5Nt2z0Ay6OzsQzZ0BGN0uBGmWgZZxwV99WIzZuTr4Q8nx2NvWAb018EMbub23cr03hvmYueemMe79-tw=; osd=UlkSBE09NtOy0Qi6NToRyZ0PGdwqBGeXgJJxz158XIzXuDv8Q8fw2d_WD7w09EMVuLyzcrM2h_2Yt-anNe7z-90=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1779158060; BEC=f23896b358f7577445de7dd8602ca4bf",
    "Referer": "https://www.zhihu.com/people/zhihssgpr",
    "Referrer-Policy": "no-referrer-when-downgrade"
}
reponse = safe_request(method='GET', url=url, headers=headers)
print(f"====:{reponse}")
'''fetch("https://www.zhihu.com/api/v3/moments/zhihssgpr/activities?limit=5&desktop=true&ws_qiangzhisafe=0", {
  "headers": {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-api-version": "3.0.40",
    "x-requested-with": "fetch",
    "x-zse-93": "101_3_3.0",
    "x-zse-96": "2.0_Ui0mSN0Wtahkjs=sv1OxR7H=MqiUpKgJZMSAgNWsgbpx21Z2mo1er8tP74LgjkBI",
    "cookie": "_zap=54cb4ec5-7b7d-430d-b74a-7701f9d0a9fb; d_c0=eUUUy49RdxuPThAzhlWTgNJcei_rIJURzs0=|1764643803; q_c1=3b425f990f1547e486f561ce97b4af9b|1764643803000|1764643803000; edu_user_uuid=edu-v1|a533f1cb-e4ac-4ed4-a193-c72e42486666; z_c0=2|1:0|10:1777250996|4:z_c0|92:Mi4xZ2psaEFBQUFBQUI1UlJUTGoxRjNHeVlBQUFCZ0FsVk5mSjNNYWdETGVxMzNsMkZVc0c4UmhmLWlDZUw3VlY4Um1B|f3ba5fbcbaa610a5a16ef253c22593f1d6a90d0aeef2d3b733648ac615ca57e6; __zse_ck=005_6xSLt=4X19iPUh9iLqir3Ne6CkUpSh1/2gWp2cmqY5Vyxs/IJSWGB4wNmpJMNHKaGjoXHi/UBmEFW8z=6s9nvKNYyzKlZjSKLSPC1QDbvt3Q4wxDYXvb22Jff7abnlQK-KUzXk5TUgFaPU54Hoil4E+GhFow4FgGDC9oBo++z69nBtGRY7a0jCooy3i9pVApwPg2IMRo9xuJYVZj1S1RJpUB4nPjO84u/sRJm6rG7tVD18UqrgbSwKSl5Qj0tQC5k; _xsrf=2a6268d3-37d1-4ed7-853b-9b0fabcaf945; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1778719659,1778806004,1779064563,1779155197; HMACCOUNT=C5F69ABBF3B5B997; SESSIONID=8WD3ExskGkYeh5GpxbAV3CO0AFoFRCcO1UvEaXylzvq; JOID=VlkcBUw5Nt2z0Ay6OzsQzZ0BGN0uBGmWgZZxwV99WIzZuTr4Q8nx2NvWAb018EMbub23cr03hvmYueemMe79-tw=; osd=UlkSBE09NtOy0Qi6NToRyZ0PGdwqBGeXgJJxz158XIzXuDv8Q8fw2d_WD7w09EMVuLyzcrM2h_2Yt-anNe7z-90=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1779158060; BEC=f23896b358f7577445de7dd8602ca4bf",
    "Referer": "https://www.zhihu.com/people/zhihssgpr",
    "Referrer-Policy": "no-referrer-when-downgrade"
  },
  "body": null,
  "method": "GET"
});'''


