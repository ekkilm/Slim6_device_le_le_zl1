Device configuration for LeEco Le Pro 3.

www.teamsuperluminal.org

Needed packages (ubuntu 15.x)

sudo apt-get install bison build-essential curl flex git gnupg gperf libesd0-dev liblz4-tool libncurses5-dev libsdl1.2-dev libwxgtk2.8-dev libxml2 libxml2-utils lzop maven openjdk-7-jdk openjdk-7-jre pngcrush schedtool squashfs-tools xsltproc zip zlib1g-dev g++-multilib gcc-multilib lib32ncurses5-dev lib32readline-gplv2-dev lib32z1-dev realpath

Init repo

repo init -u git://github.com/SlimRoms/platform_manifest.git -b mm6.0

Sync

repo sync -j4

Copy device/le/le_zl1/local_manifests/le_zl1.xml to $ANDROID_BUILD_TOP/.repo/local_manifests/

cp ./device/le/le_zl1/local_manifests/le_zl1.xml $ANDROID_BUILD_TOP/.repo/local_manifests/

Sync

repo sync -j4

Before build unzip radio files! 
device/le/le_zl1/radio/radio.zip in radio folder

Build

lunch slim_le_zl1-userdebug brunch slim_le_zl1-userdebug
