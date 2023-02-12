from datetime import datetime
import requests
import json
class InstagramScrapping: 
    def __init__(self,database):
        self.url = 'https://www.instagram.com/data/shared_data/'
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'
        self.db = database
        
        self.session = requests.session()
        self.response = self.session.get(self.url)
        self.csrf = json.loads(self.response.text)['config']['csrf_token']
        
        self.time = int(datetime.now().timestamp())
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-CSRFToken': self.csrf,
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': '',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'TE': 'trailers',
        }
    async def check_cookie(self,**cookie):
        self.headers['Referer']=f'https://www.instagram.com/ataullah1385/'
        # self.headers['X-CSRFToken']=cookie['csrftoken']

        params = {
            'username': 'ataullah1385',
        }

        response = requests.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/',
            params=params,
            cookies=cookie,
            headers=self.headers,
        )
        try:
            data = json.loads(response.text)
            return True
        except:
            return False


    async def account(self,username,password): 
        
        self.headers['Referer']="https://www.instagram.com/accounts/login/"
        
        self.payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{self.time}:{password}',
            'optIntoOneTap': 'false',
        }

        response = requests.post(self.login_url,data=self.payload,headers=self.headers)
        data=json.loads(response.text)

        if not data['authenticated']:
            return False

        await self.db.add_instagram_account(username, password)
        cookie = response.cookies.get_dict()
        cookie['account']=username
        await self.db.add_cookie(cookie)
        return True
        
    async def following(self,username,instaID):
        cookies = await self.db.get_cookie(instaID)
        self.headers['Referer']=f'https://www.instagram.com/{username}/'
        self.headers['X-CSRFToken']=cookies['csrftoken']

        params = {
            'username': username,
        }

        response = requests.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/',
            params=params,
            cookies=cookies,
            headers=self.headers,
        )
        print('user info response :',response)
        
        data = json.loads(response.text)
        usr_id = data['data']['user']['id']
        print('user ID : ',usr_id)
        
        self.headers['Referer'] = f'https://www.instagram.com/{username}/following/'
        params_following = {
        'max_id': '100',
        }
        
        for i in range(3):
            response = requests.get(f'https://www.instagram.com/api/v1/friendships/{usr_id}/following/', 
                                    headers=self.headers, 
                                    params=params_following, 
                                    cookies=cookies)
            print('following : ',response)
            following_data = json.loads(response.text)
            for user in following_data['users']:
                user = {'userName':user['username'],'full_name':user['full_name'],'is_private':user['is_private'],'which_account':username}    
                await self.db.add_following(user)
                
    async def follower(self,username,instaID):
        cookies = await self.db.get_cookie(instaID)
        self.headers['Referer']=f'https://www.instagram.com/{username}/'
        self.headers['X-CSRFToken']=cookies['csrftoken']

        params = {
            'username': username,
        }

        response = requests.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/',
            params=params,
            cookies=cookies,
            headers=self.headers,
        )
        print('user info response :',response)
        
        data = json.loads(response.text)
        usr_id = data['data']['user']['id']
        print('user ID : ',usr_id)
        
        self.headers['Referer'] = f'https://www.instagram.com/{username}/followers/'
        params_follower = {
        'max_id': '100',
        }
        
        for i in range(3):
            response = requests.get(f'https://www.instagram.com/api/v1/friendships/{usr_id}/followers/', 
                                    headers=self.headers, 
                                    params=params_follower, 
                                    cookies=cookies)
            print('follower : ',response)
            follower_data = json.loads(response.text)
            for user in follower_data['users']:
                user = {'userName':user['username'],'full_name':user['full_name'],'is_private':user['is_private'],'which_account':username}    
                await self.db.add_follower(user)
        
        