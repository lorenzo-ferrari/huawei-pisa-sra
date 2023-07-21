# Smart Resources Allocator

## Task
Given a limited set of resources and users requesting access to them, assign the resources to users in such a way that a resource is assigned to at most a user at a time.

## Implementation
* the resources are loaded in a sqlite database from a csv file
* to prevent different users from modifying the same file at the same time, every operation is encapsulated in a connection to the database
* log every operation in a ```log.txt``` file
* to change the locations of the output files, edit ```src/constants.py```

## Usage
Initialize the db and the manager: ```./clean.sh && ./init.sh```

Display the database content: ```./print_db.py```

Make requests: ```./request_from_input.py```

Free a resource: ```./free_from_input.py```

## Simulation
The file ```input/requests.csv``` contains a scenario of ~40 requests which can be used to run a simulation
* ```cd src/```
* ```./clean.sh && ./init.sh```
* ```./simulation.py```

## Hypothetical further development
* implement a priority system
    * for example, assign low priority to automated task and high to people
    * it only affects the queueing system and it can be easily implemented by keeping separate queues for every priority level
* assign each node a set of label and let the user refer to them
* consider some cost assigned to each node and find the minimal cost assignment
    * an example of cost might be the use-history of each node
    * ideally, consider an explicit cost function to minimize (taking possibly everything into account: priorities, waiting times, ...)
* the current implementation (and especially the queueing system) is limited by the fact that there isn't a server running in the background

## FAQ
Q: Should I use it in a real scenario? \
A: ~~Please don't~~ The system works well enough, but it probably needs further testing and development.
