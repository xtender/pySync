begin
   for r in (select case when sysdate > next_time +interval '{interval}' minute then 1 else 0 end flag
             from v$archived_log 
             where dest_id=1
             order by first_time desc
             fetch first 1 rows only
            ) 
   loop
      if r.flag=1 then
         execute immediate 'alter system archive log current';
      end if;
   end loop;
end;
