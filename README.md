Simple directory diff tool
==========================

Initially developed to compare versions of [ALOT](http://www.nexusmods.com/masseffect3/mods/363/)
(Mass Effect mod) and facilitate upgrading by reapplying only modified textures instead of everything.

Can be used either to compare two versions of a same directory (`-d`) or compare
and copy differences to a separate folder (default behavior).

Installation
------------
There are two versions you can download, both with the same functionality:
* Windows executable (`dir_diff.exe`) (built using [PyInstaller](http://www.pyinstaller.org/))
* Python script (`dir_diff.py`) (Python2 only, Python3 not supported)

**If you're not sure which one to choose, download `dir_diff.exe` from [the latest release](https://github.com/Skymirrh/dir-diff/releases/latest).**

If you already have Python installed on your machine, I suggest you use the script version since it is way smaller in size. Simply grab the ZIP archive of [the latest release](https://github.com/Skymirrh/dir-diff/releases/latest).

Usage
-----
##### Solution 1
* Open the directory where you stored `dir_diff.exe`
* Open a command prompt (`Shift`+`RightClick` with the mouse on empty space and `Open command window here`)
* Run `dir_diff.exe`

##### Solution 2
* Open a command prompt (`Windows+R` and run `cmd.exe`)
* Navigate to the directory where you stored `dir_diff.exe` using `cd Path\To\Download\Directory`
* Run `dir_diff.exe`
 
##### After that...
A help message will provide you the syntax and optional arguments of the tool. In the basic use case, you only need to provide the paths to the directories you want to compare, as in the example below.


Example
-------
```
> dir_diff.exe Path\To\4.2 Path\To\4.3.1
Summary of changes from 4.2 to 4.3.1:
Unchanged: 2112
Modified:  1
Added:     0
Removed:   1
  
  
Copying changes (2 files) to diff-4.2-to-4.3.1
Done copying!
  
  
I'm Commander Shepard, and this is my favorite store on the Citadel!
```
In this example, a folder `diff-4.2-to-4.3.1` is created, where you will find all the differences between the two versions, neatly arranged by folder depending on type (modified, added, or removed).
