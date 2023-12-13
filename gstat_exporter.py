from prometheus_client import start_http_server, Gauge  # type: ignore
from subprocess import Popen, PIPE
from typing import Dict
from importlib.metadata import PackageNotFoundError, version

# get version
try:
    __version__ = version("gstat_exporter")
except PackageNotFoundError:
    # package is not installed, version unknown
    __version__ = "0.0.0"


def get_deviceinfo(name: str) -> Dict[str, str]:
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


def process_request() -> None:
    """
    Run gstat in a loop and update stats per line
    """
    # start with an empty deviceinfo dict and add devices as we see them
    deviceinfo: Dict[str, Dict[str, str]] = {}

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
                # this is the first time we see this GEOM
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
                # get real info from the device if it is class DISK
                deviceinfo[name].update(get_deviceinfo(name))

            deviceinfo[name].update({"name": name})

            # up is always.. up
            up.set(1)

            queue.labels(**deviceinfo[name]).set(queue_depth)
            totalops.labels(**deviceinfo[name]).set(total_operations_per_second)

            readops.labels(**deviceinfo[name]).set(read_operations_per_second)
            readsize.labels(**deviceinfo[name]).set(read_size_kilobytes)
            readkbs.labels(**deviceinfo[name]).set(read_kilobytes_per_second)
            readms.labels(**deviceinfo[name]).set(miliseconds_per_read)

            writeops.labels(**deviceinfo[name]).set(write_operations_per_second)
            writesize.labels(**deviceinfo[name]).set(write_size_kilobytes)
            writekbs.labels(**deviceinfo[name]).set(write_kilobytes_per_second)
            writems.labels(**deviceinfo[name]).set(miliseconds_per_write)

            deleteops.labels(**deviceinfo[name]).set(delete_operations_per_second)
            deletesize.labels(**deviceinfo[name]).set(delete_size_kilobytes)
            deletekbs.labels(**deviceinfo[name]).set(delete_kilobytes_per_second)
            deletems.labels(**deviceinfo[name]).set(miliseconds_per_delete)

            otherops.labels(**deviceinfo[name]).set(other_operations_per_second)
            otherms.labels(**deviceinfo[name]).set(miliseconds_per_other)

            busy.labels(**deviceinfo[name]).set(percent_busy)


# define metrics
up = Gauge(
    "gstat_up", "The value of this Gauge is always 1 when the gstat_exporter is up"
)

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
    "The total number of operations/second for this GEOM",
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
    "The number of read operations/second for this GEOM",
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
    "The speed in kilobytes/second of read operations for this GEOM",
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
    "The speed in miliseconds/read operation for this GEOM",
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
    "The number of write operations/second for this GEOM",
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
    "The speed in kilobytes/second of write operations for this GEOM",
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
    "The speed in miliseconds/write operation for this GEOM",
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
    "The number of delete operations/second for this GEOM",
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
    "The speed in kilobytes/second of delete operations for this GEOM",
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
    "The speed in miliseconds/delete operation for this GEOM",
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
    "The number of other operations (BIO_FLUSH)/second for this GEOM",
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
    "The speed in miliseconds/other operation (BIO_FLUSH) for this GEOM",
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

start_http_server(9248)
while True:
    process_request()
