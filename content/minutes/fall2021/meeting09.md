---
title: File systems and storage
date: 2021-11-18
tags: minutes,minutes2021
author: Steven Whitaker
template: minutes
---
# File systems and storage

## introduction

Storage:

* Save large files like code, binary files, movies, etc.

* HDDs, SSDs, magnetic tape

Memory:

* Cache data

* Any type of RAM: SRAM, SDRAM, VRAM, etc.

Swap storage is fake memory that is actually storage, but pretends to be memory. You _need_ a partition for this, and so you type`mkswap /dev/sda2` to make the partition a swap file, then `swapon /dev/sdXN` to enable swap. Run `top` or `htop` to see your swap and memory usage.

This talk is all about storage, not memory.


## Looking at things
 
[`lsblk`](https://linux.die.net/man/8/lsblk) "list block devices", shows partitions

[`blkid`](https://linux.die.net/man/8/blkid) "block device ids", shows storage UUIDs

[`lsblk -f`](https://linux.die.net/man/8/lsblk) gives same info as blkid

[`fdisk -l`](https://linux.die.net/man/8/fdisk) list all your storage media

[`df -h`](https://linux.die.net/man/1/df) shows you the free space on each drive.

* TIP: When trying to save space, use `du -sh *` to look at folder sizes and work your way down to delete the shit that's not needed.

## Mounting systems

### [`findmnt`](https://linux.die.net/man/8/findmnt)  
Finds all the mounts in your system
 
Anything in [`/sys`](https://www.thegeekdiary.com/understanding-the-sysfs-file-system-in-linux/) or [`/proc`](https://www.geeksforgeeks.org/proc-file-system-linux/) are kernel stuff. The kernel opens up files for you to look at. I don't know anything else about it! Look it up yourself, cuz I don't know what it means. It's not important to this talk.

`/dev` is your stuff... mostly. Here's some links to things I don't care about: [`/dev/pts`](https://unix.stackexchange.com/questions/93531/). [`/dev/shm`](http://www.csl.mtu.edu/cs3331.ck/www/Home.html). [`/dev/mqueue`](https://users.pja.edu.pl/~jms/qnx/help/watcom/clibref/mq_overview.html). 

### Actually mounting shit

`/dev/sdX` are your drives! `/dev/sda` is your first, `/dev/sdb` is your second, etc.

You mount partitions.

`mount /dev/sdb1 /mnt`

`umount /mnt`

If you plug in a USB and you want to access it, use `lsblk -f`, then `mount /dev/sdXN /mnt` or wherever you want the USB files. Then, `umount /mnt` to safely remove.

(NOTE: if you're doing this on VirtualBox, your virtual drives have no format, so just run `mkfs.ext4 /dev/sdX` for every drive and you can mount them.) 

## Setting up the drives

`fdisk /dev/sda`

`g` sets disk as GUID Partition Table (GPT). This supports UEFI and up to 8 ZB (it goes GB, TB, PB, EB, ZB.. so a lot).

`o` Sets disk as a Master Boot Record [MBR](https://www.youtube.com/watch?v=t6KFfYdNPh8). This supports legacy boot, NO UEFI, and up to 2 TB size. Easier to set up than GPT.

`n` new partition

`p` primary partition (I have never used an extended partition).

`w` Writes what you've done

`t` Sets the file type. Key ones are: (MBR) `82=Linux swap`, `83=Linux`, `fd=RAID`, `8e=LVM`. (GPT) `19=Linux swap`, `20=Linux`, `29=Linux RAID`, `30=Linux LVM`, `1=EFI`. The default on `fdisk` is usually `Linux`.

### [Standard setup](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks#Partitioning_the_disk_with_GPT_for_UEFI) demo

```text
Device        Start      End  Sectors  Size Type
/dev/sda1      2048   526335   524288  256M EFI System
/dev/sda2    526336  2623487  2097152    1G Linux swap
/dev/sda3   2623488 19400703 16777216    8G Linux filesystem
```

I would recommend 512M for the EFI system nowadays on Gentoo or systems that let you do this manually. Your `/boot` will get too clustered if you don't. I need to clean out `/boot` every 3rd kernel update and it can get annoying.

### Logical volume management (LVM)
```text
                   /---------------\ /-----\ /--------\
Logical volumes    | movies         | code  |  home   |
                   \---------------/ \-----/ \--------/

                   /----------------------------------\
Volume groups      |               lvm                |
                   \----------------------------------/

                   /----------\ /---------\ /----------\
Physical volumes   | /dev/sda1 | /dev/sdb1 | /dev/sdc1 |
                   \----------/ \---------/ \----------/
```

LVM pools multiple drives together in a single logical drive and let's you split them arbitrarily afterwards.

```text
Device        Start      End  Sectors  Size Type
/dev/sda1      2048   526335   524288  256M EFI System
/dev/sda2    526336  2623487  2097152    1G Linux swap
/dev/sda3   2623488 19400703 16777216    8G Linux LVM
/dev/sdb1   2623488 19400703 16777216    8G Linux LVM
/dev/sdc1   2623488 19400703 16777216    8G Linux LVM
```

Format the volume: `pvcreate /dev/sdX`.

#### View the LVM settings
`pvdisplay` to view physical volumes, `vgdisplay` to view your volume groups. `lvdisplay <volume_name>` to view your partitions in the volume group. [This](https://askubuntu.com/questions/417642/) stackoverflow answer helps explain the differences and gives two good links that helped me understand what was going on, [technical](https://www.howtoforge.com/linux_lvm) and [practical](https://en.wikipedia.org/wiki/Logical_Volume_Manager_%28Linux%29).

#### Main commands

Let us assume we have `/dev/sda3`, `/dev/sdb1/`, `/dev/sdc1`, 3 drives ready to be added to an LVM group. We will name our volume group "lvm" because why not? This will create a folder, `/dev/lvm`. First, add your drives to the physical volume list:

`pvcreate /dev/sda3 /dev/sdb1 /dev/sdc1`

Then create a volume group with them all:

`vgcreate lvm /dev/sda3 /dev/sdb1 /dev/sdc1`

Say you want your home directory in a different volume: 

`lvcreate -L 30G lvm -n lv_home`

Then use the rest of the logical volume:

`lvcreate -l 100%FREE lvm -n lv_root`

You got a new hard drive? Cool. It's `/dev/sdd1`. Add it to the volume group:

`vgextend lvm /dev/sdd1`

You ran out of storage in a volume group? Resize it:

`lvextend -L 35G /dev/lvm/lv_home`

`lvreduce` to drop the size. This will probably break data.

### RAID

[RAID](https://wiki.gentoo.org/wiki/User:SwifT/Complete_Handbook/Software_RAID) is for data protection. This is _not_ a backup. It is just for protection. Instead of one drive dying and you lose all your data, you can use a RAID system so you have protection against it dying.

Instead of a table of the different RAID systems, here's a [list of them](https://www.cru-inc.com/table-raid-levels/). I'm going to assume we use RAID 1 or RAID 10.

RAID is done all under `mdadm`. It's straightforward comapred to LVM.

`mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1`

`mdadm --create /dev/md0 --level=10 --raid-devices=2 /dev/sdb1 /dev/sdc1`


### ZFS

You can use LVM and RAID by manually making sure you don't go over 50% or whatever RAID you want requires, then using `mdadm` on your logical volumes. Or just use ZFS to create a pool. Even less work.

`zpool create pool /dev/sdb /dev/sdc`

RAID 1:

`zpool create pool mirror /dev/sdb /dev/sdc`

RAID 10:

`zpool create pool mirror /dev/sdb /dev/sdc mirror /dev/sdd /dev/sde`


Check out what you did:

`zpool status`

Here is our Linux mirrors configuration:

```text
  pool: lug
 state: ONLINE
config:

	NAME                       STATE     READ WRITE CKSUM
	lug                        ONLINE       0     0     0
	  mirror-0                 ONLINE       0     0     0
	    label/lug-HGST-4TB-01  ONLINE       0     0     0
	    label/lug-HGST-4TB-02  ONLINE       0     0     0
	  mirror-1                 ONLINE       0     0     0
	    label/lug-HGST-4TB-03  ONLINE       0     0     0
	    label/lug-HGST-4TB-04  ONLINE       0     0     0
	  mirror-2                 ONLINE       0     0     0
	    label/lug-HGST-4TB-05  ONLINE       0     0     0
	    label/lug-HGST-4TB-06  ONLINE       0     0     0
	  mirror-3                 ONLINE       0     0     0
	    label/lug-HGST-4TB-07  ONLINE       0     0     0
	    label/lug-HGST-4TB-08  ONLINE       0     0     0
	  mirror-4                 ONLINE       0     0     0
	    label/lug-HGST-4TB-09  ONLINE       0     0     0
	    label/lug-HGST-4TB-10  ONLINE       0     0     0

errors: No known data errors

  pool: zroot
 state: ONLINE
  scan: scrub repaired 0B in 00:01:47 with 0 errors on Sun Sep 26 16:42:05 2021
config:

	NAME        STATE     READ WRITE CKSUM
	zroot       ONLINE       0     0     0
	  mirror-0  ONLINE       0     0     0
	    da10p3  ONLINE       0     0     0
	    da11p3  ONLINE       0     0     0

errors: No known data errors
```

## fstab

Automatically mount your file systems at start up and tells you which file system corresponds to which drive, etc.

`<fs> <mountpoint> <type> <opts> <dump/pass>`.

[It is recommended](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/System#Creating_the_fstab_file) you use UUIDs for non-LVM non-ZFS. [It is recommended](https://xan.manning.io/2017/05/29/best-practice-for-mounting-an-lvm-logical-volume-with-etc-fstab.html) you use the device mapper symlink for LVM or ZFS. I am not smart enough to know the benefits for either.

Options are seen in "Filesystem independent mount options" and "Filesystem dependent mount options" in the [mount](https://linux.die.net/man/8/mount)(8) man page. I'd just use `defaults`. Use `_netdev` for a network drive (_cough_ David _cough_).

The numbers at the end are not too necessary, but read [the man page](https://linux.die.net/man/5/fstab) on the 5th and 6th fields if you really want to know. [Gentoo](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/System#Creating_the_fstab_file) recommends having `/` at `0 1` and everything else as `0 2`.

```text
/dev/lvm/lv_root / ext4 defaults 0 1
/dev/lvm/lv_home /home ext4 defaults 0 2
UUID=46ef4b37-b2bc-4a3a-b821-604c9fb64787 /boot ext4 defaults,noatime 0 2
UUID=61518d0a-1a81-4936-85e0-6bb7e1d69155 none swap sw 0 0
