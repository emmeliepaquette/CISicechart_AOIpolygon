# CISicechart_AOIpolygon

Interpreting Canadian Ice Service's (CIS) regional ice charts within a polygon delineated by the user's area of interest (AOI).

Contact: Emmelie Paquette, emmeliepaquette@cmail.carleton.ca

Versions: Python (2.7.18) and ESRI’s “arcpy” site-package within ArcGIS Desktop 10.8.1.

Project description:
This script was developped in the pursuit of Emmelie Paquette's MSc dissertation (2021) and is cited in Paquette et al. 2022 (Accepted, in review). It intends to extract and calculate ice information represented within CIS regional ice charts for specific polygons.  The script clips each weekly regional ice chart available (1983-2020) using the user's AOI polygon and calculates the mean ice concentration (i.e., weighted average within each polygon), the dominant stage of development (e.g., new ice, ...), and the dominant form of ice (e.g., small floe, ....). The dominant stage and form of ice refers to the modal class within each polygon. In 2020, CIS changed the format the charts were available in. This projects contains two scripts to handle each of the formats (see script files for more information). 

Getting started: 
The user will need to download ArcGIS Desktop 10.8.1. to excecute the code, relying on "ArcPy" to programmatically run all ArcGIS standard geoprocessing tools and provides helper functions and classes. In particular, this project relies on the Spatial Analyst module, arcpy.sa, to analyze raster and vector data with the functionality provided by the ArcGIS Spatial Analyst extension. The script calls upon local folders wherein the user stores their AOI polygon, output spatial reference, empty folder and directory of CIS charts they aim to interpret (obtained from https://www.canada.ca/en/environment-climate-change/services/ice-forecasts-observations/latest-conditions/archive-overview.html). 

How to use the project: 
The user can use this script to interpret information available with CIS's ice charts within a polygon delineated by the user. The project is highly adaptable and users can edit the script to interpret and summarize their desired CIS values. 

Credits: Script built by Benoit MonPetit (ECCC) and Emmelie Paquette (Carleton University). Used in MSc disseration supervised by Gita Ljubicic (McMaster University), Cheryl Johnson (ECCC), Derek Mueller (Carleton University) and Simon Okpakok (Independant researcher, Gjoa Haven, NU).

