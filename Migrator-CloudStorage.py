from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from libcloud.storage.types import ContainerDoesNotExistError
from libcloud.storage.drivers.atmos import AtmosError
import libcloud.security
import libcloud.storage
from pprint import pprint
import string
import os
import datetime
import time
import sys
import logging
import mimetypes
mimetypes.init()
mimetypes.add_type('text/plain', '.bak', strict=True)
mimetypes.add_type('text/plain', '.php', strict=True)

# Checking that all the arguments were entered on the command line, exiting with a message if not.
if len(sys.argv) < 9:
    argumentsnotset = '\nError: one or more arguments were not passed. \n\nUsage is like so: \n\nPython Migrator-CloudStorage.py ORIGIN-PROVIDER origin-access-token.txt origin-shared-secret.txt ORIGIN-BASE-DIRECTORY DESTINATION-PROVIDER destination-access-token.txt destination-shared-secret.txt BASE-DIRECTORY datestamp=on'
    print argumentsnotset
    sys.exit(1)	


# Take command line arguments and set to variables
# 1 is ORIGIN-PROVIDER
# 2 is ORIGIN-PROVIDER access-token.txt
# 3 is ORIGIN-PROVIDER shared-secret.txt
# 4 is ORIGIN-BASE-DIRECTORY
# 5 is DESTINATION-PROVIDER
# 6 is DESTINATION-PROVIDER access-token.txt
# 7 is DESTINATION-PROVIDER shared-secret.txt
# 8 is DESTINATION-BASE-DIRECTORY
# 9 is datestamp=on or datestamp=off
# Loading ORIGIN-PROVIDER
origin_provider = sys.argv[1]
print "\n New migration starting."
print "ORIGIN-PROVIDER = ", origin_provider
# Loading ORIGIN-PROVIDER origin-access-token.txt
origin_access_token_file = open(sys.argv[2])
for line in origin_access_token_file:
    origin_access_token = line.rstrip()
origin_access_token_file.close()
print 'Origin Access Token = ', origin_access_token
# Loading ORIGIN-PROVIDER origin-shared-secret.txt
origin_shared_secret_file = open(sys.argv[3]) 
for line in origin_shared_secret_file:
    origin_shared_secret = line.rstrip()
origin_shared_secret_file.close()
print "Origin Shared Secret = ", origin_shared_secret
# Loading ORIGIN-BASE-DIRECTORY
origin_base_directory = sys.argv[4]
print "ORIGIN-BASE-DIRECTORY = ", origin_base_directory
# TODO: Here, access the base-directory and log its contents.
# Could be an adjustment of showcloudassets().
# DEPRECATED scandir = sys.argv[3]
# DEPRECATED print 'Processing string for starting directory: ' + scandir
# DEPRECATED scandir=(string.replace(scandir, "\\", "/"))
# Loading DESTINATION-PROVIDER
destination_provider = sys.argv[5]
# Loading DESTINATION-PROVIDER destination-access-token.txt
destination_access_token_file = open(sys.argv[6])
for line in destination_access_token_file:
    destination_access_token = line.rstrip()
destination_access_token_file.close()
# Loading DESTINATION-PROVIDER destination-shared-secret.txt
destination_shared_secret_file = open(sys.argv[7]) 
for line in destination_shared_secret_file:
    destination_shared_secret = line.rstrip()
destination_shared_secret_file.close()
# Loading DESTINATION-BASE-DIRECTORY
destination_base_directory = sys.argv[8]
# TODO - check it exists, log the contents.
# Could be an adjustment of showcloudassets().
# Loading date_stamp
date_stamp_toggle = sys.argv[9]
if (date_stamp_toggle == "datestamp=on"):
    rootstring="O"
    print 'Datestamping is ON'
    datestamp = datetime.date.today().strftime("%d-%B-%Y")
    container_name = (datestamp)
else:
    print 'Datestamping is OFF'
    rootstring=''
    datestamp=''
    container_name = ('')
# Set up logging file
loggydatestamp = datetime.date.today().strftime("%d-%B-%Y")
logfilename = loggydatestamp + '-Migrator-Cloud' + '.log'
print 'Logging to ' + logfilename
logging.basicConfig(filename=logfilename,filemode='w',level=logging.INFO,format='%(asctime)s %(message)s')
initialloggystring = 'New scan started.' + loggydatestamp
print initialloggystring
logging.info(initialloggystring)
errorcount = 0

