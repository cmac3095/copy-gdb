#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import os, traceback
import sys
import arcpy
import arcpy.mapping as mapping
import errno

def deleteanything(src):
    try:
        if (os.path.isdir(src)):
            shutil.rmtree(src)
        elif (os.path.isfile(src)):
            os.remove(src)
    except:
        arcpy.AddMessage("Error removing " + src)
        
def make_sure_dir_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

inWks = arcpy.GetParameterAsText(0)   #e.g. r"C:\Data\MyGDBs\Napperville_QC.sde"
outWks = arcpy.GetParameterAsText(1)   #can be empty or fullpath to a FILE Geodatabase
outWksName = ""

if (inWks is None or len(inWks) == 0):
    arcpy.AddError("Provide the full path to the input workspace (or sde connection file)")
    sys.exit(0)
    
if not arcpy.Exists(inWks):
    arcpy.AddError("Workspace " + inWks + " does not exist")
    sys.exit(0)
    
if (outWks is None or len(outWks) == 0):
    outWksPath = os.path.dirname(inWks)
    outWksName, outExt = os.path.splitext(os.path.basename(inWks))
    outWksName += ".gdb"
else:
    outWksPath = os.path.dirname(outWks)
    outWksName, outExt = os.path.splitext(os.path.basename(outWks))
    outWksName += ".gdb"  #make sure it is a File GDB extension
    
#delete the output
deleteanything(os.path.join(outWksPath,outWksName))
    
#now we are ready to do the actual work...

arcpy.env.workspace = inWks   #input
outGDB = os.path.join(outWksPath,outWksName)
                      
make_sure_dir_exists(outWksPath)
if not arcpy.Exists(outGDB):
    arcpy.AddMessage("Creating workspace " + outGDB)
    arcpy.CreateFileGDB_management(outWksPath,os.path.splitext(outWksName)[0],"CURRENT")

lds = arcpy.ListDatasets()
#create the datasets
for ds in lds:
    dsName = ds.split(".")[-1]
    
    print "Creating dataset {0}".format(dsName)
    if not arcpy.Exists(os.path.join(outGDB,dsName)):
        arcpy.Copy_management(ds, os.path.join(outGDB,dsName))
    else:
        print "Skipping feature dataset {0}. Already exists".format(dsName)
                          
#copy the feature classes
print "::::::::::::::::::::::::::::::::"
print "Copying feature classes in datasets"

for ds in lds:
    lfc = arcpy.ListFeatureClasses(feature_dataset=ds)
    dsName = ds.split(".")[-1]
    for fc in lfc:
        fcName = os.path.join(dsName,fc.split(".")[-1])
        print "Creating feature class {0}".format(fcName)
        if not arcpy.Exists(os.path.join(outGDB,fcName)):
            arcpy.Copy_management(fc, os.path.join(outGDB,fcName))
        else:
            print "Skipping feature class {0}. Already exists".format(fcName)
        
print "::::::::::::::::::::::::::::::::"
print "Copying standalone feature classes..."
lfc = arcpy.ListFeatureClasses()

for fc in lfc:
    fcName = fc.split(".")[-1]
    print "Creating feature class {0}".format(fcName) 
    if not arcpy.Exists(os.path.join(outGDB,fcName)):
        arcpy.Copy_management(fc, os.path.join(outGDB,fcName))
    else:
        print "Skipping feature class {0}. Already exists".format(fcName)
            
print "::::::::::::::::::::::::::::::::"
print "Copying tables..."
ldt = arcpy.ListTables()
for t in ldt:
    tName = t.split(".")[-1]
    print "Creating table {0}".format(tName)
    #skip "GDB_" tables as they are special, Copy_management will error
    if (tName.lower().startswith("gdb_")):
        #this is a system table
        print "Skipping table {0}. GDB system table".format(tName)
        arcpy.AddMessage("Skipping table " + tName + ". GDB system table")
        
    elif (not arcpy.Exists(os.path.join(outGDB,tName))):
        try:
            arcpy.Copy_management(t, os.path.join(outGDB,tName))
        except:
            print "Error copying {}".format(t)
            arcpy.AddError("Error copying " + t)
    else:
        print "Skipping table {0}. Already exists".format(tName)
        
print " "
print "Done"
arcpy.AddMessage("Done")
