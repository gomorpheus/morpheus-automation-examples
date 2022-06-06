# Clean Morpheus Agent Repos

This is just a small Python script to cleanup old versions of the agent from a Morpheus UI node.  It needs to be run as root.

Run in a virtual environment as it needs the packaging module and python3:
```
virtualenv -p python3 venv3
source venv3/bin/activate
pip install -r requirements.txt
# to see what the script would do
python clean_repos.py
# to actually delete the extra files
python clean_repos.py doit
```

## Please use at your own risk
