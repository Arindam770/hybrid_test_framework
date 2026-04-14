import csv


class CSV_Helper:

    def __init__(self, path):
        self.path = path

    def read_csv(self):

        all_csv_details = []
        with open(self.path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # is_empty = True
                # for cell in row.values():
                #     if cell and cell.strip():
                #         is_empty = False
                #         break
                # if is_empty:
                #     continue
                all_csv_details.append(row)
        #print(all_csv_details)
        return all_csv_details
    
    def write_csv(self, data):
        header = data[0].keys()
        with open(self.path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()

            for row in data:
                writer.writerow(row)

if __name__ == "__main__":
    csv_obj = CSV_Helper("sample_file\\DummyData.csv")
    data = csv_obj.read_csv()
    csv_obj.write_csv(data)