# Log in to the Ninefold Cloud Storage
#def ninefoldlogin(origin_access_token, origin_shared_secret):
print '\nLogging in to Ninefold...'
print 'Origin Access Token = ', origin_access_token
print 'Origin Shared Secret = ', origin_shared_secret
print 'Logging in with our certificates...'
libcloud.security.VERIFY_SSL_CERT = False
print 'Loading our provider info...'
Ninefold = get_driver(Provider.NINEFOLD)
print 'Submitting username & password...'
driver = Ninefold(origin_access_token, origin_shared_secret)
# This plays out as driver = Ninefold('YOUR Atmos Access Token HERE', 'YOUR Atmos Shared Secret HERE')

# Show/get the list of files and folders in cloud storage
def showcloudassets():
    try:
        containers = driver.list_containers()
        print '\nList of Containers\n'
        pprint(containers)
        print '\n'
    except:
        print "*** Error occurred: ", sys.exc_info()[0] , " ***"
        print 'Exiting...'
        sys.exit(1)

# Origin Cloud scanning -- scanning all child files and directories of the origin directory
#allfiles = [] #store all files found
#alldirs = [] #store all directories found
#for root,dir,files in os.walk(scandir):	
#    if (rootstring=="O"): 
#        #Code to convert backslashes to forward slashes
#        rootstring=(string.replace(root, "\\", "/"))
#        alldirs.append(rootstring)
#        try:
#            container=driver.get_container(datestamp) #Check for the file's existence in cloud storage
#            baseloggystring = "\nBase directory already exists: " + datestamp + " -- skipping."
#            print baseloggystring
#            logging.info(baseloggystring)
#        except ContainerDoesNotExistError:
#            container=driver.create_container(datestamp)
#            baseloggystring = '\nCreating base directory in cloud storage with name: ' + loggydatestamp
#            print baseloggystring
#            logging.info(baseloggystring)
#    dirlist = [ os.path.join(root,di) for di in dir ]
#    for d in dirlist: 
#        #Code to convert backslashes to forward slashes
#        d=(string.replace(d, "\\", "/"))
#        d=(string.replace(d, " ", "_"))
#        alldirs.append(d)
#        container_name = d
#    filelist = [ os.path.join(root,fi) for fi in files ]
#    for f in filelist:
#        f=(string.replace(f, '\\', '/'))
#        allfiles.append(f)
#        object_name = f
#print "\n"


# Download the specified directory from origin-base-directory to the local disk
# download_object(obj, destination_path, overwrite_existing=False, 
file_name = "test"
local_path = "test"
container_name = "test"
object_name = "test1.txt"
destination_path = "temp/test1.txt"

print "\nPrinting a list of root-level containers..."
container_list=driver.list_containers()
pprint(container_list)

# Check for the existence of the container and file in Cloud Storage
try:
    print "Checking for the folder/container ", container_name, " in Cloud Storage..."
    container=driver.get_container(container_name) 
    print "Checking for the file ", object_name, " in Cloud Storage..."
    object=driver.get_object(container_name, object_name)
    print "Attempting to download the object ", object_name, "..."
    file=driver.download_object(object, destination_path, overwrite_existing=False, delete_on_failure=True)
    folderloggystring = "\n* Download successful for file: " + object_name + " " + datestamp
    print folderloggystring
    logging.info(folderloggystring)
except: 
    print "\n*** Unexpected error", sys.exc_info()[0] , " ***\n"
    errorcode = sys.exc_info()[0]
    errorloggystring = ('An unexpected Error ' + 'occurred on file: ' + object_name + ' in folder: ' + destination_path)
    logging.info(errorloggystring)
    logging.info(errorcode)
    errorcount = errorcount + 1

# Logging the containers and objects in cloud storage:
#print "\n Printing a list of containers under container:", container_name
#my_container_list=driver.iterate_container_objects(container)
#pprint(my_container_list)

# Local hard drive scanning -- scanning all children directories of the starting directory
def localdrivescan():
    allfiles = [] #store all files found
    alldirs = [] #store all directories found
    for root,dir,files in os.walk(scandir):	
        if (rootstring=="O"): 
            #Code to convert backslashes to forward slashes
            rootstring=(string.replace(root, "\\", "/"))
            alldirs.append(rootstring)
            try:
                container=driver.get_container(datestamp) #Check for the file's existence in cloud storage
                baseloggystring = "\nBase directory already exists: " + datestamp + " -- skipping."
                print baseloggystring
                logging.info(baseloggystring)
            except ContainerDoesNotExistError:
                container=driver.create_container(datestamp)
                baseloggystring = '\nCreating base directory in cloud storage with name: ' + loggydatestamp
                print baseloggystring
                logging.info(baseloggystring)
        dirlist = [ os.path.join(root,di) for di in dir ]
        for d in dirlist: 
            #Code to convert backslashes to forward slashes
            d=(string.replace(d, "\\", "/"))
            d=(string.replace(d, " ", "_"))
            alldirs.append(d)
            container_name = d
        filelist = [ os.path.join(root,fi) for fi in files ]
        for f in filelist:
            f=(string.replace(f, '\\', '/'))
            allfiles.append(f)
            object_name = f
    print "\n"

