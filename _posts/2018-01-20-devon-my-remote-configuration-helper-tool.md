---
layout: post
title: devON - my remote configuration tool
date: 2018-01-20 15:47 +0200
categories: [Tips & Tricks]
tags: [Ruby, Configuration, SSH]
description: How I configure remote machines via SSH using devON
excerpt:  devOn is a Ruby [gem](http://guides.rubygems.org/what-is-a-gem/) that has capability to to run one or many scripts with any configuration
---
A couple of years ago (in [2015](https://www.linkedin.com/in/paulbrodner/) to be precise), I was testing a high availability system configured through multiple cluster nodes.
There was a standard architecture and infrastructure that I needed to setup prior to my performance test execution: one load balancer, 4 web server nodes configured in a cluster environment, one solr service that will communicate with these nodes, a shared [NTFS](https://en.wikipedia.org/wiki/NTFS) location for repository and one MySQL database.

As you figure it out, there were a lot of manual configuration to be made:
* each web server node had a particular configuration that was pretty hard to maintain manually (like clustering settings, database connection string, session configuration, server tuning, etc)
* the load balancer needed also a configuration
* database needed to be created, tuned for load testing or/and cleaned up
* other housekeeping tasks, like cleanup space - mainly if I wanted to re-run the tests on a new version of the [SUT](https://en.wikipedia.org/wiki/System_under_test) on the same instances.

This is how  
[![devON](/images/posts/devOn-logo.png)](https://goo.gl/znSM9n)
came to life.


## What is devON ?

`devOn` is a Ruby [gem](http://guides.rubygems.org/what-is-a-gem/) that has capability to 
to run one or many scripts with any configuration (parameters) from your host to remote machines in interactive or unattended way (via [SSH](https://en.wikipedia.org/wiki/Secure_Shell) protocol)    
![devON](/images/posts/devON-idea.png)

The scripts, configuration files and connections are all group inside generated projects.

#### How can you install it ?

* a) Inside a Gemfile:
```ruby
$ gem "devon", :git => "git://github.com/paulbrodner/devon.git"
$ bundle install
```

* b) clone [devOn](https://goo.gl/znSM9n) repository and follow instructions.

### a) Project Generation
With devOn, you can generate new projects with one command line
```ruby
$ devon -n my-awesome-project
```
You will have now all the boilerplates in place for just start creating your configuration scripts.

### b) Helper Tasks
You just need to remember the generic `rake -T` command that will show you all available helper tasks

From there, just follow the interactive shell in order to execute your scripts with any configuration.

```ruby
$ rake -T
rake configs:list                               # List available configurations
rake configs:new                                # Create a new Configuration
rake conn:list                                  # List available connections
rake db:init                                    # Initialize/Reinitialize db
rake scripts:list                               # List available scripts
rake scripts:new                                # Create a new script
rake scripts:run                                # Run script (in bash: rake scripts:run CMD=1,2,3 
rake scripts:run_all[script,connection,config]  # Run script (in bash: rake scripts:run CMD=1,2,3
rake server:up                                  # Start Sinatra Server
```

{% include idea.html content="Example: showing all available connections configured" %}
```ruby
$ rake conn:list
[
    [0] "connections/my_buddy_machine.rb {192.168.1.20}",
    [1] "connections/vagrant.rb {127.0.0.1}",
    [2] "connections/virtual_machine.rb {192.168.1.10}",
    [3] "connections/cloud_instance.rb {50.16.23.10}"
]
```

### c) Interactive Execution

```ruby
$ rake scripts:run                  #execute the scripts
[
    [0] "scripts/connect.rb"
]
Choose a file from scripts to use:
```
You are asked to choose what script you want to execute.
These are identified by their ID starting from 0 to "number-of-available-scripts"

After selecting the first one (position `0`) the scrip will show you available connections.

```ruby
"Available Connections:"
[
    [0] "connections/vagrant.rb {127.0.0.1}"
]
Choose a file from connections to use:
```

After selecting the connection you are asked for a configuration. These are the parameters used in script. You can choose `0` if you don't setup parameters for your script.
```ruby
0
"Available Configs:"
[
    [0] "No config",
    [1] "configs/simple.rb"
]
Choose a file from configs to use:
1
```
After selecting the `script`, the `connection` and the optional `config` file, the execution is started and results are logged on your terminal verbosely.

```ruby
Using shell command: echo 'from UNIX OS' && ls -la
Using config: {:hostname=>"127.0.0.1", :username=>"vagrant", :password=>"vagrant", :port=>"2222"}
I, [2018-01-20T17:23:31.033121 #45298]  INFO -- net.ssh.transport.server_version[3fcd5188a3e8]: negotiating protocol version
I, [2018-01-20T17:23:31.038328 #45298]  INFO -- net.ssh.transport.algorithms[3fcd51886180]: sending KEXINIT
I, [2018-01-20T17:23:31.038621 #45298]  INFO -- net.ssh.transport.algorithms[3fcd51886180]: got KEXINIT from server
I, [2018-01-20T17:23:31.038751 #45298]  INFO -- net.ssh.transport.algorithms[3fcd51886180]: negotiating algorithms
/Users/p3700454/.rvm/gems/ruby-2.4.1/gems/awesome_print-1.6.1/lib/awesome_print/formatter.rb:378: warning: constant ::Fixnum is deprecated
{
    :title => "Preparing SSH command",
    :value => "echo 'from UNIX OS' && ls -la"
}
I, [2018-01-20T17:23:41.078196 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: channel_open_confirmation: 0 0 0 32768
I, [2018-01-20T17:23:41.078403 #45298]  INFO -- net.ssh.connection.channel[3fcd50c65e78]: sending channel request "env"
I, [2018-01-20T17:23:41.078608 #45298]  INFO -- net.ssh.connection.channel[3fcd50c65e78]: sending channel request "exec"
I, [2018-01-20T17:23:41.079428 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: channel_window_adjust: 0 +2097152
I, [2018-01-20T17:23:41.079526 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: channel_success: 0
I, [2018-01-20T17:23:41.082034 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: channel_request: 0 exit-status false
I, [2018-01-20T17:23:41.082132 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: channel_data: 0 579b
I, [2018-01-20T17:23:41.082225 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: channel_eof: 0
I, [2018-01-20T17:23:41.082281 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: channel_close: 0
I, [2018-01-20T17:23:41.082376 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: 127.0.0.1 delete channel 0 which closed locally and remotely
{
     :title => "[SHELL OUTPUT]",
    :output => [
        [ 0] "from UNIX OS",
        [ 1] "total 36",
        [ 2] "drwxr-xr-x 4 vagrant vagrant 4096 Dec 15  2015 .",
        [ 3] "drwxr-xr-x 3 root    root    4096 Feb 21  2015 ..",
        [ 4] "-rw------- 1 vagrant vagrant   79 Jan 20 04:31 .bash_history",
        [ 5] "-rw-r--r-- 1 vagrant vagrant  220 Feb 21  2015 .bash_logout",
        [ 6] "-rw-r--r-- 1 vagrant vagrant 2273 Feb 21  2015 .bashrc",
        [ 7] "drwx------ 2 vagrant vagrant 4096 Feb 21  2015 .cache",
        [ 8] "-rw-r--r-- 1 vagrant vagrant  675 Feb 21  2015 .profile",
        [ 9] "-rw-rw-r-- 1 vagrant vagrant    0 Feb 21  2015 .selected_editor",
        [10] "drwx------ 2 vagrant vagrant 4096 Jan 18 04:54 .ssh",
        [11] "-rw------- 1 vagrant vagrant  906 Dec 15  2015 .viminfo"
    ]
}
I, [2018-01-20T17:23:41.082960 #45298]  INFO -- net.ssh.connection.session[3fcd50c69348]: closing remaining channels (0 open)
"NO ERRORS ENCOUNTERED!"
```

Our selected [script](https://github.com/paulbrodner/devon/blob/master/structure/scripts/connect.rb) is just listing the content of the machine 'ls -la` 


### d) Unnattended Execution
You can also execute the same scripts without manual intervention.
Use:
```ruby
$ rake scripts:run_all['scripts/connect.rb','connections/vagrant.rb','']
```

### e) Browser 'Execution'
You can also execute your test within your favorite browser
```ruby
$ rake db:init      #initialize database where the script execution history will be saved
```

```ruby
$ rake server:up    #starts server
```
This will start a [Sinatra](http://sinatrarb.com/) based web server available at `localhost:4567` 
![devON](/images/posts/devON-server.png)

Check available radio buttons according to your test plan, click `Execute` and watch the results.

{% include idea.html content="That is not all, there are a lot of new features added in this little configuration tool, all available in my public  <a href='https://goo.gl/znSM9n'>github</a> repository" %}


Please take a look at the [devOn](https://goo.gl/znSM9n) repository, add issues or leave pull request.

