import os, arcpy, csv, time
from os import listdir
from os.path import join, isfile, isdir, basename, splitext
from arcpy import env
from shutil import rmtree

                                                               
### Options / Paths ############################################################

# URGENT: These options / paths should be changed to suit the project at hand

# The full project folder                 
BASE_PATH = r''

# A temporary folder for files as needed
TEMP_DIR = ''          

# Location of the source shp files
out_dir = r''

# Location of a .csv file containing the output information
CSV_FILE = r''

# Location of a projection file for coordinate remapping
PROJECTION_FILE = ''

# A shape file containing the area of interest (AOI)
SHAPE_FILE = ''



# Toggle these booleans to turn column checking on/off

# Concentration checks
CHECK_CT = True
CHECK_CA = True
CHECK_CB = True
CHECK_CC = True

# Form of ice checks
CHECK_FA = True
CHECK_FB = True
CHECK_FC = True

# Stage of development checks
CHECK_SA = True
CHECK_SB = True
CHECK_SC = True

### Function definitions #######################################################

logfile = open(join(BASE_PATH, 'logfile.txt'), 'a')

def list_folder(out_dir):
    # List all files in a folder
    # parameters
    filename = [f for f in listdir(out_dir) if f.endswith('.shp')]

    return filename


def is_float(s):
    # Returns "True" if the STRING s is a float (error handling helper function)

    # parameters
    # s: a string to test if a float can be parsed without a value error
    try:
        float(s)
        return True
    except ValueError:
        return False

def spatial_avg(area, x):
    return area * x

def LOG(msg):
    logfile.write(msg+'\n')



################################################################################

# Set the path that arcpy is using
env.workspace = BASE_PATH

# a copy of the SpatialReference for this current projection file
sr = arcpy.SpatialReference(join(BASE_PATH, PROJECTION_FILE))

# a polygon for CLIPPING (binary intersection) using the currecnt ShapeFile
clip_feature = join(BASE_PATH, SHAPE_FILE)

# tolerance for the min distance for points to be equal, left balnk to use
# the map's default settings
tolerance = ""

# Creates a list of all the shapefiles
filename = list_folder(out_dir)

