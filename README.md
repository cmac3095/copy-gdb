copy-gdb
========

Python script to copy one ESRI GDB to a File Geodatabase. I took a sample (I think) as the starting point that had the basic copy loop in it then modified it so that I could rerun the script multiple times on the same database (in case some of the copy oerpations failed - which can happen - in that case you need to ignore feature classes that have already been copied). 

What I (ultimately) wanted was to export the content from an Enterprise GDB to a file gdb so's I could copy the content onto a USB stick (or similar).

Refer to [Copy Management](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//001700000035000000) GP Tool for more information.
