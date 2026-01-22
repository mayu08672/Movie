import requests

url = "https://api.themoviedb.org/3/account/22365794/favorite"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjN2M4YTFiYTExYzk4MjM1ODczNjAyNjBlYjk5ZTUwNiIsIm5iZiI6MTc1OTgwODM3My43Nzc5OTk5LCJzdWIiOiI2OGU0OGI3NTI3ZTFjZDEyODU2MTgxM2QiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.L1lIlKJOH-YRL1zrBby86dVcn79QR1OTJUgzqOGsdno"
}

response = requests.post(url, headers=headers)

print(response.text)