import os, requests
from fastapi import Request, HTTPException

def token(request: Request):

    token = request.headers.get("Authorization")
    print(token)

    if not token:
        raise HTTPException(status_code= 403, detail="Not allowed")

 
    # response: str = requests.post('http://127.0.0.1:8000/validate', headers = {"Authorization": token})
    response: str = requests.get(f'http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate', headers = {"Authorization": token})

    # response: str = requests.post(f'http://http://192.168.49.2:30013/validate', headers = {"Authorization": token})


    if response.status_code == 200:
        # print('from validate')
        # print(response.text)
        return response.text, None
    else:
        return None, response.text
    # print(response)
    