from RPA.Excel.Files import Files
from main.constants import excel_file

class Excel:
    def __init__(self) -> None:
        pass
    
    def read_excel(self):
        self.lib = Files()
        self.lib.open_workbook(excel_file)
        data = self.lib.read_worksheet_as_table(header=True)
        # for row in data:
            # print(data)
        return data

