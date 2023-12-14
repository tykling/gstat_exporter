# gstat_exporter
Prometheus exporter for FreeBSD gstat data.

# Blog post
https://blog.tyk.nu/blog/all-in-a-days-work-prometheus-gstat_exporter-and-grafana-dashboard/

# Grafana Dashboard
https://grafana.com/grafana/dashboards/11223

# Example Metrics
The following is an example of the metrics exported from a system with a small 500G flashdisk and two large spinning disks:

```
root@plads1:~ # fetch -qo - http://127.0.0.1:9248
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 426.0
python_gc_objects_collected_total{generation="1"} 0.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 48.0
python_gc_collections_total{generation="1"} 4.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="9",patchlevel="18",version="3.9.18"} 1.0
# HELP gstat_up The value of this Gauge is always 1 when the gstat_exporter is up
# TYPE gstat_up gauge
gstat_up 1.0
# HELP gstat_queue_depth The queue depth for this GEOM
# TYPE gstat_queue_depth gauge
gstat_queue_depth{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_queue_depth{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_queue_depth{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_total_operations_per_second The total number of operations/second for this GEOM
# TYPE gstat_total_operations_per_second gauge
gstat_total_operations_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_total_operations_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_total_operations_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_read_operations_per_second The number of read operations/second for this GEOM
# TYPE gstat_read_operations_per_second gauge
gstat_read_operations_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_read_operations_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_read_operations_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_read_size_kilobytes The size in kilobytes of read operations for this GEOM
# TYPE gstat_read_size_kilobytes gauge
gstat_read_size_kilobytes{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_read_size_kilobytes{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_read_size_kilobytes{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_read_kilobytes_per_second The speed in kilobytes/second of read operations for this GEOM
# TYPE gstat_read_kilobytes_per_second gauge
gstat_read_kilobytes_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_read_kilobytes_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_read_kilobytes_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_miliseconds_per_read The speed in miliseconds/read operation for this GEOM
# TYPE gstat_miliseconds_per_read gauge
gstat_miliseconds_per_read{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_miliseconds_per_read{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_miliseconds_per_read{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_write_operations_per_second The number of write operations/second for this GEOM
# TYPE gstat_write_operations_per_second gauge
gstat_write_operations_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_write_operations_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_write_operations_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_write_size_kilobytes The size in kilobytes of write operations for this GEOM
# TYPE gstat_write_size_kilobytes gauge
gstat_write_size_kilobytes{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_write_size_kilobytes{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_write_size_kilobytes{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_write_kilobytes_per_second The speed in kilobytes/second of write operations for this GEOM
# TYPE gstat_write_kilobytes_per_second gauge
gstat_write_kilobytes_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_write_kilobytes_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_write_kilobytes_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_miliseconds_per_write The speed in miliseconds/write operation for this GEOM
# TYPE gstat_miliseconds_per_write gauge
gstat_miliseconds_per_write{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_miliseconds_per_write{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_miliseconds_per_write{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_delete_operations_per_second The number of delete operations/second for this GEOM
# TYPE gstat_delete_operations_per_second gauge
gstat_delete_operations_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_delete_operations_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_delete_operations_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_delete_size_kilobytes The size in kilobytes of delete operations for this GEOM
# TYPE gstat_delete_size_kilobytes gauge
gstat_delete_size_kilobytes{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_delete_size_kilobytes{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_delete_size_kilobytes{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_delete_kilobytes_per_second The speed in kilobytes/second of delete operations for this GEOM
# TYPE gstat_delete_kilobytes_per_second gauge
gstat_delete_kilobytes_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_delete_kilobytes_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_delete_kilobytes_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_miliseconds_per_delete The speed in miliseconds/delete operation for this GEOM
# TYPE gstat_miliseconds_per_delete gauge
gstat_miliseconds_per_delete{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_miliseconds_per_delete{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_miliseconds_per_delete{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_other_operations_per_second The number of other operations (BIO_FLUSH)/second for this GEOM
# TYPE gstat_other_operations_per_second gauge
gstat_other_operations_per_second{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_other_operations_per_second{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_other_operations_per_second{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_miliseconds_per_other The speed in miliseconds/other operation (BIO_FLUSH) for this GEOM
# TYPE gstat_miliseconds_per_other gauge
gstat_miliseconds_per_other{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_miliseconds_per_other{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_miliseconds_per_other{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
# HELP gstat_percent_busy The percent of the time this GEOM is busy
# TYPE gstat_percent_busy gauge
gstat_percent_busy{descr="WDC WDS500G2B0B-00YS70",fwheads="16",fwsectors="63",ident="212989464604",lunid="5001b444a72bc7d9",mediasize="500107862016 (466G)",name="ada0",rotationrate="0",sectorsize="512"} 0.0
gstat_percent_busy{descr="WDC WD181KRYZ-01AGBB0",fwheads="16",fwsectors="63",ident="3WJJG8NK",lunid="5000cca284e3aa8c",mediasize="18000207937536 (16T)",name="ada1",rotationrate="7200",sectorsize="512"} 0.0
gstat_percent_busy{descr="ST18000NE000-2YY101",fwheads="16",fwsectors="63",ident="ZR50A7AJ",lunid="5000c500c7dc3971",mediasize="18000207937536 (16T)",name="ada2",rotationrate="7200",sectorsize="512"} 0.0
```
