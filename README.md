# huawei-pisa

## Task

## Implementation
* input resources file (csv)
* input simulation (requests) file (csv)
* priority queue
* should events have a dedicated class? probably yes
* store the events in a priority queue and process them in cronological order
    * note: in case of tie, "UNLOCK" events should preceed "LOCK" events

### How to handle request
* 

## Ideas
* linux daemon
* actual DB (done)
* priorities (low,high)
    * low priority to automated task, high to people
* labels (and nodes with different labels)
* cost assigned to each node
* use-history of each node
* queue requests
    * one queue per resource

## Other
