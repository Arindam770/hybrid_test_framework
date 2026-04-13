import toml

class Toml_Support:

    def __init__(self, path):
        self.path = path

    def read_toml(self):
        with open(self.path, "r") as file:
            toml_details = toml.load(file)
        print(toml_details)
        return toml_details

    def write_toml(self, data):
        with open(self.path, "w") as file:
            toml.dump(data, file)
    

if __name__ == "__main__":
    toml_obj = Toml_Support("sample_file\\DummyData.toml")
    data = toml_obj.read_toml()
    toml_obj.write_toml(data)
