#!/bin/bash
source  /root/.bash_profile
syncDir="/data0/syncdata"
date=`date +'%Y-%m-%d'`
targetDir="/opt/db_backup_nfs/${date}"
binlogDir="/data0/binlog/"
log="$syncDir/tools/check_mysql_backup/log/${date}_backupLog"

### check nfs mount
df -h|grep "/opt/db_backup_nfs"
if [[ $? -ne 0 ]];then
	echo "### can't found mount point : /opt/db_backup_nfs, remount nfs!" >> $log
	mount -a
fi

### check disk space
availableSize=`df -m /opt/db_backup_nfs/|grep /db_backup_nfs|awk '{print $3}'`
dbSize=`du -s --block-size=1024k /data0/db_data/mysql |awk '{print $1}'`
if [[ $availableSize -le $dbSize ]];then
        echo "### Available disk space is not enough!!!"
        exit
fi


function cp_sync()
{
	t_sync="${targetDir}/syncdata"
	sync_data="${targetDir}/syncdata/data"
	[ -d $sync_data ] || mkdir -p $sync_data
	echo "$(date +'%Y-%m-%d %H:%M:%S'), Start to copy syncdata..." >> $log
	cd $syncDir && ls |grep "py$"|xargs -i cp {} $t_sync &&
	cp -ra tools $t_sync &&
	cd data && ls |egrep 'record_|lock_'|xargs -i cp {} $sync_data
	return $?
}

################################
# $0 days 
# cp_binlog 7
################################
function cp_binlog()
{
	days=$1
	echo "$(date +'%Y-%m-%d %H:%M:%S'), Start to copy binlog ..." >> $log
	t_binlog="${targetDir}/binlog"
	[ -d $t_binlog ] || mkdir -p $t_binlog
	find $binlogDir -type f -ctime -${days}|xargs -i cp {} $t_binlog
	return $?
}

function cp_mysql()
{
	echo "$(date +'%Y-%m-%d %H:%M:%S'), Start to copy mysql databases ..." >> $log
	/etc/init.d/mysql stop
	cp -ra /data0/db_data/mysql ${targetDir}/ &&
	/etc/init.d/mysql start
	return $?
}


###############################
# copy syncdata/binlog/myslq dir
###############################

### stop rtsync
RTSYNC_HOME="/data0/rtsync-1.0.0"
cd $RTSYNC_HOME && sh bin/rtsyncshutdown
sleep 10
ip=`ifconfig |grep -A 1 em1|grep 'inet addr' |awk '{print $2}'|awk -F: '{print $2}'`
if [[ $ip == "10.10.1.163" ]];then
        echo "$(date +'%Y-%m-%d %H:%M:%S'), Start backup on ${ip}..." >>  $log
        #cp_sync && cp_binlog 5 && cp_mysql
        cp_sync && cp_mysql
        [[ $? -eq 0 ]] && echo "Backup done..." >>  $log || echo "Backup failed..." >>  $log
else
        echo "$(date +'%Y-%m-%d %H:%M:%S'), Start backup on ${ip}..." >>  $log
        #cp_sync && cp_binlog 1 && cp_mysql
        cp_sync && cp_mysql
        [[ $? -eq 0 ]] && echo "Backup done..." >>  $log || echo "Backup failed..." >>  $log
fi

### start rtsync after backup done
echo "start rtsyncSvc ..." >> $log
cd $RTSYNC_HOME && 
nohup sh bin/rtsyncSvc -l true 2>&1 > nohup.out &
echo "$(date +'%Y-%m-%d %H:%M:%S'), backup ended!" >>  $log
