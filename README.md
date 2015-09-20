# aws_scripts
Collection of various use cases in aws using boto like sanitization of environment and scaling group actions.

## Current functionalities:
* Remove launch conf, ami and snapshots associated with it.
* Dereigister ami and deletes all the snapshots associated with it.
* Deletes detached volumes all at once.
* Update a scaling group with new launch configuration with new ami created based on an a running instance.
