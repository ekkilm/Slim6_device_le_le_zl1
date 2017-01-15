# Copyright (C) 2009 The Android Open Source Project
# Copyright (c) 2011-2013, The Linux Foundation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Emit commands needed for QCOM devices during OTA installation
(installing the radio image)."""

import common
import re

commonImages = {}
x720Images = {}
x727Images = {}

# Parse filesmap file containing firmware residing places
def LoadFilesMap(zip, name="RADIO/filesmap"):
  try:
    data = zip.read(name)
  except KeyError:
    print "Warning: could not find %s in %s." % (name, zip)
    data = ""
  d = {}
  for line in data.split("\n"):
    line = line.strip()
    if not line or line.startswith("#"):
      continue
    pieces = line.split()
    if not (len(pieces) == 2):
      raise ValueError("malformed filesmap line: \"%s\"" % (line,))
    d[pieces[0]] = pieces[1]
  return d


# Read firmware images from target files zip
def GetRadioFiles(z):
  out = {}
  for info in z.infolist():
    f = info.filename
    if f.startswith("RADIO/") and (f.__len__() > len("RADIO/")):
      fn = f[6:]
      if fn.startswith("filesmap"):
        continue
      data = z.read(f)
      out[fn] = common.File(f, data)
  return out


# Get firmware residing place from filesmap
def GetFileDestination(fn, filesmap):
  # if file is encoded disregard the .enc extention
  if fn.endswith('.enc'):
    fn = fn[:-4]

  # If full filename is not specified in filesmap get only the name part
  # and look for this token
  if fn not in filesmap:
    fn = fn.split(".")[0] + ".*"
    if fn not in filesmap:
      print "warning radio-update: '%s' not found in filesmap" % (fn)
      return None
  return filesmap[fn]


# Separate image types as each type needs different handling
def SplitFwTypes(files):
  common = {}
  x720 = {}
  x727 = {}

  for f in files:

    if "720" in f:
      x720[f] = files[f]
    elif "727" in f:
      x727[f] = files[f]
    else:
      common[f] = files[f]
	
  return common, x720, x727


# Prepare radio-update files and verify them
def OTA_VerifyEnd(info, api_version, target_zip, source_zip=None):
  if api_version < 3:
    print "warning radio-update: no support for api_version less than 3"
    return False

  print "Loading radio filesmap..."
  filesmap = LoadFilesMap(target_zip)
  if filesmap == {}:
    print "warning radio-update: no or invalid filesmap file found"
    return False

  print "Loading radio target..."
  tgt_files = GetRadioFiles(target_zip)
  if tgt_files == {}:
    print "warning radio-update: no radio images in input target_files"
    return False

  src_files = None
  if source_zip is not None:
    print "Loading radio source..."
    src_files = GetRadioFiles(source_zip)

  update_list = {}

  print "Preparing radio-update files..."
  for fn in tgt_files:
    dest = GetFileDestination(fn, filesmap)
    if dest is None:
      continue

    tf = tgt_files[fn]
    f = "firmware-update/" + fn
    common.ZipWriteStr(info.output_zip, f, tf.data)
    update_list[f] = dest

  global commonImages
  global x720Images
  global x727Images
  commonImages, x720Images, x727Images = SplitFwTypes(update_list)

  return True


def FullOTA_Assertions(info):
  #TODO: Implement device specific asserstions.
  return


def IncrementalOTA_Assertions(info):
  #TODO: Implement device specific asserstions.
  return


def IncrementalOTA_VerifyEnd(info):
 OTA_VerifyEnd(info, info.target_version, info.target_zip, info.source_zip)
 return


# This function handles only non-HLOS whole partition images
def InstallRawImage(script, f, dest):
  script.AppendExtra('package_extract_file("%s", "%s");' % (f, dest))
  return


# This function handles only non-HLOS bin images
def InstallBinImages(script, files):
  for f in files:
    dest = files[f]
    InstallRawImage(script, f, dest)
  return


def OTA_InstallEnd(info):
  print "Applying radio-update script modifications..."
  info.script.Print("Patching common fw images...")

  if commonImages != {}:
    InstallBinImages(info.script, commonImages)

  info.script.AppendExtra('ifelse((sha1_check(read_file("EMMC:/dev/block/bootdevice/by-name/devinfo:4096:d7a8e93f24493ee2bef82367ae6d6effdc074bcb")) != ""),(')
  info.script.Print("Patching X727 firmware images...")
  if x727Images != {}:
    InstallBinImages(info.script, x727Images)
  info.script.AppendExtra('),(')
  info.script.Print("Patching X720 firmware images...")
  if x720Images != {}:
    InstallBinImages(info.script, x720Images)
  info.script.AppendExtra('));')

  info.script.Print("DONE")

  return


def FullOTA_InstallEnd_MMC(info):
  if OTA_VerifyEnd(info, info.input_version, info.input_zip):
    OTA_InstallEnd(info)
  return


def FullOTA_InstallEnd_MTD(info):
  print "warning radio-update: radio update for NAND devices not supported"
  return


def FullOTA_InstallEnd(info):
  FullOTA_InstallEnd_MMC(info)
  return

def IncrementalOTA_InstallEnd_MMC(info):
  OTA_InstallEnd(info)
  return


def IncrementalOTA_InstallEnd_MTD(info):
  print "warning radio-update: radio update for NAND devices not supported"
  return

def IncrementalOTA_InstallEnd(info):
  IncrementalOTA_InstallEnd_MMC(info)
  return
