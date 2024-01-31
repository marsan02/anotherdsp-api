import requests

class UserManagementService:
    def __init__(self,domain,client_id,client_secret):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
    def get_token(self):
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": f"https://{self.domain}/api/v2/",
            "grant_type": "client_credentials"
        }
        response = requests.post(url, json=payload)
        resp_json = response.json()
        self.token = resp_json["access_token"]

    def create_user(self,user_data):
        url = f"https://{self.domain}/api/v2/users"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        user_data["connection"]="Username-Password-Authentication"
        response = requests.post(url, headers=headers, json=user_data)
        return response.json()

    def edit_user(self,user_id, updated_data):
        url = f"https://{self.domain}/api/v2/users/{user_id}"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        print(updated_data)
        print(url)
        response = requests.patch(url, headers=headers, json=updated_data)
        print(response.json())
        return response.json()

    def create_role(self,token, role_data):
        url = f"https://{self.domain}/api/v2/roles"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=role_data)
        return response.json()
    def get_users(self,query_params=None):
        url = f"https://{self.domain}/api/v2/users"
        if "user_id" in query_params:
            url = url + f"/{query_params['user_id']}"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        if query_params is None:
            query_params = {}
        query_params['fields'] = 'email,name,nickname,user_id'
        query_params['include_fields'] = 'true'
        response = requests.get(url, headers=headers, params=query_params)
        response = response.json()  
        if "user_id" in query_params:
            return response
        for item in response:
            item['id']=item['user_id']
        return response  
    def get_roles(self):
        url = f"https://{self.domain}/api/v2/roles"
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()  # List of roles

    def delete_user(self,user_id):
        url = f"https://{self.domain}/api/v2/users/{user_id}"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json' 
        }
        print("deleting")
        response = requests.delete(url, headers=headers)
        return response
"""
role_data = {
    "name": "Example Role",
    "description": "Role Description"
}

user_data = {
    "email": "user@example.com",
    "name": "test"
    "password": "password",
}
"""