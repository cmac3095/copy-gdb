#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import os, traceback
import sys
import arcpy
import arcpy.mapping as mapping


arcpy.env.workspace = r"Napperville_QC.sde"
outputPath = r"C:\Data\Exports"

outGDB = os.path.join(outputPath,"Napperville_QC.gdb")
if not arcpy.Exists(outGDB):
    print "Creating workspace {0}".format(outGDB)
    arcpy.CreateFileGDB_management(outputPath,"Napperville_QC","CURRENT")

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
    if not arcpy.Exists(os.path.join(outGDB,tName)):
        try:
            arcpy.Copy_management(t, os.path.join(outGDB,tName))
        except:
            print "Error copying {}".format(t)
    else:
        print "Skipping table {0}. Already exists".format(tName)
        
print " "
print "Done"
