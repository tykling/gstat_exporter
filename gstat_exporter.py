from prometheus_client import start_http_server, Gauge
import argparse
import logging
import datetime
from subprocess import Popen, PIPE
from typing import Dict
from importlib.metadata import PackageNotFoundError, version

# get version
try:
    __version__ = version("gstat_exporter")
except PackageNotFoundError:
    # package is not installed, version unknown
    __version__ = "0.0.0"

class GstatExporter:
    def __init__(self, interval: int = 30, grace: int = 30, sleep: int = 15) -> None:
        """Define metrics and other neccesary variables."""
        # save interval, grace, and sleep
        self.interval = interval
        self.grace = grace
        self.sleep = sleep

        # save the version as a class attribute
        self.__version__ = __version__

        # define the metric labels
        self.labels: list[str] = [
            "name",
            "descr",
            "mediasize",
            "sectorsize",
            "lunid",
            "ident",
            "rotationrate",
            "fwsectors",
            "fwheads",
        ]

        # define the metrics
        self.metrics: dict[str, Gauge] = {}
        self.metrics["up"] = Gauge(
            "gstat_up",
            "The value of this Gauge is always 1 when the gstat_exporter is up",
        )

        self.metrics["queue"] = Gauge(
            "gstat_queue_depth",
            "The queue depth for this GEOM",
            self.labels,
        )
        self.metrics["totalops"] = Gauge(
            "gstat_total_operations_per_second",
            "The total number of operations/second for this GEOM",
            self.labels,
        )

        self.metrics["readops"] = Gauge(
            "gstat_read_operations_per_second",
            "The number of read operations/second for this GEOM",
            self.labels,
        )
        self.metrics["readsize"] = Gauge(
            "gstat_read_size_kilobytes",
            "The size in kilobytes of read operations for this GEOM",
            self.labels,
        )
        self.metrics["readkbs"] = Gauge(
            "gstat_read_kilobytes_per_second",
            "The speed in kilobytes/second of read operations for this GEOM",
            self.labels,
        )
        self.metrics["readms"] = Gauge(
            "gstat_miliseconds_per_read",
            "The speed in miliseconds/read operation for this GEOM",
            self.labels,
        )

        self.metrics["writeops"] = Gauge(
            "gstat_write_operations_per_second",
            "The number of write operations/second for this GEOM",
            self.labels,
        )
        self.metrics["writesize"] = Gauge(
            "gstat_write_size_kilobytes",
            "The size in kilobytes of write operations for this GEOM",
            self.labels,
        )
        self.metrics["writekbs"] = Gauge(
            "gstat_write_kilobytes_per_second",
            "The speed in kilobytes/second of write operations for this GEOM",
            self.labels,
        )
        self.metrics["writems"] = Gauge(
            "gstat_miliseconds_per_write",
            "The speed in miliseconds/write operation for this GEOM",
            self.labels,
        )

        self.metrics["deleteops"] = Gauge(
            "gstat_delete_operations_per_second",
            "The number of delete operations/second for this GEOM",
            self.labels,
        )
        self.metrics["deletesize"] = Gauge(
            "gstat_delete_size_kilobytes",
            "The size in kilobytes of delete operations for this GEOM",
            self.labels,
        )
        self.metrics["deletekbs"] = Gauge(
            "gstat_delete_kilobytes_per_second",
            "The speed in kilobytes/second of delete operations for this GEOM",
            self.labels,
        )
        self.metrics["deletems"] = Gauge(
            "gstat_miliseconds_per_delete",
            "The speed in miliseconds/delete operation for this GEOM",
            self.labels,
        )

        self.metrics["otherops"] = Gauge(
            "gstat_other_operations_per_second",
            "The number of other operations (BIO_FLUSH)/second for this GEOM",
            self.labels,
        )
        self.metrics["otherms"] = Gauge(
            "gstat_miliseconds_per_other",
            "The speed in miliseconds/other operation (BIO_FLUSH) for this GEOM",
            self.labels,
        )

        self.metrics["busy"] = Gauge(
            "gstat_percent_busy",
            "The percent of the time this GEOM is busy",
            self.labels,
        )

        # start with an empty deviceinfo dict and add devices as we see them
        self.deviceinfo: Dict[str, Dict[str, str]] = {}

        # variables used for checking for removed devices
        self.lastcheck = datetime.datetime.now()
        self.timestamps: Dict[str, datetime.datetime] = {}

        logging.debug("Done initialising GstatExporter class")

    def get_deviceinfo(self, name: str) -> Dict[str, str]:
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
        logging.debug(f"Getting deviceinfo for GEOM {name}...")
        with Popen(
            ["geom", "-p", name], stdout=PIPE, bufsize=1, universal_newlines=True
        ) as p:
            result = {}
            for line in p.stdout:  # type: ignore
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
            logging.debug(f"Returning deviceinfo for {name}: {result}")
            return result

    def run_gstat_forever(self) -> None:
        """
        Run gstat in a loop and update stats per line
        """
        logging.debug(f"Running 'gstat -pdosCI {self.sleep}s' (will loop forever)...")
        with Popen(
            ["gstat", "-pdosCI", f"{self.sleep}s"], stdout=PIPE, bufsize=1, universal_newlines=True
        ) as p:
            # loop over lines in the output
            for line in p.stdout:  # type: ignore
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

                # first check if this GEOM has been seen before
                if name not in self.deviceinfo:
                    logging.info(f"Adding new GEOM to deviceinfo: {name}")
                    # this is the first time we see this GEOM
                    self.deviceinfo[name] = {}
                    # we always need a value for all labels
                    for key in self.labels:
                        self.deviceinfo[name][key] = ""
                    # get real info from the device if it is class DISK
                    self.deviceinfo[name].update(self.get_deviceinfo(name))
                    self.deviceinfo[name].update({"name": name})

                # update timestamp to track when this GEOM was last seen
                self.timestamps[name] = datetime.datetime.strptime(
                    timestamp.split(".")[0], "%Y-%m-%d %H:%M:%S"
                )

                # up is always.. up
                self.metrics["up"].set(1)

                self.metrics["queue"].labels(**self.deviceinfo[name]).set(queue_depth)
                self.metrics["totalops"].labels(**self.deviceinfo[name]).set(
                    total_operations_per_second
                )

                self.metrics["readops"].labels(**self.deviceinfo[name]).set(
                    read_operations_per_second
                )
                self.metrics["readsize"].labels(**self.deviceinfo[name]).set(
                    read_size_kilobytes
                )
                self.metrics["readkbs"].labels(**self.deviceinfo[name]).set(
                    read_kilobytes_per_second
                )
                self.metrics["readms"].labels(**self.deviceinfo[name]).set(
                    miliseconds_per_read
                )

                self.metrics["writeops"].labels(**self.deviceinfo[name]).set(
                    write_operations_per_second
                )
                self.metrics["writesize"].labels(**self.deviceinfo[name]).set(
                    write_size_kilobytes
                )
                self.metrics["writekbs"].labels(**self.deviceinfo[name]).set(
                    write_kilobytes_per_second
                )
                self.metrics["writems"].labels(**self.deviceinfo[name]).set(
                    miliseconds_per_write
                )

                self.metrics["deleteops"].labels(**self.deviceinfo[name]).set(
                    delete_operations_per_second
                )
                self.metrics["deletesize"].labels(**self.deviceinfo[name]).set(
                    delete_size_kilobytes
                )
                self.metrics["deletekbs"].labels(**self.deviceinfo[name]).set(
                    delete_kilobytes_per_second
                )
                self.metrics["deletems"].labels(**self.deviceinfo[name]).set(
                    miliseconds_per_delete
                )

                self.metrics["otherops"].labels(**self.deviceinfo[name]).set(
                    other_operations_per_second
                )
                self.metrics["otherms"].labels(**self.deviceinfo[name]).set(
                    miliseconds_per_other
                )

                self.metrics["busy"].labels(**self.deviceinfo[name]).set(percent_busy)

                # check for removed GEOMs
                now = datetime.datetime.now()
                if (now - self.lastcheck).seconds > self.interval:
                    logging.debug("Running periodic check for removed devices...")
                    # enough time has passed since the last check
                    # loop over devices and check timestamp for each
                    remove = []
                    for name in self.deviceinfo.keys():
                        delta = (now - self.timestamps[name]).seconds
                        if delta > self.grace:
                            remove.append(name)
                            logging.info(
                                f"It has been {self.grace} seconds since gstat last reported data for GEOM {name} - removing metrics"
                            )

                    # loop over the GEOMs for which gstat stopped giving data and remove them
                    for name in remove:
                        # it has been too long since we have seen this GEOM, remove it
                        for metric in self.metrics.keys():
                            if metric == "up":
                                # skip the up metric
                                continue
                            self.metrics[metric].remove(*self.deviceinfo[name].values())
                        del self.deviceinfo[name]
                    self.lastcheck = datetime.datetime.now()


