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

# Set the base portion of the path for Amazon, the "bucket" which will be prepended to all paths.
aws_bucket="eddawsonpersonalphotos"

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

# Log in to AWS S3 Cloud Storage
print '\nLogging in to AWS...'
print 'Destination Access Token = ', destination_access_token
print 'Destination Shared Secret = ', destination_shared_secret
print 'Logging in with our certificates...'
libcloud.security.VERIFY_SSL_CERT = False
print 'Loading our provider info...'
AWS = get_driver(Provider.S3_US_WEST_OREGON) #Can be just "S3". Check your region.
print 'Submitting username & password...'
driver2 = AWS(destination_access_token, destination_shared_secret)
# This plays out as driver = AWS('YOUR Access Key ID HERE', 'YOUR Secret Access Key HERE')

# Testing Libcloud's ability to interrogate Cloud Storage contents
print "\nShowing all root-level containers in the destination cloud..."
container_list2=driver2.list_containers()
pprint(container_list2)
for each in (container_list2):
    folderloggystring = "Folder in destination: " + each.name
    print folderloggystring
    logging.info(folderloggystring)

#Trying to detect a known directory in S3 cloud storage
known_directory = "eddawsonpersonalphotos"
try:
    container_test = driver2.get_container(known_directory)
    folderloggystring = '\nSuccessfully logged known directory in S3'
    print folderloggystring
    logging.info(folderloggystring)
except:
    errorloggystring = "*** Error occurred: ", sys.exc_info()[0] , " ***", " Something went wrong. We were unable to connect to our known directory in S3."
    print errorloggystring
    logging.info(errorloggystring)
    print 'Exiting...'
    sys.exit(1)

# Show/get the list of folders in cloud storage
def showcloudassets():
    try:
        containers = driver.list_containers()
        print '\nList of Containers\n'
        pprint(containers)
        print '\n'
    except:
        errorloggystring = "*** Error occurred: ", sys.exc_info()[0] , " ***", " Something went wrong. We were unable to show the root list of folders in S3." 
        print errorloggystring
        logging.info(errorrloggystring)
        print 'Exiting...'
        sys.exit(1)

##################################################################
#Rudimentary test to detect objects in cloud storage. Can I do it?

print "\n Showing the file contents of " + origin_base_directory
container=driver.get_container(origin_base_directory) 
object_list_origin = driver.list_container_objects(container)
pprint(object_list_origin)

'''
test_cloud_folder_origin = "/Personal Photos/Ninefold Photos/Nerf Event 6 Aug-2012"
print "\n Showing the file contents of: ", test_cloud_folder_origin
container=driver.get_container(test_cloud_folder_origin) 
object_list_origin = driver.list_container_objects(container)
pprint(object_list_origin)
'''

'''
for each in object_list_origin:
    #download to local disk
    download_target_origin = INSERT LIBCLOUD DOWNLOAD COMMAND HERE
    #verify download 
    #upload to destination
    #verify upload

destination_base_directory_with_bucket = aws_bucket + "/" + destination_base_directory
print "\n Showing the file contents of " + destination_base_directory_with_bucket
container2=driver2.get_container(destination_base_directory_with_bucket) 
object_list_destination = driver2.list_container_objects(container2)
pprint(object_list_destination)
'''

###################################################################

# Read the list of folders from local file and check they are in cloud storage
directory_list_file = open("directories.txt")
for line in directory_list_file:
    cloud_directory = line.rstrip()
    print "\nChecking folder: ", cloud_directory
    try:
        container=driver.get_container(cloud_directory)
        folderloggystring = "Folder exists in origin ", cloud_directory
        print folderloggystring
        logging.info(folderloggystring)
    except:
        errorloggystring = "*** Error occurred scanning origin folders: ", sys.exc_info()[0] , " ***"
        print errorloggystring
        logging.info(errorloggystring)
        print 'Exiting...'
        sys.exit(1)
    try:
        # Assemble correct paths for the destination cloud, and test to see if each folder is in the destination
        cloud_directory2 = aws_bucket + cloud_directory
        cloud_directory2_nospace=(string.replace(cloud_directory2, " ", "_"))
        #print "DEBUG: This is the bucket plus directory:", cloud_directory2_nospace
        container2=driver2.get_container(cloud_directory2_nospace)
        folderloggystring = "Folder exists in destination ", cloud_directory2_nospace
        print folderloggystring
        logging.info(folderloggystring)
    except:
        errorloggystring = "*** Error occurred detecting folders: ", sys.exc_info()[0] , " ***"
        print errorloggystring
        logging.info(errorloggystring)
        folderloggystring = "Folder doesn't exist in destination ", cloud_directory2_nospace
        print folderloggystring
        logging.info(folderloggystring)
        folderloggystring = "Creating folder in destination ", cloud_directory2_nospace
        print folderloggystring
        logging.info(folderloggystring)
        # If directory does not exist at destination, create it.
        container2=driver2.create_container(cloud_directory2_nospace)
    try:
        objectloggystring = "Detecting/Downloading the list of objects in the current folder from origin."
        container=driver.get_container(cloud_directory) #DEBUG: possibly redundant addition
        print objectloggystring
        logging.info(objectloggystring)
        object_list_origin = driver.list_container_objects(container)
        print "Showing files in this origin folder: ", cloud_directory
        pprint(object_list_origin)
        #Check if there were no files detected and if so, move on.
        if object_list_origin:
            print "Downloading files to local disk."
            #print "Checking if files in origin yet exist in destination."
            #check if any of them exist in the destination folder (& are not 0 bytes) and build another list of the items that are not detected at the destination
            #Download all the current folder's contents to local disk.
            for each in object_list_origin:
                temp_download_location = ("temp/" + each.name)
                print "Downloading: ", each.name, " to location: ", temp_download_location
                download_status = driver.download_object(each, temp_download_location, overwrite_existing=False, delete_on_failure=False)
                #time.sleep(1)
                if download_status: 
                    print "Download success: ", each.name
            print "Download for this folder complete! Now starting upload to destination."
            #Once download is complete, upload these items from temp to the destination
            container2=driver2.get_container(cloud_directory2_nospace) #DEBUG: possibly not required?
            for root,dir,files in os.walk("temp"):
                filelist = [ os.path.join(fi) for fi in files ]
                for f in filelist:
                    #f=(string.replace(f, 'temp\', ''))
                    #allfiles.append(f)
                    upload_object_name = f
                    print "Uploading: ", upload_object_name, " to destination cloud."
                    #fileloggystring = "Uploading file: ", upload_object_name, " to: ", cloud_directory_nospace
                    #logging.info(fileloggystring)
                    #print fileloggystring
                    uploaded_object = driver2.upload_object(temp_download_location, container2, upload_object_name, verify_hash=False, extra=None)
        else:
            print "No files in this origin folder."
    except:
        errorloggystring = "*** Error occurred downloading objects: ", sys.exc_info()[0] , " ***"
        print errorloggystring
        logging.info(errorloggystring)
        print 'Exiting...'
        sys.exit(1)
    '''try:
        #Verify that they were all uploaded and are not 0 bytes - if not, retry those
        #Continue with next directory
    except:
        errorloggystring = "*** Error occurred: ", sys.exc_info()[0] , " ***"
        print errorloggystring
        logging.info(errorloggystring)
        print 'Exiting...'
        sys.exit(1) '''
directory_list_file.close()






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


# Main logic 
# 0 capture command line values 
# 1 Log into ORIGIN-PROVIDER
# 2 check Base directory exists
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