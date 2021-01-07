select
        recid
        ,name
        ,sequence# as sequence
        ,dest_id
        ,resetlogs_change# as resetlogs_change
        ,resetlogs_time
        ,first_change# as first_change
        ,first_time
        ,next_change# as next_change
        ,next_time
        ,blocks
        ,block_size
        ,creator
        ,standby_dest
        ,archived
        ,applied
        ,deleted
        ,status
        ,completion_time
        ,backup_count
from v$archived_log
where dest_id=1
  and sequence#>:seq