def main() -> None:
    """Run the main function."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-g",
        "--grace",
        type=int,
        help="Stop exporting metrics for a GEOM after gstat has not reported data from it for this many seconds. Defaults to 30 seconds.",
        default=30,
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        help="How many seconds to wait between checking for removed devices. Defaults to 30 seconds.",
        default=30,
    )
    parser.add_argument(
        "-l",
        "--listen-ip",
        type=str,
        help="Listen IP. Defaults to 0.0.0.0 (all v4 IPs). Set to :: to listen on all v6 IPs.",
        default="0.0.0.0",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Portnumber. Defaults to 9248.",
        default=9248,
    )
    parser.add_argument(
        "-s",
        "--sleep",
        type=int,
        help="How long should gstat sleep between reporting data, in seconds. Set this to the same as your Prometheus scrape interval. Defaults to 15.",
        default=15,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const="DEBUG",
        help="Debug mode.",
        default="INFO",
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    logging.info(f"Starting gstat_exporter v{__version__} - logging at level {args.loglevel}")
    logging.info(f"Starting HTTP listener on address '{args.listen_ip}' port '{args.port}'")
    start_http_server(addr=args.listen_ip, port=args.port)
    exporter = GstatExporter(interval=args.interval, grace=args.grace, sleep=args.sleep)
    while True:
        exporter.run_gstat_forever()

if __name__ == "__main__":
    main()
