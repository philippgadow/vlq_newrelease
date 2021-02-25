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

