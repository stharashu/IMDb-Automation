from main.browser import BrowserOpen
from main.excel_reader import Excel
from main.connect_database import Database


class Process:
    def __init__(self) -> None:
        self.browser = None

        
    
    def before_run_process(self):
        self.browser = BrowserOpen()
        self.browser.open_browser()
        database = Database()
        database.create_table()
    
    def run_process(self):
        self.excel_file = Excel()
        self.excel_file.read_excel()
        self.browser.search_bar()
    
    def after_run_process(self):
        self.browser.close_browser()