#!/system/bin/sh

if [ ! -f /data/data/com.uei.quicksetsdk.letv/files/Settings ]; then
	mkdir -p /data/data/com.uei.quicksetsdk.letv/files
	cp /system/etc/UEISettings /data/data/com.uei.quicksetsdk.letv/files/Settings
	chown system:system /data/data/com.uei.quicksetsdk.letv/files/Settings
	chmod 777 /data/data/com.uei.quicksetsdk.letv/
	chmod 777 /data/data/com.uei.quicksetsdk.letv/files
	chmod 666 /data/data/com.uei.quicksetsdk.letv/files/Settings
fi

