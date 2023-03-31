from fabric import task

@task
def getuname(context):
    "Get server's uname"
    context.run('uname -a')