# Creates a spreadsheet in .csv format in which the data will be saved in
with open(join(BASE_PATH, CSV_FILE), 'a') as csvfile:

    # Creates a CSVWriter
    output = csv.writer(csvfile, delimiter=' ')

    # Writes the column headers of the .csv file
    output.writerow(['Year', 'Month', 'Day', 'CT', 'CA', 'CB', 'CC', 'FA', 'FB', 'FC', 'SA', 'SB', 'SC'])

    # for all the source .e00 files
    for shapefile in filename:

        # Reprojects the chart to the standard projection
        arcpy.DefineProjection_management(join(out_dir, shapefile), sr)

        # 5 SECOND DELAY
        # This is one of the only ways around ARC not crashing when
        # processing and also seems to be a stanard way to avoid such
        # issues. Normally awful things should never be in a loop.
        time.sleep(5)

        # Creates a new attribute to compute the area of the polygons
        arcpy.AddField_management(join(out_dir, shapefile), "AREA2", "Double")

        # Same for the perimeter
        arcpy.AddField_management(join(out_dir, shapefile), "PERIMETER2", "Double")

        # Use the resulting shape from clipping
        clip_result = join(TEMP_DIR, '.'.join([shapefile]))
        arcpy.Clip_analysis(join(out_dir, shapefile),
                            clip_feature, clip_result, tolerance)

        # Calculates the new area based on the new projection
        arcpy.CalculateField_management(clip_result, "AREA2", "!SHAPE.AREA@squaremeters!", "PYTHON_9.3")

        # Same for the perimeter
        arcpy.CalculateField_management(clip_result, "PERIMETER2", "!SHAPE.LENGTH@meters!", "PYTHON_9.3")

        # Initialize the ice concentration variable
        concentration = {'CT' : 0.0, 'CA' : 0.0, 'CB' : 0.0, 'CC' : 0.0}

        # Create a tally table for categorical info containing
        # form of ice type
        form_frequency = []
        for i in range(3):
            form_frequency.append([0]*11)
        

        sum_of_weights = 0

        area_shapefile = 0.0

        #Creates the object that reads all the polygons in the clipped AOI
        rows = arcpy.UpdateCursor(join(TEMP_DIR, '.'.join([shapefile])))

        # Create a symbol based tally chart for the stage of development
        stage_of_dev = [{},{},{}]
        

        # Loops on all the polygons of the AOI
        for row in rows:

                sum_of_weights += row.AREA2
                area_shapefile += float(row.AREA2)

                if is_float(row.CT) and CHECK_CT:
                    # if the data exist at this column...
                    # use a spatially weighted average to calculate
                    concentration['CT'] += spatial_avg(float(row.AREA2), round(float(row.CT)))

                if is_float(row.CA) and CHECK_CA:
                    # Same as CT
                    concentration['CA'] += spatial_avg(float(row.AREA2), round(float(row.CA)))

                if is_float(row.CB) and CHECK_CB:
                    # Same as CT
                    concentration['CB'] += spatial_avg(float(row.AREA2), round(float(row.CB)))

               	if is_float(row.CC) and CHECK_CC:
                    # Same as CT
                    concentration['CC'] += spatial_avg(float(row.AREA2), round(is_float(row.CC)))

                    # if the data exist at this column
                    # tally the data for the given value
                if str(row.FA) != " " and CHECK_FA:
                    if int(row.FA) < 10:
                        form_frequency[0][int(row.FA)] += 1
                    else:
                        form_frequency[0][10] += 1 

                if str(row.FB) != " " and CHECK_FB:
                    if int(row.FB) < 10:
                        form_frequency[1][int(row.FB)] += 1
                    else:
                        form_frequency[1][10] += 1

                if str(row.FC) != " " and CHECK_FC:
                    if int(row.FC) < 10:
                        form_frequency[2][int(row.FC)] += 1
                    else:
                        form_frequency[2][10] += 1 

                if str(row.SA) != " " and CHECK_SA:
                    # if the data exists at this column
                    # tally the data for the given value
                    # the value from E_SA is expected to be a string
                    
                    if str(row.SA) in stage_of_dev[0].keys():
                        stage_of_dev[0][str(row.SA)] += 1
                    else:
                        stage_of_dev[0][str(row.SA)] = 1
 
                if str(row.SB) != " " and CHECK_SB:
                    # Same as SA
                    if str(row.SB) in stage_of_dev[1].keys():
                        stage_of_dev[1][str(row.SB)] += 1
                    else:
                        stage_of_dev[1][str(row.SB)] = 1

                if str(row.SC) != " " and CHECK_SC:
                    # Same as SA
                    if str(row.SC) in stage_of_dev[2].keys():
                        stage_of_dev[2][str(row.SC)] += 1
                    else:
                        stage_of_dev[2][str(row.SC)] = 1

                
        # TODO: Test for bugs in ARC GIS
        # Divide Total_Conc_Area/area_shapefile
        if area_shapefile > 0:
            for key,value in concentration.items():
                concentration[key] = value / area_shapefile
        else:
            for key,value in concentration.items():
                concentration[key] = -1

        # Get the mode of the categorical column containing form of ice type
        for i in range(3):
            max_of_form = max(form_frequency[i])
            form_frequency[i] = form_frequency[i].index(max_of_form)
        
        
        # Get the mode of the categorical column containing the symbol for
        # stage of development

        LOG("S* PRE MAX: " + str(stage_of_dev))
        max_stages = []
        for i in range(3):
            if len(stage_of_dev[i].values()) ==0:
                max_stages.append('-1')
                continue
            max_value = max(stage_of_dev[i].values())  # maximum value
            max_keys = [k for k, v in stage_of_dev[i].items() if v == max_value]

            # Only one value gets written
            max_stages.append(max_keys[0])
        LOG("S* POST MAX: " + str(max_stages))

        # Writes the year, month, day and total ice concentration of the
        # polygon, and the form of ice type in the .csv file
        # (shapefile[0:4], shapefile[4:6], shapefile[6:8]) is the date of the chart
        output.writerow([shapefile[0:4], shapefile[4:6], shapefile[6:8],
                         concentration['CT'], concentration['CA'],
                         concentration['CB'], concentration['CC'],
                         form_frequency[0], form_frequency[1], form_frequency[2],
                         max_stages[0], max_stages[1], max_stages[2]])

