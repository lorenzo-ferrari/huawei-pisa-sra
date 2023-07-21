# Smart Resources Allocator

## Task
Given a limited set of resources assign them to users in such a way that a resource is assigned to at most a user at a time.

## Implementation
* the resources are loaded in a sqlite database from a csv file
* to prevent different users from modifying the same file at the same time, every operation is encapsulated in a connection to the database
* log every operation in a ```log.txt``` file
* to change the locations of the output files, edit ```src/constants.py```

## Simulation
The file ```input/requests.csv``` contains a scenario of ~40 requests which can be used to run a simulation
* ```cd src/```
* ```./clean.sh && ./init.sh```
* ```python3 simulation.py```

## Ideas hypothetical further development
* implement a priority system
    * for example, assign low priority to automated task and high to people
* assign each node a set of label and let the user refer to them
* consider some cost assigned to each node and find the minimal cost assignment
    * an example of cost function might be the use-history of each node
* the current implementation (and especially the queueing system) is limited by the fact that there isn't a server running in the background
