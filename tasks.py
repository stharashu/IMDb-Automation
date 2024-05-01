from robocorp.tasks import task
from main.process import Process

@task
def run_files():
    process = Process()
    process.before_run_process()
    process.run_process()
    process.after_run_process()
    