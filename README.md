Simple directory diff tool
==========================

Initially developed to compare versions of [ALOT](http://www.nexusmods.com/masseffect3/mods/363/)
(Mass Effect mod) and facilitate upgrading by reapplying only modified textures instead of everything.

Can be used either to compare two versions of a same directory (`-d`) or compare
and copy differences to a separate folder (default behavior).

Installation
------------
If you already have Python installed on your machine, you can simply grab an archive of
[the latest release](https://github.com/Skymirrh/dir-diff/releases/latest).

If you do not have Python installed, you can download a Windows executable of
[the latest release](https://github.com/Skymirrh/dir-diff/releases/latest) built using
[PyInstaller](http://www.pyinstaller.org/).

Usage
-----
Both the Python script and the Windows executable offer the same functionality.
Open a command prompt (`Windows+R` and run `cmd.exe`) and run `dir_diff.py` or `dir_diff.exe`:
a help message will provide you the syntax and optional arguments of the tool.

Example
-------
```
> dir_diff.exe Path\To\4.2 Path\To\4.3.1
Summary of changes from 4.2 to 4.3.1:
Unchanged: 2112
Modified:  1
Added:     0
Removed:   1
  
  
Copying changes (2 files) to: diff-4.2-to-4.3.1
Done copying!
  
  
I'm Commander Shepard, and this is my favorite store on the Citadel!
```
And then you will find the changes under `diff-4.2-to-4.3.1`, neatly arranged by folder :)