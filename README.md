# NPM Importer

## What is this?

The NPM Importer is designed to work with NPM private repositories to import packages into a new NPM repositories. It works by using existing NPM API's to gather a list of packages an versions, it then proceeds to download them and utimately publish them to the new NPM repository.


### Requirements:

* Python 2.X
  * request module for python
* NPM already set up to publish to the new NPM repository


### Running the Script:

1. Make sure to meet all the requirements
2. Change the VARIABLES in the script to match your configuration
3. If you would like to import ALL packages and not just the scoped packages that match the SCOPED_PREFIX_TO_IMPORT variable, comment out the line below the "Comment me out" comment.


