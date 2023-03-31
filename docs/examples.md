# Automation Examples

Here are some examples and ideas of what you can do to automate your system administration tasks.

## 1. Find Missing Data and Update in Database

Using a real world working example that I was working on, received a ticket that the system had missing data. After formulating what the SQL statement is, I could easily VPN, ssh to the DB and run that SQL script. Or, I could just VPN and run the `fab` task to search, filter, list, and update if I wanted to.

Example `fabfile.py`:

```python
from fabric import task

@task
def searchmissingdata(context):
  "Find and list missing data"
  sql = "select * from some_table where column is null;"
  psql = f"psql -d app_core -c '{sql}'"
  context.run(psql)

@task
def updateonemissingdata(context):
  "Update One Missing Data"
  row_id = input("What is the row_id to update?\n")
  new_value = input(f"What's the new value to update in {row_id}?\n")
  sql = f"update from some_table set column = '{new_value}' where row_id = {row_id};"
  psql = f"psql -d app_core -c '{sql}'"
  context.run(psql)
```

Then in `fab` command:

```shell
> fab -H db1 searchmissingdata
```

Do some cross reference with a different system (sometimes its in Excel because backups), gets the value and use that to update the missing data.

```shell
> fab -H db1 updateonemissingdata
```

And when prompted for the inputs for each row and what value to update, it handles it for us.

## 2. Find Errors in Logs

Often times, we would find odd errors not accounted for in system design or something unexpected happen in one service that the system started malfunctioning. Service checks are already in place but they can only give us an indication or alert of the malfunction but not enough to help diagnose or fix the problem faster before it gets worse. So the workflow usually goes: ssh to app server -> open different log files -> find error message -> traceback to root cause -> fix or remove problematic cause -> restart service? -> done.

So a `fabfile` might look like:

```python
from fabric import task

@task
def checkapplog(context):
  "Checks app log for ERROR"
  app_log_command = "grep ERROR /var/log/messages"
  context.sudo(app_log_command)
```

Notice that this uses `sudo` as part of the context connection. So in a `fab` cli, this should look like:

```shell
> fab -H app1 --prompt-for-sudo-password checkapplog
```
