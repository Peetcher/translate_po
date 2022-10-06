import requests


def translate(text_array: []):
    url = "https://translo.p.rapidapi.com/api/v3/translate"

    payload = f"from=en&to=ru&text={text_array}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "a2fac7da1amshbc3d24c632b854ep105c68jsnb03b6c0c4878",
        "X-RapidAPI-Host": "translo.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text
