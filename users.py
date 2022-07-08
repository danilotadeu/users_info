import requests
import csv
import sys

class MakeApiCall:
    def get_user_by_id(self, api, userId):
        url = api+"users/"+str(userId)
        response = requests.get(f"{url}")
        if response.status_code == 200:
            user = response.json()["data"]
            print(user["first_name"] + " " + user["last_name"])
        else:
            print("usuário não encontrado")

    def get_user_data(self, api, nameFile, perPage):
        page = 1
        dados = []
        while(True):
            url = api+"users?"+"page="+str(page)+"&per_page="+str(perPage)
            response = requests.get(f"{url}")
            if response.status_code == 200:
                if response.json()["data"] == []:
                    break
                else:                
                    page += 1
                    for u in response.json()["data"]:
                        dados.append({
                            "id":u["id"],
                            "email":u["email"],
                            "first_name":u["first_name"],
                            "last_name":u["last_name"],
                            "avatar":u["avatar"]
                        })
            else:
                print("Call to API failed")
        
        with open(nameFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Email", "First Name", "Last Name", "Avatar"])

            for user in dados:
                writer.writerow([user["id"]]+[user["email"]]+[user["first_name"]]+[user["last_name"]]+[user["avatar"]])

    def __init__(self, api):
        nameFile = "user.csv"
        if 0 <= 1 < len(sys.argv):
            nameFile = sys.argv[1]+".csv"

        perPage = 12
        if 0 <= 2 < len(sys.argv):
            perPage = sys.argv[2]

        userId = 0
        if 0 <= 3 < len(sys.argv):
            userId = sys.argv[3]

        if userId == 0:
            self.get_user_data(api, nameFile, perPage)
        else:
            self.get_user_by_id(api, userId)

if __name__ == "__main__":
    api_call = MakeApiCall("https://reqres.in/api/")
