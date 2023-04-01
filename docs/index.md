# How to Fabric

This is but a small side tutorial on how to use [fabric 3.0.0](https://docs.fabfile.org/) in Python 3.

As always, please read the official docs.

## Getting Started

### Pre-requisites

In order to fully understand how useful and powerful Fabric is, build a VPS (or a Linux VM) and set up a user account with credentials.

We can quickly spin one up with Vagrant ([install](https://developer.hashicorp.com/vagrant/docs/installation) Vagrant if you havn't already) on our local machine. For this tutorial, we will be using VirtualBox.

#### Get a VM

We can use any Vagrant file. We just need a dummy VM to play around. The following terminal command will initialise a `Vagrantfile` with setup and installed for a simple Postgresql DB VM.

```shell
# Init a Vagrantfile template
$ vagrant init benfante/pgbox --box-version 1.0.0

# Download and start the VM
$ vagrant up
```

Once its up, get the vagrant ssh config into a file to ssh with.

```shell
$ vagrant ssh-config > my-vagrant-ssh-config

# Contents of my-vagrant-ssh-config
$ cat my-vagrant-ssh-config

Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile C:/Users/yourusername/.vagrant.d/boxes/wagtail-VAGRANTSLASH-buster64/1.1.0/virtualbox/vagrant_private_key
  IdentitiesOnly yes
  LogLevel FATAL

```


NB: If this is done on Windows, writing the vagrant ssh-config to a file will set its encoding to UTF-16 LE or UTF-8 with BOM. If there's mingw or cygwin or equivalent on the Windows machine, run `dos2unix my-vagrant-ssh-config` to change it to UTF-8. Or copy and paste the content into a new file with the UTF-8 encoding works too.

Then test ssh with it to the VM (assuming its name is `default` as per the ssh config file)

```shell
$ ssh -F my-vagrant-ssh-config default
```

Or alternatively, set up a quick VPS on DigitalOcean. If you don't have a DigitalOcean account yet, [sign up here](https://m.do.co/c/a15586514e4a) and get $200 credit to play around with. Cheapest VPS is $4 per month.

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=a15586514e4a&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)


## Using Fabric

As usual, install fabric (at time of this writing, version 3.0.0) to your local machine. Highly recommended to set it up in a virtual environment. I personally prefer `pipenv`.


```shell
# Enter pipenv shell
$ python -m pipenv shell

# Install fabric after pipenv is installed and activated
$ pip install fabric

# Verify with `pip list`
$ pip list

# Or by test importing fabric in Python IDLE/REPL
Python 3.10.5 (tags/v3.10.5:f377153, Jun  6 2022, 16:14:13) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import fabric
>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'fabric'] # We can see 'fabric'
```

Installing fabric also provides us the `fab` cli. Typing `fab --help` in a terminal will show us what options are available to us:

```shell
$ fab --help
Usage: fab [--core-opts] task1 [--task1-opts] ... taskN [--taskN-opts]

Core options:

  --complete                         Print tab-completion candidates for given parse remainder.
  --hide=STRING                      Set default value of run()'s 'hide' kwarg.
  --no-dedupe                        Disable task deduplication.
  --print-completion-script=STRING   Print the tab-completion script for your preferred shell (bash|zsh|fish).
  --prompt-for-login-password        Request an upfront SSH-auth password prompt.
  --prompt-for-passphrase            Request an upfront SSH key passphrase prompt.
  --prompt-for-sudo-password         Prompt user at start of session for the sudo.password config value.
  --write-pyc                        Enable creation of .pyc files.
  -c STRING, --collection=STRING     Specify collection name to load.
  -d, --debug                        Enable debug output.
  -D INT, --list-depth=INT           When listing tasks, only show the first INT levels.
  -e, --echo                         Echo executed commands before running.
  -f STRING, --config=STRING         Runtime configuration file to use.
  -F STRING, --list-format=STRING    Change the display format used when listing tasks. Should be one of: flat (default), nested, json.
  -h [STRING], --help[=STRING]       Show core or per-task help and exit.
  -H STRING, --hosts=STRING          Comma-separated host name(s) to execute tasks against.
  -i, --identity                     Path to runtime SSH identity (key) file. May be given multiple times.
  -l [STRING], --list[=STRING]       List available tasks, optionally limited to a namespace.
  -p, --pty                          Use a pty when executing shell commands.
  -r STRING, --search-root=STRING    Change root directory used for finding task modules.
  -R, --dry                          Echo commands instead of running.
  -S STRING, --ssh-config=STRING     Path to runtime SSH config file.
  -t INT, --connect-timeout=INT      Specifies default connection timeout, in seconds.
  -T INT, --command-timeout=INT      Specify a global command execution timeout, in seconds.
  -V, --version                      Show version and exit.
  -w, --warn-only                    Warn, instead of failing, when shell commands fail.
```


### The fabfile

Fabric works by storing the logic and tasks in a specific file, aptly named, `fabfile.py`. A quick simple example of setting up a task in `fabfile.py`:

```python
from fabric import task

@task
def getuname(context):
    "Get server's uname"
    context.run('uname -a')
```

The above script creates a very simple task of running `uname -a` in the server. The `fab` cli will pick this up as one of the available task in a list.

```shell
$ fab --list

Available tasks:

  getuname   Get server's uname
```

If we are doing this via the Vagrant route, we can run this task and supply the saved ssh-config to it like so:

```shell
$ fab -H default -S my-vagrant-ssh-config getuname

Linux buster 4.19.0-8-amd64 #1 SMP Debian 4.19.98-1 (2020-01-26) x86_64 GNU/Linux
```

Likewise if we did it with an actual VPS, we have to supply our ssh config to it. By default, `fab` will use our actual `~/.ssh/config` if it exists and matches on the host name. Assuming that the VPS is tied to a username and is authenticated with a private key and these details are already in the ssh config, then the following command will work.

```shell
$ fab -H <VPS IP or Hostname> getuname
```

If the private key has a passphrase, add the `--prompt-for-passphrase` to the `fab` command.

```shell
$ fab -H <VPS IP or Hostname> --prompt-for-passphrase getuname
```

If no keys and uses a standard login password (albeit definitely not a recommended setup), add the `--prompt-for-login-password` to the `fab` command.

```shell
$ fab -H <VPS IP or Hostname> --prompt-for-login-password getuname
```

The option `-H` is short for `--hosts` and for each host should also be included in the ssh-config for easily identifying which needs authentication. Example:

```shell
$ fab -H app1,app2,db1,db2,git,redis,log getuname
```

The above command will execute the task `getuname` to all of those hosts from app1 to log, assuming those are valid hosts to ssh into and exists in the ssh-config file. Equivalently, we could store this in a bash or powershell script so we don't have to rerun the task to which hosts each time.

Assuming I have a file `my_custom_fab_script.ps1`, it would contain the following:
```powershell
fab -H app1 readerrorlog
fab -H db1 searchemptycolumns
```

