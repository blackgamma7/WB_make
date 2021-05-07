# WB_make
A whiteboxing python Script for Autodesk Maya made in my college years.
## how to install
create a shelf button with the python commands
~~~
import WB_Make_VA1_5 as WB_Make
WB_Make.MakeWin()
~~~
## what it does
Quickly creates a whitebox primitive to whatever real-world measurements you have, then immedately exports an FBX for level-blocking use and creates a scene file with the primitive as a template layer. It also allows this to be done en masse with a CSV (example can be found in the repo.) and the importing of orthographics.
## why the "Silly mode?"
I wanted to give the project a personality. I added a toggle if you don't.
## for the record
Maya 2016's Python Interpreter is awful for debugging. "syntax error on line 1" can mean one of the following things:
- there is an error with indentation somewhere in your code
- there is a typo somewhere in your code
- ¯\\_(ツ)_/¯ IDK,LOL.
