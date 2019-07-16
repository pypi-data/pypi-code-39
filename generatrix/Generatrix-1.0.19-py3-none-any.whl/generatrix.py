import os, sys
import argparse
import subprocess

# return output from bash pipe cmd as decoded string
def run_cmd(cmd):
	bash_cmd = cmd
	process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
	output = process.stdout.read()
	return output.decode('utf-8')


# return branches list
def get_branches():
	unwanted_branches = ['master', 'HEAD', '>']
	decoded_string = run_cmd("git branch -r --sort=committerdate")
	branches = decoded_string.split()
	clean_branch_list = []

	branch_list = [branch for branch in branches if not any(unwanted_branch in branch for unwanted_branch in unwanted_branches)]

	for branch in branch_list:
		string = branch.split("/")
		clean_branch_list.append(string[1])

	return clean_branch_list


def get_tags():
	decoded_string = run_cmd("git tag")
	tags = decoded_string.split()
	return tags


def get_git_username():
	decoded_string = run_cmd("git config user.name")
	return decoded_string.rstrip("\n\r")


def get_repo_name():
	decoded_string = run_cmd("git rev-parse --show-toplevel")
	split_string = decoded_string.split("/")
	return split_string[-1].rstrip("\n\r")


def main():
	
	parser = argparse.ArgumentParser(
		description='Generate branches or tags markdown output',
		formatter_class=argparse.RawDescriptionHelpFormatter,
    	epilog='''Example of use:
		Default usage returns all branches and tags markdown in chronological order:
		gtrix

		Optional arguments:
		gtrix -u "username"
		gtrix -t''')
	
	parser.add_argument('-u', '--user', help='set user[Optional]')
	parser.add_argument("-t", '--tags', dest='tags', action='store_true', help='get tags only')
	parser.set_defaults(tags=False)
	args = parser.parse_args()

	# check if .git directory exists
	# exit if it doesn't exists
	if ".git" not in os.listdir():
		print("Not a git directory! Ensure you are inside a git repository")
		sys.exit()

	branches = get_branches()
	tags = get_tags()
	repo = get_repo_name()

	if args.user:
		username = args.user
	else:
		username = get_git_username()
		

	# - [Board-Setup-2](https://github.com/kodaman2/TTT-Book/tree/Board-Setup-2)
	if not args.tags:
		for branch in branches:
			print("- [%s](https://github.com/%s/%s/tree/%s)\n" % (branch, username, repo, branch))

	if args.tags:
		for tag in tags:
			print("- [%s](https://github.com/%s/%s/tree/%s)\n" % (tag, username, repo, tag))


if __name__ == '__main__':
	main()