# A doc for implementation of simulator
## Hierarchy of cache
Every LLM computation device(GPU) has its own local storage.  
Denote this GPU-CPU-DISK as a machine.  
And other GPU's local storage can serve as its remote storage.  
(CPU and DISK of other machines can be remote storage for this machine).  
```
   machine 0                  machine 1
-------------               -------------
|    GPU    |               |    GPU    |
-------------               -------------
      ^                           ^
      |                           |
      |                           |
      v                           v
-------------               -------------
|    CPU    |               |    CPU    |
-------------               -------------
      ^                           ^
      |                           |
      |                           |
      v                           v
-------------               -------------
|    DISK   |               |    DISK   |
-------------               -------------
```
### Implementation of hierarchy
Every machine(GPU-CPU-DISK) has its own trie.  
The elements in the trie are KV cache blocks.  
A KV cache block can tell its content(tokens) and which devices it is on(in this machine).  
## Basic Operations
### Mark if the KV cache block is on one device
llmkvb/executor/vidur/vidur/entities/kv_block_trie.py  
class KVBlockTrieNode, function set_storage_layer_info_timestamps  
#### Input
Destination, timestamps for when it is ready, bool value for mark as present or not.  
#### Output
None  
### Channel Transmission
llmkvb/executor/vidur/vidur/entities/communications.py  
class Channel, function transmit.  
Every call to transmit function launches a transmission job.  
The later jobs are blocked by previous ones until previous ones complete.  
#### Data granularity
Logically, the device space is divided into X blocks.  
(For block size bs, that unit should hold bs tokens' KV cache).  
Then inside every block, KV cache is placed layer by layer, so that they can be pipelined layer by layer.  
#### Input
token_number, current_time, num_layers  
#### Output
Three timestamps.  
Completion time, completion time for the first layer, per layer transmission time  
### Lookup in trie
llmkvb/executor/vidur/vidur/entities/kv_block_trie.py  
class KVBlockTrie, function lookup.  
#### Input
A list of tokens(divided into blocks), a timestamp.  
#### Output
A list of KV cache blocks(including its content and which devices it is on).  
## Move, Generation, Delete of KV cache
### Movements of KV cache across storage
Possible paths:  
1. Local GPU <--> Local CPU.  
2. Local CPU <--> Local Disk.  
3. Remote CPU --> Local CPU (Which is also Local CPU --> Remote CPU).  
4. Remote DISK --> Local CPU (Which is Local DISK --> Remote CPU).  
#### Local
Only possible to move between consecutive layers.  
For example, if you want to move a block from DISK to GPU, you need to fetch to CPU first, then GPU.  
#### Remote
Only possible to move across machines when is KV cache block is in CPU/DISK.  
When fetching a KV cache block from CPU/DISK of another machine, it will fetch to CPU of this machine first.  
#### Implementation
1. Make sure that it is necessary to read/write(not present before).  
2. Call transmit of Channel, and get the timestamps of completion.  
3. Call set_storage_layer_info_timestamps to mark present on some device.  

Take llmkvb/executor/vidur/vidur/entities/kvstorage.py, KVStorageController.synced_fetch_from_disk_to_memory as an example,  
it prepares the space for movements first by calling synced_acquire_space.  
Then it calls transmit on read channel from disk to CPU.  
Then it calls fetch_to_higher_location, which will call set_storage_layer_info_timestamps in the end to mark its presence in CPU layer.  

### Generation of KV cache into storage device
llmkvb/executor/vidur/vidur/entities/kv_block_trie.py  
KVStorageController  
KVStorageController.active_blocks, switch_active_fullblocks_into_cache  
#### Implementation
##### Allocate active blocks
Before computation, some blocks are allocated in GPU as active blocks(in KVStorageController._lookup_and_fetch_from_remote).  
In KVStorageController.move_to_gpu, GPU must make sure that it has space for extra active blocks and loaded(reused) blocks.  
So it will call synced_acquire_space, which might call _evict_blocks, then trigger a evict write if necessary, in the way mentioned above.  
##### Switch into KV cache
Then after computation, these blocks should be filled with KV cache of generated/prefilled tokens.  
Then call KVStorageController.switch_active_fullblocks_into_cache to insert those KV cache blocks into GPU.  
### Delete of KV cache out of storage device
llmkvb/executor/vidur/vidur/entities/kv_block_trie.py  
Class KVBlockTrie, function _evict_blocks  
In _evict_blocks, it will trigger a write to lower local storage layer if it is not present.  
_evict_blocks will always delete the block from the original device.  
#### Implementation
##### Delete from device
For delete, evict_to_lower_location and evict_to_discard can be called on the KV cache block node.  
Both of them call set_storage_layer_info_timestamps to set self as not present on that storage layer.  
##### Delete from lookup structure
evict_to_discard is called when it is already the lowest layer, and will delete itself from the lookup structure, so that it cannot be found anymore.  
## Caching Policy
### The serving system
```
Scheduling and computation
---------------     ---------------  
|  Scheduler  |     | Computation |
---------------     ---------------
KV cache operations
--------------------------------
| lookup, insert, move, delete |
--------------------------------
basic operations
----------------- ---------------- ----------
| mark position | | transmission | | lookup |
----------------- ---------------- ----------
```
### Where is caching policy
The caching policy is how KV cache operations are built upon basic operations,  
and how Scheduling and Computation interact with KV cache operations.  
#### Examples
1. An insert into KV cache can immediately launch transmission and mark present on CPU although it is in GPU first.  
This is write through from GPU to CPU.  
1. A KV cache lookup can look up only local lookup structure, or lookup all the serving instances with basic operation lookup.  
2. Computation can be pipelined layer by layer with KV cache move from CPU to GPU.  
3. Scheduler can call lookup of KV cache and check which machine has more KV cache hit, then do a locality-aware scheduling.  
### How to add/change caching policy
#### Supported ones
Just change command line arguments.  
#### New caching policy
Change the implementation of a KV cache operation, or change how Scheduler and Computation calls KV cache operations.  
### How to model serving system
Layer of storage(from 1 to 3), capacity and bandwidth can be changed by command line arguments.  
If you want to model contention(which transmission should contend with each other), should modify code on channel selection.  
For example, if you think:  
1. machine 0 read from machine 1 by network.  
2. machine 1 read from machine 0 by network.  
They should contend --> make them select the same channel on fetching from remote.  
They should not contend --> make them select two different channels on fetching from remote.  

