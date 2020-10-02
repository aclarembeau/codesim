# codesim

Easily find duplicated code. 

## Installation 

Run the following 
```
wget --no-cache https://raw.githubusercontent.com/aclarembeau/codesim/master/main.py -O /usr/local/bin/codesim ; chmod +x /usr/local/bin/codesim
```


## Usage 

`codesim .` : Look for similar code in the current directory
`codesim . --min-lines=40 --ratio=0.8` : Look for similar code in the current directory (using some tweaked parameters) 

## Sample output 

```
== Results ==

changes	ratio	lines a	lines b
6.00	0.92	37	37	./projects/hook_logs/_index.html.haml -> ./admin/hook_logs/_index.html.haml
6.00	0.92	37	37	./admin/hook_logs/_index.html.haml -> ./projects/hook_logs/_index.html.haml
```