def showlocalassets():
    # Setting default values for file and directory iterators to allow error detection
    a = ""
    z = ""
    print ('List of local files that will be uploaded:\n\n')
    for a in allfiles:
        print "file: ", a
    if (a == ""):
        print "Warning: no files detected in the chosen path."
    for z in alldirs:
        print "directory: ", z
    if (z == ""):
        print "FATAL: Invalid directory name was detected. Did you specify a path with spaces in it?"
        sys.exit(1)
    print ('\nEnd list of local files.\n')

#showlocalassets()

#Upload folders to Ninefold Cloud Storage
def ninefoldupload():
    print "\n*** BEGIN UPLOAD PROCESS ***"
    print "\n*** CREATING DIRECTORIES IN CLOUD***\n"
    for d in alldirs:
        container_name = (datestamp + d)
        try:
            container=driver.get_container(container_name) #Check for the file's existence in cloud storage
            folderloggystring = "\n* Directory already exists (skipping):\n" + datestamp + d
            print folderloggystring
            logging.info(folderloggystring)
        except ContainerDoesNotExistError:
            folderloggystring = '\n* Creating directory in Cloud Storage: \n'+ loggydatestamp + d
            print folderloggystring
            logging.info(folderloggystring)
            container = driver.create_container(container_name=container_name)
    print "\nFinished creating directories.\n"
    #Upload files to Cloud Storage
    print "\n*** UPLOADING FILES TO CLOUD ***\n"
    for f in allfiles:
        local_path = (f)
        f=(string.replace(f, " ", "_")) # Converting spaces to underscores
        cloud_path = (datestamp + f)
        try:
            container=driver.get_container(datestamp + f) #Check for the file's existence in cloud storage
            uploadloggystring = "\n* File already exists (skipping):\n" + cloud_path
            print uploadloggystring
            logging.info(uploadloggystring)
        except ContainerDoesNotExistError:
            uploadloggystring = "\n* Uploading to Cloud Storage: " + cloud_path
            print uploadloggystring
            logging.info(uploadloggystring)
            URL = (cloud_path)
            file_name = URL.rsplit('/', 1)[1] # Split off the filename from path
            path_directory = URL.rpartition('/') # Split off the pathname from path
            container=driver.get_container(path_directory[0])
            #Adding a content-type setting
            detected_file_type = mimetypes.guess_type(local_path)
            printable_file_type = detected_file_type[0]
            if printable_file_type == None:
                printable_file_type = 'application/binary'
            extra_settings = {'content_type':printable_file_type}
            try:
                driver.upload_object(local_path,container,file_name,extra=extra_settings)
            except:
                print "\n*** Unexpected error", sys.exc_info()[0] , " ***\n"
                errorcode = sys.exc_info()[0]
                errorloggystring = ('An unexpected Error ' + 'occurred on file: ' + file_name + ' in folder' + local_path)
                logging.info(errorloggystring)
                logging.info(errorcode)
                errorcount = errorcount + 1
    endloggystring = "\n*** END UPLOAD PROCESS ***\n"
    logging.info(endloggystring)

# Main logic 
# 0 capture command line values (inline at top of file)
# 1 Log into ORIGIN-PROVIDER
##ninefoldlogin(origin_access_token, origin_shared_secret)
# 2 check Base directory exists
#showcloudassets()
# 3 Log its contents to workfile
# 4 Log into DESTINATION-PROVIDER
# 5 Compare Base and Destination directories
# 6 Create list of work to be done (directories to be created, files to be copied)

# 7 Take an item off the workfile list
# 8 Download it to temp directory on local disk
# 9 Upload it to destination cloud and verify
# 10 Make entry in workfile to mark it as done
# 11 Delete the file from local disk


print 'Process complete. ', errorcount, ' error(s) were found. \nSee the logfile: ', logfilename, ' for details.'

# Exiting and send codes to Linux prompt
# Sending correct system exit code (transmission errors) for bash detection
if (errorcount > 0): sys.exit(1)
# Sending correct system exit code (no errors) for bash detection
sys.exit(0)