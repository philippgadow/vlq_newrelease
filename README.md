## Development of the VLQ job option for Atlas MC Generation releases 21.6.23 and later


### Run this example quickly

Run in release `21.6.58` (CC7)

```
git clone git@github.com:philippgadow/vlq_newrelease.git
source setup.sh
source run.sh
```

Run in release `21.6.48` (SL6)

```
git clone git@github.com:philippgadow/vlq_newrelease.git
source setup_sl6.sh
# now inside SL6 singularity container
source setup_sl6.sh
source run.sh
```

### Modify job option

Take the job option [`100xxx/100001/mc.MGPy8EG_ZBHb1000LH100_sigonly.py`](https://github.com/philippgadow/vlq_newrelease/blob/master/100xxx/100001/mc.MGPy8EG_ZBHb1000LH100_sigonly.py) to implement your changes for testing.
All other job options are symlinks to this file.


### DSID logbook

#### nominal samples

| ------ | -------------- | ---- | -------- | -------- |
| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 100001 | ZBHb (sigonly) | 1000 | 1.0      | yes      |
| 100002 | ZBHb (sigbar)  | 1000 | 1.0      | yes      |
| 100003 | ZBHb (sigonly) | 1200 | 1.0      | yes      |
| 100004 | ZBHb (sigbar)  | 1200 | 1.0      | yes      |
| 100005 | ZBHb (sigonly) | 1400 | 1.0      | yes      |
| 100006 | ZBHb (sigbar)  | 1400 | 1.0      | yes      |
| 100007 | ZBHb (sigonly) | 1600 | 1.0      | yes      |
| 100008 | ZBHb (sigbar)  | 1600 | 1.0      | yes      |
| 100009 | ZBHb (sigonly) | 1800 | 1.0      | yes      |
| 100010 | ZBHb (sigbar)  | 1800 | 1.0      | yes      |
| 100011 | ZBHb (sigonly) | 2000 | 1.0      | yes      |
| 100012 | ZBHb (sigbar)  | 2000 | 1.0      | yes      |
| 100013 | ZBHb (sigonly) | 2200 | 1.0      | yes      |
| 100014 | ZBHb (sigbar)  | 2200 | 1.0      | yes      |
| 100015 | ZBHb (sigonly) | 2400 | 1.0      | yes      |
| 100016 | ZBHb (sigbar)  | 2400 | 1.0      | yes      |
| 100017 | WBHb (sig)     | 1000 | 1.0      | yes      |
| 100018 | WBHb (sig)     | 1200 | 1.0      | yes      |
| 100019 | WBHb (sig)     | 1400 | 1.0      | yes      |
| 100020 | WBHb (sig)     | 1600 | 1.0      | yes      |
| 100021 | WBHb (sig)     | 1800 | 1.0      | yes      |
| 100022 | WBHb (sig)     | 2000 | 1.0      | yes      |
| 100023 | WBHb (sig)     | 2200 | 1.0      | yes      |
| 100024 | WBHb (sig)     | 2400 | 1.0      | yes      |
| 100025 | ZBHb (sigonly) |  800 | 1.0      | yes      |
| 100026 | ZBHb (sigbar)  |  800 | 1.0      | yes      |
| 100027 | WBHb (sig)     |  800 | 1.0      | yes      |
| ------ | -------------- | ---- | -------- | -------- |

#### mass closure test

| ------ | -------------- | ---- | -------- | -------- |
| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 100100 | ZBHb (sigonly) | 1300 | 1.0      | no       |
| 100101 | ZBHb (sigbar)  | 1300 | 1.0      | no       |
| 100102 | WBHb (sig)     | 1300 | 1.0      | no       |
| 100103 | ZBHb (sigonly) | 1900 | 1.0      | no       |
| 100104 | ZBHb (sigbar)  | 1900 | 1.0      | no       |
| 100105 | WBHb (sig)     | 1900 | 1.0      | no       |
| ------ | -------------- | ---- | -------- | -------- |

#### coupling closure test

| ------ | -------------- | ---- | -------- | -------- |
| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 100110 | ZBHb (sigonly) | 1400 | 0.1      | no       |
| 100111 | ZBHb (sigbar)  | 1400 | 0.1      | no       |
| 100112 | WBHb (sig)     | 1400 | 0.1      | no       |
| 100113 | ZBHb (sigonly) | 1400 | 0.4      | no       |
| 100114 | ZBHb (sigbar)  | 1400 | 0.4      | no       |
| 100115 | WBHb (sig)     | 1400 | 0.4      | no       |
| 100116 | ZBHb (sigonly) | 1400 | 1.3      | no       |
| 100117 | ZBHb (sigbar)  | 1400 | 1.3      | no       |
| 100118 | WBHb (sig)     | 1400 | 1.3      | no       |
| 100119 | ZBHb (sigonly) | 1400 | 1.6      | no       |
| 100120 | ZBHb (sigbar)  | 1400 | 1.6      | no       |
| 100121 | WBHb (sig)     | 1400 | 1.6      | no       |
| ------ | -------------- | ---- | -------- | -------- |
