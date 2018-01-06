# rstudio-ec2
## Overview
A set of tools to quickly set up and access rstudio server on ec2, in case you need some extra computational power for your data analytics.

Simply run
```
launch_rs
```
It will print out instructions to (1) access the rstudio server application in your browser and (2) ssh into your instance if you feel the need. You'll need to log in with username `ubuntu` and password `password`.

To save a file locally from the instance, run
```
save_rs <file-name>
```
where the `<file-name>` is relative to the instance's `~` directory.

To shut down the instance, run
```
shutdown_rs
```

## Command Line Arguments
```
launch_rs
[-s --setup-file <file-name>]
[-f --files <value>] 
[-i --instance-type <value>] (defaults to m5.large)
[-m --max-price <value>] (defaults to 0.05)
```

Here's what they mean:
> setup-file
>> A bash script to automatically run on the (ubuntu) instance after it is created.

> files
>> A comma (no space) separated list of local files to copy to the instance.

> instance-type
>> The ec2 instance type. Defaults to `m5.large`.

> max-price
>> The maximum spot price to pay. Defaults to `0.05`.



## Setup
To run these tools, your python environment will need `boto3` installed.
You'll also need to have [setup](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)
and [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) the AWS command line interface (these are quick).

Setup the project by `cd`ing into the main directory and running the following:
```
sudo sh resources/setup.sh
```
This script creates a symlink to the three tools in `/usr/local/bin/`; if uninstalling, you'll have to
```
rm /usr/local/bin/{launch_rs,save_rs,shutdown_rs}
```
