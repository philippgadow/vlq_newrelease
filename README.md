## Development of the VLQ job option for Atlas MC Generation releases 21.6.23 and later

The reweighting module doesn't work properly in CC7 releases, therefore we use the most recent SL6 release, which is `21.2.48`.

### Run this example quickly

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

