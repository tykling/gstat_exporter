from prometheus_client import start_http_server, Gauge
from subprocess import Popen, PIPE


def get_deviceinfo(name):
    """
    Return a dict of GEOM device info for GEOM devices in class DISK,
    for use as labels for the metrics.

    Sample output from the geom command:

    $ geom -p ada0
    Geom class: DISK
    Geom name: ada0
    Providers:
    1. Name: ada0
       Mediasize: 250059350016 (233G)
       Sectorsize: 512
       Mode: r2w2e4
       descr: Samsung SSD 860 EVO mSATA 250GB
       lunid: 5002538e700b753f
       ident: S41MNG0K907238X
       rotationrate: 0
       fwsectors: 63
       fwheads: 16
    $
    """
    with Popen(
        ["geom", "-p", name], stdout=PIPE, bufsize=1, universal_newlines=True
    ) as p:
        result = {}
        for line in p.stdout:
            # remove excess whitespace
            line = line.strip()
            # we only care about the DISK class for now
            if line[0:12] == "Geom class: " and line[-4:] != "DISK":
                break

            if line[0:11] == "Mediasize: ":
                result["mediasize"] = line[11:]
            if line[0:12] == "Sectorsize: ":
                result["sectorsize"] = line.split(" ")[1]
            if line[0:7] == "descr: ":
                result["descr"] = " ".join(line.split(" ")[1:])
            if line[0:7] == "lunid: ":
                result["lunid"] = line.split(" ")[1]
            if line[0:7] == "ident: ":
                result["ident"] = line.split(" ")[1]
            if line[0:14] == "rotationrate: ":
                result["rotationrate"] = line.split(" ")[1]
            if line[0:11] == "fwsectors: ":
                result["fwsectors"] = line.split(" ")[1]
            if line[0:9] == "fwheads: ":
                result["fwheads"] = line.split(" ")[1]
        return result


def process_request():
    """
    Run gstat in a loop and update stats per line
    """
    global deviceinfo
    with Popen(
        ["gstat", "-pdosCI", "5s"], stdout=PIPE, bufsize=1, universal_newlines=True
    ) as p:
        for line in p.stdout:
            (
                timestamp,
                name,
                queue_depth,
                total_operations_per_second,
                read_operations_per_second,
                read_size_kilobytes,
                read_kilobytes_per_second,
                miliseconds_per_read,
                write_operations_per_second,
                write_size_kilobytes,
                write_kilobytes_per_second,
                miliseconds_per_write,
                delete_operations_per_second,
                delete_size_kilobytes,
                delete_kilobytes_per_second,
                miliseconds_per_delete,
                other_operations_per_second,
                miliseconds_per_other,
                percent_busy,
            ) = line.split(",")
            if timestamp == "timestamp":
                # skip header line
                continue

            if name not in deviceinfo:
                deviceinfo[name] = {}
                # we always need a value for all labels
                for key in [
                    "name",
                    "descr",
                    "mediasize",
                    "sectorsize",
                    "lunid",
                    "ident",
                    "rotationrate",
                    "fwsectors",
                    "fwheads",
                ]:
                    deviceinfo[name][key] = ""
                # get info from the device if it is class DISK
                deviceinfo[name].update(get_deviceinfo(name))

            labels = deviceinfo[name]
            labels.update({"name": name})

            queue.labels(**labels).set(queue_depth)
            totalops.labels(**labels).set(total_operations_per_second)

            readops.labels(**labels).set(read_operations_per_second)
            readsize.labels(**labels).set(read_size_kilobytes)
            readkbs.labels(**labels).set(read_kilobytes_per_second)
            readms.labels(**labels).set(miliseconds_per_read)

            writeops.labels(**labels).set(write_operations_per_second)
            writesize.labels(**labels).set(write_size_kilobytes)
            writekbs.labels(**labels).set(write_kilobytes_per_second)
            writems.labels(**labels).set(miliseconds_per_write)

            deleteops.labels(**labels).set(delete_operations_per_second)
            deletesize.labels(**labels).set(delete_size_kilobytes)
            deletekbs.labels(**labels).set(delete_kilobytes_per_second)
            deletems.labels(**labels).set(miliseconds_per_delete)

            otherops.labels(**labels).set(other_operations_per_second)
            otherms.labels(**labels).set(miliseconds_per_other)

            busy.labels(**labels).set(percent_busy)


# define metrics
queue = Gauge(
    "gstat_queue_depth",
    "The queue depth for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
totalops = Gauge(
    "gstat_total_operations_per_second",
    "The total number operations for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)

readops = Gauge(
    "gstat_read_operations_per_second",
    "The number of read operations per second for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
readsize = Gauge(
    "gstat_read_size_kilobytes",
    "The size in kilobytes of read operations for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
readkbs = Gauge(
    "gstat_read_kilobytes_per_second",
    "The speed in kilobytes per second of read operations for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
readms = Gauge(
    "gstat_miliseconds_per_read",
    "The speed in miliseconds per read operation for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)

writeops = Gauge(
    "gstat_write_operations_per_second",
    "The number of write operations per second for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
writesize = Gauge(
    "gstat_write_size_kilobytes",
    "The size in kilobytes of write operations for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
writekbs = Gauge(
    "gstat_write_kilobytes_per_second",
    "The speed in kilobytes per second of write operations for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
writems = Gauge(
    "gstat_miliseconds_per_write",
    "The speed in miliseconds per write operation for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)

deleteops = Gauge(
    "gstat_delete_operations_per_second",
    "The number of delete operations per second for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
deletesize = Gauge(
    "gstat_delete_size_kilobytes",
    "The size in kilobytes of delete operations for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
deletekbs = Gauge(
    "gstat_delete_kilobytes_per_second",
    "The speed in kilobytes per second of delete operations for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
deletems = Gauge(
    "gstat_miliseconds_per_delete",
    "The speed in miliseconds per delete operation for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)

otherops = Gauge(
    "gstat_other_operations_per_second",
    "The number of other operations (BIO_FLUSH) per second for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)
otherms = Gauge(
    "gstat_miliseconds_per_other",
    "The speed in miliseconds per other operation (BIO_FLUSH) for this GEOM",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)

busy = Gauge(
    "gstat_percent_busy",
    "The percent of the time this GEOM is busy",
    [
        "name",
        "descr",
        "mediasize",
        "sectorsize",
        "lunid",
        "ident",
        "rotationrate",
        "fwsectors",
        "fwheads",
    ],
)

# start with an empty deviceinfo dict
deviceinfo = {}

start_http_server(9248)
while True:
    process_request()
