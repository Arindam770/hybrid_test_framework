import json

class Json_Support:

    def __init__(self, path):
        self.file_path = path

    def read_Json(self):
        with open (self.file_path, "r") as file:
            json_details = json.load(file)
        #print(json_details)
        return json_details
        
    def write_json(self, data):

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    json_obj = Json_Support("sample_file\\DummyData.json")
    data = json_obj.read_Json()
    json_obj.write_json(data)