## Development of the VLQ job option for Atlas MC Generation releases 21.6.23 and later


### Run this example quickly

Run in release `21.6.57` (CC7)

```
git clone git@github.com:philippgadow/vlq_newrelease.git
source setup.sh
source run.sh
```


### Modify job option

Take the job option [`100xxx/100001/mc.MGPy8EG_ZBHb1000LH100_sigonly.py`](https://github.com/philippgadow/vlq_newrelease/blob/master/100xxx/100001/mc.MGPy8EG_ZBHb1000LH100_sigonly.py) to implement your changes for testing.
All other job options inside `100xxx` are symlinks to this file. Similar is true for the job options inside `101xxx` (and other directories), where only `101xxx/101000` will include the file and the other directories will point to it. Have a look at the logbook of DSIDs to identify the most recent version and those kept for documentation.


### DSID logbook

#### VLB Hb nominal samples, including t-channel processes (with reweighting, LO PDF)

These samples correspond to the final job options which were used to create simulated EVNT and AOD samples.

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 107000 | ZBHb (sig)     | 1000 | 0.4      | yes      |
| 107001 | ZBHb (sig)     | 1000 | 1.0      | yes      |
| 107002 | ZBHb (sig)     | 1200 | 0.4      | yes      |
| 107003 | ZBHb (sig)     | 1200 | 1.0      | yes      |
| 107004 | ZBHb (sig)     | 1400 | 0.4      | yes      |
| 107005 | ZBHb (sig)     | 1400 | 1.0      | yes      |
| 107006 | ZBHb (sig)     | 1600 | 0.4      | yes      |
| 107007 | ZBHb (sig)     | 1600 | 1.0      | yes      |
| 107008 | ZBHb (sig)     | 1800 | 0.4      | yes      |
| 107009 | ZBHb (sig)     | 1800 | 1.0      | yes      |
| 107010 | ZBHb (sig)     | 2000 | 0.4      | yes      |
| 107011 | ZBHb (sig)     | 2000 | 1.0      | yes      |
| 107012 | ZBHb (sig)     | 2200 | 0.4      | yes      |
| 107013 | ZBHb (sig)     | 2200 | 1.0      | yes      |
| 107014 | ZBHb (sig)     | 2400 | 0.4      | yes      |
| 107015 | ZBHb (sig)     | 2400 | 1.0      | yes      |
| 107016 | WBHb (sig)     | 1000 | 0.4      | yes      |
| 107017 | WBHb (sig)     | 1000 | 1.0      | yes      |
| 107018 | WBHb (sig)     | 1200 | 0.4      | yes      |
| 107019 | WBHb (sig)     | 1200 | 1.0      | yes      |
| 107020 | WBHb (sig)     | 1400 | 0.4      | yes      |
| 107021 | WBHb (sig)     | 1400 | 1.0      | yes      |
| 107022 | WBHb (sig)     | 1600 | 0.4      | yes      |
| 107023 | WBHb (sig)     | 1600 | 1.0      | yes      |
| 107024 | WBHb (sig)     | 1800 | 0.4      | yes      |
| 107025 | WBHb (sig)     | 1800 | 1.0      | yes      |
| 107026 | WBHb (sig)     | 2000 | 0.4      | yes      |
| 107027 | WBHb (sig)     | 2000 | 1.0      | yes      |
| 107028 | WBHb (sig)     | 2200 | 0.4      | yes      |
| 107029 | WBHb (sig)     | 2200 | 1.0      | yes      |
| 107030 | WBHb (sig)     | 2400 | 0.4      | yes      |
| 107031 | WBHb (sig)     | 2400 | 1.0      | yes      |


#### VLB Hb(yy) nominal samples, including t-channel processes (with reweighting, LO PDF)

These samples correspond to the final job options which were used to create simulated EVNT and AOD samples.

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 108000 | ZBH(yy)b (sig) | 1000 | 0.4      | yes      |
| 108001 | ZBH(yy)b (sig) | 1000 | 1.0      | yes      |
| 108002 | ZBH(yy)b (sig) | 1200 | 0.4      | yes      |
| 108003 | ZBH(yy)b (sig) | 1200 | 1.0      | yes      |
| 108004 | ZBH(yy)b (sig) | 1400 | 0.4      | yes      |
| 108005 | ZBH(yy)b (sig) | 1400 | 1.0      | yes      |
| 108006 | ZBH(yy)b (sig) | 1600 | 0.4      | yes      |
| 108007 | ZBH(yy)b (sig) | 1600 | 1.0      | yes      |
| 108008 | ZBH(yy)b (sig) | 1800 | 0.4      | yes      |
| 108009 | ZBH(yy)b (sig) | 1800 | 1.0      | yes      |
| 108010 | ZBH(yy)b (sig) | 2000 | 0.4      | yes      |
| 108011 | ZBH(yy)b (sig) | 2000 | 1.0      | yes      |
| 108012 | ZBH(yy)b (sig) | 2200 | 0.4      | yes      |
| 108013 | ZBH(yy)b (sig) | 2200 | 1.0      | yes      |
| 108014 | ZBH(yy)b (sig) | 2400 | 0.4      | yes      |
| 108015 | ZBH(yy)b (sig) | 2400 | 1.0      | yes      |
| 108016 | WBH(yy)b (sig) | 1000 | 0.4      | yes      |
| 108017 | WBH(yy)b (sig) | 1000 | 1.0      | yes      |
| 108018 | WBH(yy)b (sig) | 1200 | 0.4      | yes      |
| 108019 | WBH(yy)b (sig) | 1200 | 1.0      | yes      |
| 108020 | WBH(yy)b (sig) | 1400 | 0.4      | yes      |
| 108021 | WBH(yy)b (sig) | 1400 | 1.0      | yes      |
| 108022 | WBH(yy)b (sig) | 1600 | 0.4      | yes      |
| 108023 | WBH(yy)b (sig) | 1600 | 1.0      | yes      |
| 108024 | WBH(yy)b (sig) | 1800 | 0.4      | yes      |
| 108025 | WBH(yy)b (sig) | 1800 | 1.0      | yes      |
| 108026 | WBH(yy)b (sig) | 2000 | 0.4      | yes      |
| 108027 | WBH(yy)b (sig) | 2000 | 1.0      | yes      |
| 108028 | WBH(yy)b (sig) | 2200 | 0.4      | yes      |
| 108029 | WBH(yy)b (sig) | 2200 | 1.0      | yes      |
| 108030 | WBH(yy)b (sig) | 2400 | 0.4      | yes      |
| 108031 | WBH(yy)b (sig) | 2400 | 1.0      | yes      |

#### VLB Hb nominal samples, including t-channel processes (with reweighting, LO PDF)

Buggy samples, the file name botched up the coupling strength.

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 105000 | ZBHb (sig)     | 1000 | 0.02     | yes      |
| 105001 | ZBHb (sig)     | 1000 | 0.02     | yes      |
| 105002 | ZBHb (sig)     | 1200 | 0.02     | yes      |
| 105003 | ZBHb (sig)     | 1200 | 0.02     | yes      |
| 105004 | ZBHb (sig)     | 1400 | 0.02     | yes      |
| 105005 | ZBHb (sig)     | 1400 | 0.02     | yes      |
| 105006 | ZBHb (sig)     | 1600 | 0.02     | yes      |
| 105007 | ZBHb (sig)     | 1600 | 0.02     | yes      |
| 105008 | ZBHb (sig)     | 1800 | 0.02     | yes      |
| 105009 | ZBHb (sig)     | 1800 | 0.02     | yes      |
| 105010 | ZBHb (sig)     | 2000 | 0.02     | yes      |
| 105011 | ZBHb (sig)     | 2000 | 0.02     | yes      |
| 105012 | ZBHb (sig)     | 2200 | 0.02     | yes      |
| 105013 | ZBHb (sig)     | 2200 | 0.02     | yes      |
| 105014 | ZBHb (sig)     | 2400 | 0.02     | yes      |
| 105015 | ZBHb (sig)     | 2400 | 0.02     | yes      |
| 105016 | WBHb (sig)     | 1000 | 0.02     | yes      |
| 105017 | WBHb (sig)     | 1000 | 0.02     | yes      |
| 105018 | WBHb (sig)     | 1200 | 0.02     | yes      |
| 105019 | WBHb (sig)     | 1200 | 0.02     | yes      |
| 105020 | WBHb (sig)     | 1400 | 0.02     | yes      |
| 105021 | WBHb (sig)     | 1400 | 0.02     | yes      |
| 105022 | WBHb (sig)     | 1600 | 0.02     | yes      |
| 105023 | WBHb (sig)     | 1600 | 0.02     | yes      |
| 105024 | WBHb (sig)     | 1800 | 0.02     | yes      |
| 105025 | WBHb (sig)     | 1800 | 0.02     | yes      |
| 105026 | WBHb (sig)     | 2000 | 0.02     | yes      |
| 105027 | WBHb (sig)     | 2000 | 0.02     | yes      |
| 105028 | WBHb (sig)     | 2200 | 0.02     | yes      |
| 105029 | WBHb (sig)     | 2200 | 0.02     | yes      |
| 105030 | WBHb (sig)     | 2400 | 0.02     | yes      |
| 105031 | WBHb (sig)     | 2400 | 0.02     | yes      |


#### VLB Hb(yy) nominal samples, including t-channel processes (with reweighting, LO PDF)

Buggy samples, the file name botched up the coupling strength.

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 106000 | ZBH(yy)b (sig) | 1000 | 0.02     | yes      |
| 106001 | ZBH(yy)b (sig) | 1000 | 0.02     | yes      |
| 106002 | ZBH(yy)b (sig) | 1200 | 0.02     | yes      |
| 106003 | ZBH(yy)b (sig) | 1200 | 0.02     | yes      |
| 106004 | ZBH(yy)b (sig) | 1400 | 0.02     | yes      |
| 106005 | ZBH(yy)b (sig) | 1400 | 0.02     | yes      |
| 106006 | ZBH(yy)b (sig) | 1600 | 0.02     | yes      |
| 106007 | ZBH(yy)b (sig) | 1600 | 0.02     | yes      |
| 106008 | ZBH(yy)b (sig) | 1800 | 0.02     | yes      |
| 106009 | ZBH(yy)b (sig) | 1800 | 0.02     | yes      |
| 106010 | ZBH(yy)b (sig) | 2000 | 0.02     | yes      |
| 106011 | ZBH(yy)b (sig) | 2000 | 0.02     | yes      |
| 106012 | ZBH(yy)b (sig) | 2200 | 0.02     | yes      |
| 106013 | ZBH(yy)b (sig) | 2200 | 0.02     | yes      |
| 106014 | ZBH(yy)b (sig) | 2400 | 0.02     | yes      |
| 106015 | ZBH(yy)b (sig) | 2400 | 0.02     | yes      |
| 106016 | WBH(yy)b (sig) | 1000 | 0.02     | yes      |
| 106017 | WBH(yy)b (sig) | 1000 | 0.02     | yes      |
| 106018 | WBH(yy)b (sig) | 1200 | 0.02     | yes      |
| 106019 | WBH(yy)b (sig) | 1200 | 0.02     | yes      |
| 106020 | WBH(yy)b (sig) | 1400 | 0.02     | yes      |
| 106021 | WBH(yy)b (sig) | 1400 | 0.02     | yes      |
| 106022 | WBH(yy)b (sig) | 1600 | 0.02     | yes      |
| 106023 | WBH(yy)b (sig) | 1600 | 0.02     | yes      |
| 106024 | WBH(yy)b (sig) | 1800 | 0.02     | yes      |
| 106025 | WBH(yy)b (sig) | 1800 | 0.02     | yes      |
| 106026 | WBH(yy)b (sig) | 2000 | 0.02     | yes      |
| 106027 | WBH(yy)b (sig) | 2000 | 0.02     | yes      |
| 106028 | WBH(yy)b (sig) | 2200 | 0.02     | yes      |
| 106029 | WBH(yy)b (sig) | 2200 | 0.02     | yes      |
| 106030 | WBH(yy)b (sig) | 2400 | 0.02     | yes      |
| 106031 | WBH(yy)b (sig) | 2400 | 0.02     | yes      |


#### VLB Hb nominal samples, including t-channel processes (with reweighting, NLO PDF)

Outdated samples, kept for the sake of documentation: wrong PDF (should be LO PDF and not NLO PDF)

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 103000 | ZBHb (sig)     |  800 | 0.4      | yes      |
| 103001 | ZBHb (sig)     |  800 | 1.0      | yes      |
| 103002 | ZBHb (sig)     | 1000 | 0.4      | yes      |
| 103003 | ZBHb (sig)     | 1000 | 1.0      | yes      |
| 103004 | ZBHb (sig)     | 1200 | 0.4      | yes      |
| 103005 | ZBHb (sig)     | 1200 | 1.0      | yes      |
| 103006 | ZBHb (sig)     | 1400 | 0.4      | yes      |
| 103007 | ZBHb (sig)     | 1400 | 1.0      | yes      |
| 103008 | ZBHb (sig)     | 1600 | 0.4      | yes      |
| 103009 | ZBHb (sig)     | 1600 | 1.0      | yes      |
| 103010 | ZBHb (sig)     | 1800 | 0.4      | yes      |
| 103011 | ZBHb (sig)     | 1800 | 1.0      | yes      |
| 103012 | ZBHb (sig)     | 2000 | 0.4      | yes      |
| 103013 | ZBHb (sig)     | 2000 | 1.0      | yes      |
| 103014 | ZBHb (sig)     | 2200 | 0.4      | yes      |
| 103015 | ZBHb (sig)     | 2200 | 1.0      | yes      |
| 103016 | ZBHb (sig)     | 2400 | 0.4      | yes      |
| 103017 | ZBHb (sig)     | 2400 | 1.0      | yes      |
| 103018 | WBHb (sig)     |  800 | 0.4      | yes      |
| 103019 | WBHb (sig)     |  800 | 1.0      | yes      |
| 103020 | WBHb (sig)     | 1000 | 0.4      | yes      |
| 103021 | WBHb (sig)     | 1000 | 1.0      | yes      |
| 103022 | WBHb (sig)     | 1200 | 0.4      | yes      |
| 103023 | WBHb (sig)     | 1200 | 1.0      | yes      |
| 103024 | WBHb (sig)     | 1400 | 0.4      | yes      |
| 103025 | WBHb (sig)     | 1400 | 1.0      | yes      |
| 103026 | WBHb (sig)     | 1600 | 0.4      | yes      |
| 103027 | WBHb (sig)     | 1600 | 1.0      | yes      |
| 103028 | WBHb (sig)     | 1800 | 0.4      | yes      |
| 103029 | WBHb (sig)     | 1800 | 1.0      | yes      |
| 103030 | WBHb (sig)     | 2000 | 0.4      | yes      |
| 103031 | WBHb (sig)     | 2000 | 1.0      | yes      |
| 103032 | WBHb (sig)     | 2200 | 0.4      | yes      |
| 103033 | WBHb (sig)     | 2200 | 1.0      | yes      |
| 103034 | WBHb (sig)     | 2400 | 0.4      | yes      |
| 103035 | WBHb (sig)     | 2400 | 1.0      | yes      |


#### VLB Hb(yy) nominal samples, including t-channel processes (with reweighting, NLO PDF)

Outdated samples, kept for the sake of documentation: wrong PDF (should be LO PDF and not NLO PDF)

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 104000 | ZBH(yy)b (sig) |  800 | 0.4      | yes      |
| 104001 | ZBH(yy)b (sig) |  800 | 1.0      | yes      |
| 104002 | ZBH(yy)b (sig) | 1000 | 0.4      | yes      |
| 104003 | ZBH(yy)b (sig) | 1000 | 1.0      | yes      |
| 104004 | ZBH(yy)b (sig) | 1200 | 0.4      | yes      |
| 104005 | ZBH(yy)b (sig) | 1200 | 1.0      | yes      |
| 104006 | ZBH(yy)b (sig) | 1400 | 0.4      | yes      |
| 104007 | ZBH(yy)b (sig) | 1400 | 1.0      | yes      |
| 104008 | ZBH(yy)b (sig) | 1600 | 0.4      | yes      |
| 104009 | ZBH(yy)b (sig) | 1600 | 1.0      | yes      |
| 104010 | ZBH(yy)b (sig) | 1800 | 0.4      | yes      |
| 104011 | ZBH(yy)b (sig) | 1800 | 1.0      | yes      |
| 104012 | ZBH(yy)b (sig) | 2000 | 0.4      | yes      |
| 104013 | ZBH(yy)b (sig) | 2000 | 1.0      | yes      |
| 104014 | ZBH(yy)b (sig) | 2200 | 0.4      | yes      |
| 104015 | ZBH(yy)b (sig) | 2200 | 1.0      | yes      |
| 104016 | ZBH(yy)b (sig) | 2400 | 0.4      | yes      |
| 104017 | ZBH(yy)b (sig) | 2400 | 1.0      | yes      |
| 104018 | WBH(yy)b (sig) |  800 | 0.4      | yes      |
| 104019 | WBH(yy)b (sig) |  800 | 1.0      | yes      |
| 104020 | WBH(yy)b (sig) | 1000 | 0.4      | yes      |
| 104021 | WBH(yy)b (sig) | 1000 | 1.0      | yes      |
| 104022 | WBH(yy)b (sig) | 1200 | 0.4      | yes      |
| 104023 | WBH(yy)b (sig) | 1200 | 1.0      | yes      |
| 104024 | WBH(yy)b (sig) | 1400 | 0.4      | yes      |
| 104025 | WBH(yy)b (sig) | 1400 | 1.0      | yes      |
| 104026 | WBH(yy)b (sig) | 1600 | 0.4      | yes      |
| 104027 | WBH(yy)b (sig) | 1600 | 1.0      | yes      |
| 104028 | WBH(yy)b (sig) | 1800 | 0.4      | yes      |
| 104029 | WBH(yy)b (sig) | 1800 | 1.0      | yes      |
| 104030 | WBH(yy)b (sig) | 2000 | 0.4      | yes      |
| 104031 | WBH(yy)b (sig) | 2000 | 1.0      | yes      |
| 104032 | WBH(yy)b (sig) | 2200 | 0.4      | yes      |
| 104033 | WBH(yy)b (sig) | 2200 | 1.0      | yes      |
| 104034 | WBH(yy)b (sig) | 2400 | 0.4      | yes      |
| 104035 | WBH(yy)b (sig) | 2400 | 1.0      | yes      |


#### nominal samples (with reweighting)

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

#### mass closure test


| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 100100 | ZBHb (sigonly) | 1300 | 1.0      | no       |
| 100101 | ZBHb (sigbar)  | 1300 | 1.0      | no       |
| 100102 | WBHb (sig)     | 1300 | 1.0      | no       |
| 100103 | ZBHb (sigonly) | 1900 | 1.0      | no       |
| 100104 | ZBHb (sigbar)  | 1900 | 1.0      | no       |
| 100105 | WBHb (sig)     | 1900 | 1.0      | no       |


#### coupling closure test


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



### validation of WBHb and ZBHb job options with t-channel processes

NOTE: use release 21.6.57 for these to be consistent with Avik Roy's setup!

#### nominal samples


| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 102000 | ZBHb (sig)     | 1000 | 0.4      | yes      |
| 102001 | ZBHb (sig)     | 1000 | 1.0      | yes      |
| 102002 | WBHb (sig)     | 1000 | 0.4      | yes      |
| 102003 | WBHb (sig)     | 1000 | 1.0      | yes      |
| 102004 | ZBHb (sig)     | 1400 | 0.4      | yes      |
| 102005 | ZBHb (sig)     | 1400 | 1.0      | yes      |
| 102006 | WBHb (sig)     | 1400 | 0.4      | yes      |
| 102007 | WBHb (sig)     | 1400 | 1.0      | yes      |
| 102008 | ZBHb (sig)     | 2000 | 0.4      | yes      |
| 102009 | ZBHb (sig)     | 2000 | 1.0      | yes      |
| 102010 | WBHb (sig)     | 2000 | 0.4      | yes      |
| 102011 | WBHb (sig)     | 2000 | 1.0      | yes      |


#### mass closure test


| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 102100 | ZBHb (sig)     |  900 | 0.4      | no       |
| 102101 | ZBHb (sig)     |  900 | 1.0      | no       |
| 102102 | WBHb (sig)     |  900 | 0.4      | no       |
| 102103 | WBHb (sig)     |  900 | 1.0      | no       |
| 102104 | ZBHb (sig)     | 1300 | 0.4      | no       |
| 102105 | ZBHb (sig)     | 1300 | 1.0      | no       |
| 102106 | WBHb (sig)     | 1300 | 0.4      | no       |
| 102107 | WBHb (sig)     | 1300 | 1.0      | no       |
| 102108 | ZBHb (sig)     | 1900 | 0.4      | no       |
| 102109 | ZBHb (sig)     | 1900 | 1.0      | no       |
| 102110 | WBHb (sig)     | 1900 | 0.4      | no       |
| 102111 | WBHb (sig)     | 1900 | 1.0      | no       |


#### coupling closure test


| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 102200 | ZBHb (sig)     | 1400 | 0.1      | no       |
| 102201 | WBHb (sig)     | 1400 | 0.1      | no       |
| 102202 | ZBHb (sig)     | 1400 | 0.2      | no       |
| 102203 | WBHb (sig)     | 1400 | 0.2      | no       |
| 102204 | ZBHb (sig)     | 1400 | 0.3      | no       |
| 102205 | WBHb (sig)     | 1400 | 0.3      | no       |
| 102206 | ZBHb (sig)     | 1400 | 0.5      | no       |
| 102207 | WBHb (sig)     | 1400 | 0.5      | no       |
| 102208 | ZBHb (sig)     | 1400 | 0.7      | no       |
| 102209 | WBHb (sig)     | 1400 | 0.7      | no       |
| 102210 | ZBHb (sig)     | 1400 | 0.9      | no       |
| 102211 | WBHb (sig)     | 1400 | 0.9      | no       |
| 102212 | ZBHb (sig)     | 1400 | 1.1      | no       |
| 102213 | WBHb (sig)     | 1400 | 1.1      | no       |
| 102214 | ZBHb (sig)     | 1400 | 1.3      | no       |
| 102215 | WBHb (sig)     | 1400 | 1.3      | no       |




### validation of WBHb and ZBHb job options with t-channel processes (outdated)

#### nominal samples


| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 101000 | ZBHb (sigonly) | 1000 | 1.0      | yes      |
| 101001 | ZBHb (sigbar)  | 1000 | 1.0      | yes      |
| 101002 | WBHb (sig)     | 1000 | 1.0      | yes      |
| 101003 | ZBHb (sigonly) | 1400 | 1.0      | yes      |
| 101004 | ZBHb (sigbar)  | 1400 | 1.0      | yes      |
| 101005 | WBHb (sig)     | 1400 | 1.0      | yes      |
| 101006 | ZBHb (sigonly) | 2000 | 1.0      | yes      |
| 101007 | ZBHb (sigbar)  | 2000 | 1.0      | yes      |
| 101008 | WBHb (sig)     | 2000 | 1.0      | yes      |


#### mass closure test

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 101100 | ZBHb (sigonly) |  900 | 1.0      | no       |
| 101101 | ZBHb (sigbar)  |  900 | 1.0      | no       |
| 101102 | WBHb (sig)     |  900 | 1.0      | no       |
| 101103 | ZBHb (sigonly) | 1300 | 1.0      | no       |
| 101104 | ZBHb (sigbar)  | 1300 | 1.0      | no       |
| 101105 | WBHb (sig)     | 1300 | 1.0      | no       |
| 101106 | ZBHb (sigonly) | 1900 | 1.0      | no       |
| 101107 | ZBHb (sigbar)  | 1900 | 1.0      | no       |
| 101108 | WBHb (sig)     | 1900 | 1.0      | no       |


#### coupling closure test

| DSID   | mode           | mass | coupling | reweight |
| ------ | -------------- | ---- | -------- | -------- |
| 101110 | ZBHb (sigonly) | 1400 | 0.1      | no       |
| 101111 | ZBHb (sigbar)  | 1400 | 0.1      | no       |
| 101112 | WBHb (sig)     | 1400 | 0.1      | no       |
| 101113 | ZBHb (sigonly) | 1400 | 0.4      | no       |
| 101114 | ZBHb (sigbar)  | 1400 | 0.4      | no       |
| 101115 | WBHb (sig)     | 1400 | 0.4      | no       |
| 101116 | ZBHb (sigonly) | 1400 | 1.3      | no       |
| 101117 | ZBHb (sigbar)  | 1400 | 1.3      | no       |
| 101118 | WBHb (sig)     | 1400 | 1.3      | no       |
| 101119 | ZBHb (sigonly) | 1400 | 1.6      | no       |
| 101120 | ZBHb (sigbar)  | 1400 | 1.6      | no       |
| 101121 | WBHb (sig)     | 1400 | 1.6      | no       |

