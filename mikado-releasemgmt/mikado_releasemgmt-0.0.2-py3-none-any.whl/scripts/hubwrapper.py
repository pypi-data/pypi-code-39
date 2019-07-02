"""
Simple wrapper around hub api to give access to useful bits like 
adding issue comments

Using `hub`
-----------
* simple usage
* configuring the local environment
  (export GITHUB_TOKEN=xxxx)
* using hub api

`hub api` command is a wrapper around the low-level REST based 
API that github supplies. THat REST API can do pretty much anything 
in github, so as long as we have our token setup, and know the right 
commands for the API we can do pretty much anything on the command line

My main need is a way to manage issues on the command line (because I 
don't like all that clicking).  So I shall build out some hub-wrapping 
commands to ease my path 

"""
