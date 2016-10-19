import requests, os
from subprocess import call

# VARIABLES - Change these to match your environment
URL = 'http://10.6.16.164:4873'
SINOPIA_USER_NAME='admin'
SINOPIA_PASSWORD='password'
SCOPED_PREFIX_TO_IMPORT='@angular'
WORKING_DIRECTORY='/Users/arturoa/npm'

# Get a list of packages
response = requests.get(URL + '/-/all/', auth=(SINOPIA_USER_NAME, SINOPIA_PASSWORD))
package_names = response.json().keys()
# Filter the packages to the scoped packages
package_names =  [x for x in package_names if x.startswith(SCOPED_PREFIX_TO_IMPORT)]

# Query for the packages to get a full list of versions
for package in package_names:
    package = package.replace('/', '%2F')
    print "Working on package " + package
    # Make a directory for each package
    package_dir = WORKING_DIRECTORY + '/' + package
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)    
    # Perform the query
    response = requests.get(URL + '/' + package, auth=(SINOPIA_USER_NAME, SINOPIA_PASSWORD))
    # For each version, download the package
    json = response.json()
    if not 'versions' in json:
        print "    No versions for this package"
        continue
    versions = json['versions']
    for version, version_info in versions.iteritems():
    	print "    Working on version: " + version
        tar_path = version_info['dist']['tarball']
        response = requests.get(tar_path, auth=(SINOPIA_USER_NAME, SINOPIA_PASSWORD), stream=True)
        package_file_path = package_dir + '/' + version + '.tar.gz'
        with open(package_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)        
        # Publish the package - Assumes npm is already configured to push to the desired Artifatory location
        print "    Publishing package: " + package_file_path
        call(["npm", "publish", package_file_path])
