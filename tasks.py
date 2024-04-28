from robocorp.tasks import task
from main.browser import BrowserOpen
from main.excel_reader import Excel

@task
def run_files():
    BrowserOpen.open_browser()
    Excel.read_excel()
    BrowserOpen.search_bar()
