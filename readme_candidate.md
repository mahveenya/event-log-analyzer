# Take-home exercise: Event Log Analyzer

## Context

You will find attached `event\_log\_sample.csv` which is an event log export from a hardware device. The device logs
everything it does, such as: boot sequence, sensor state, Bluetooth connections — as tab-separated rows.

Your job: write a small Python program that loads this file and does basic data collection,
such as filtering by severity, counting event amounts and error rate of the device.

Note: despite the `.csv` extension, the file is **tab-separated**, not comma-separated.



## What to build

1. An `EventSeverity` type that supports ordering

   * The severity goes as follows:

     * `Info`
     * `Warning`
     * `Error`
2. An `Event` class representing one row.
3. A loader that reads the file into a list of `Event` objects.
4. An `EventLog` class (wraps the list of events) with at least these methods:

   * `filter\_by\_severity(min\_severity)` — events at or above a given severity
   * `count\_by\_object()` — dict of object name → count
   * `error\_rate` — property: fraction of events that are `Error` severity

## How to share

Please create a GitHub repository and add all corresponding code there.
This repository needs to be used to share your solution with us.
Please ensure that the work is committed incrementally and not in bulk.

## Constraints

* No pandas, no third-party CSV/data libraries.

