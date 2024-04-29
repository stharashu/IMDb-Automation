from robocorp.tasks import task
from main.process import Process

@task
def run_files():
    Process.before_run_process()
    Process.run_process()
    Process.after_run_process()
    