# aws_scripts
Collection of various use cases in aws using boto like sanitization of environment and scaling group actions.

Current functionalities:
1. Remove launch conf, ami and snapshots associated with it.
2. Dereigister ami and deletes all the snapshots associated with it.
3. Deletes detached volumes all at once.
4. Update a scaling group with new launch configuration with new ami created based on an a running instance.
