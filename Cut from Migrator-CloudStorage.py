#Cut from Migrator-CloudStorage.py

line 249
        #print "\n Showing output of a call to the container generator "
        #iterated_object = driver.iterate_container_objects(container)
        #listed_objects = driver.list_container_objects(container)
        #pprint(listed_objects)
        #creating a list for the objects in the current directory
        #object_list_origin_current_dir = []
        #print "Trying to get values out of the generator"
        #object_list_origin_current_dir.append(iterated_object)
        # Logging the containers and objects in cloud storage:
        #print "\n Printing a list of containers under container:", container_name
        #my_container_list=driver.iterate_container_objects(container)
        #pprint(my_container_list)

line 233
    #
    # Download the specified directory from origin-base-directory to the local disk
    # download_object(obj, destination_path, overwrite_existing=False, 
    #file_name = "test"
    #local_path = "test"
    #container_name = "test"
    #object_name = "test1.txt"
    #destination_path = "temp/test1.txt"
    #

line 341
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

line 360
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

line 273
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

# Check for the existence of the container and file in Cloud Storage
#try:
#    print "Checking for the folder/container ", container_name, " in Cloud Storage..."
#    container=driver.get_container(container_name) 
#    print "Checking for the file ", object_name, " in Cloud Storage..."
#    object=driver.get_object(container_name, object_name)
#    print "Attempting to download the object ", object_name, "..."
#    file=driver.download_object(object, destination_path, overwrite_existing=False, delete_on_failure=True)
#    folderloggystring = "\n* Download successful for file: " + object_name + " " + datestamp
#    print folderloggystring
#    logging.info(folderloggystring)
#except: 
#    print "\n*** Unexpected error", sys.exc_info()[0] , " ***\n"
#    errorcode = sys.exc_info()[0]
#    errorloggystring = ('An unexpected Error ' + 'occurred on file: ' + object_name + ' in folder: ' + destination_path)
#    logging.info(errorloggystring)
#    logging.info(errorcode)
#    errorcount = errorcount + 1

# Testing Libcloud's ability to interrogate Cloud Storage contents
#print "\nShowing all root-level containers..."
#container_list=driver.list_containers()
#pprint(container_list)

#print "\n Showing the file contents of " + origin_base_directory
#object_list = driver.list_container_objects(container)
#pprint(object_list)

# Logging the containers and objects in cloud storage:
#print "\n Printing a list of containers under container:", container_name
#my_container_list=driver.iterate_container_objects(container)
#pprint(my_container_list)

line 249
                '''destination_object=driver2.get_object(cloud_directory2_nospace, each)
                if destination_object.name == "each.name":
                    print "Object: ", each.name, " already exists at destination."
            #Download only these non-existing items to the local temp directory. 
                else:'''