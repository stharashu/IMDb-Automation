from main.browser import BrowserOpen
from main.excel_reader import Excel
from main.connect_database import Database


class Process:
    def __init__(self) -> None:
        pass
        
    
    def before_run_process():
        BrowserOpen().open_browser()
        Database().create_table()
    
    
    def run_process():
        Excel.read_excel()
        BrowserOpen.search_bar()
    
    def after_run_process():
        BrowserOpen.close_browser()
        
        
        
