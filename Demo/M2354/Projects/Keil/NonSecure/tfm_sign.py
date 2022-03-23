#-------------------------------------------------------------------------------
# Copyright (c) 2019-2021 Arm Limited. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#-------------------------------------------------------------------------------

import subprocess
import sys
import getopt
import os.path
from pathlib import Path
import runpy
import platform

NS_BIN = 0
TFM_DIR = 0
PLATFORM = 0
VERSION = 0
BL2_BIN_OFFSET = 0
SIGN_BIN_OFFSET = 0
FLASH_LAYOUT = 0
SIGN_BIN_SIZE = 0x0
tfm_directory = 0

def usageDescription():
    print("Usage: tfm_rtos_mcuboot_integrate.py <-n path_to_ns_bin> <-t path_to_tfm> <-p xxx>\n \
      -n, --ns_bin     The path of non-secure bin file. Absolute path and relative path to the execute path are accepted. <mandatory>\n \
      -t, --tfm_dir    The path of TFM base folder. Absolute path and relative path to the execute path are accepted. <mandatory>\n \
      -p, --platform   The target platform. 'MUSCA_B' is supported. <mandatory>\n")

def getInputArg():
    try:
        opts,args = getopt.getopt(sys.argv[1:],'-n:-t:-p:',['ns_bin=','tfm_dir=','platform='])
        if len(opts) != 3:
            usageDescription()
            sys.exit(2)
        for opt_name,opt_value in opts:
            if opt_name in ('-n','--ns_bin'):
                global NS_BIN
                NS_BIN = opt_value
                print(NS_BIN)
            if opt_name in ('-t','--tfm_dir'):
                global TFM_DIR
                TFM_DIR = opt_value
                print(TFM_DIR)
            if opt_name in ('-p','--platform'):
                global PLATFORM
                PLATFORM = opt_value
                print(PLATFORM)
    except getopt.GetoptError as err:
        print (str(err))
        usageDescription()
        sys.exit(2)

''' Check the input arguments' validity. 0, 1, 2 is returned respectivily for invalid input case,
    valid input and file found case, valid input but file no found case.'''
def checkInputArgValid():
    global FLASH_LAYOUT
    global SIGN_BIN_SIZE
    global BL2_BIN_OFFSET
    global SIGN_BIN_OFFSET
    global NS_BIN
    global TFM_DIR
    global TFM_BUILD_DIR
    valid_param = 0
    NS_BIN = os.path.abspath(NS_BIN)
    ns_bin_path = Path(NS_BIN)
    if not ns_bin_path.is_file():
        print(NS_BIN, "does not exist!")
        valid_param = 0
        return valid_param
    TFM_DIR = os.path.abspath(TFM_DIR)
    TFM_BUILD_DIR = os.path.join(TFM_DIR, 'out\\build\\m2354')
    tfm_directory = Path(TFM_DIR)
    if not tfm_directory.is_dir():
        print(tfm_directory, "does not exit!")
        valid_param = 0
        return valid_param
    #if PLATFORM == "ARM/MUSCA_B1/SSE_200":
    if PLATFORM == "nuvoton\\m2354":
        SIGN_BIN_SIZE = 0x90000
        BL2_BIN_OFFSET = 0x0000000
        SIGN_BIN_OFFSET = 0x10070000
    else:
        print(PLATFORM, "is not supported!")
        valid_param = 0
        return valid_param

    print("BL2 binary offset is hardcode at", BL2_BIN_OFFSET)
    print("Sign binary offset is hardcode at", SIGN_BIN_OFFSET)
    valid_param = 1
    return valid_param

def getTFMFullBin():
    global TFM_DIR
    SCRIPTS_DIR=os.path.join(TFM_DIR, 'bl2', 'ext', 'mcuboot', 'scripts')
    assemble_path = os.path.join(SCRIPTS_DIR, 'assemble.py')
    assemble_file = Path(assemble_path)
    secure_flash_layout_file = os.path.join(TFM_BUILD_DIR, 'bl2', 'ext', 'mcuboot','CMakeFiles','signing_layout_s.dir', 'signing_layout_s.o')		
    if not assemble_file.is_file():
        print("Cannot find", ASSEMBLE_PY)
        sys.exit(2)
    tfm_s_bin = os.path.join(TFM_BUILD_DIR, 'install', 'outputs', PLATFORM, "tfm_s.bin")
    cmd = 'python {path} --layout {flash_path} -s {tfm_s_bin_arg} -n {ns_bin} -o {tfm_full_bin}'
    p_cmd = cmd.format(path=assemble_file, flash_path=secure_flash_layout_file, tfm_s_bin_arg = 'tfm_secure_sign.bin', ns_bin=r'non_secure_sign.bin', tfm_full_bin=r'tfm_s_ns_signed.bin')
    print("666666666")
    print(p_cmd)
    subprocess.call(p_cmd, shell=True)


def getSignsecureBin():
    global TFM_DIR
    IMGTOOL_PY_PATH = os.path.join(TFM_DIR, 'bl2', 'ext', 'mcuboot', 'scripts', 'wrapper', 'wrapper.py')
    imgtool_py_file = Path(IMGTOOL_PY_PATH)	
    secure_image_bin = os.path.join(TFM_BUILD_DIR, 'install', 'outputs','tfm_s.bin')
    pem = os.path.join(TFM_DIR, 'bl2', 'ext', 'mcuboot', 'root-rsa-2048.pem')
    value = 0x400
    secure_flash_layout_file = os.path.join(TFM_BUILD_DIR, 'bl2', 'ext', 'mcuboot','CMakeFiles','signing_layout_s.dir', 'signing_layout_s.o')	
    cmd = 'python {path} -k {pem_path} --public-key-format {key_hash} -v {version} --layout {flash_path} --align 4 --pad --pad-header -H {value_400} -s {count} --confirm {tfm_secure_bin} {tfm_sign_bin}'
    print("SIGN_BIN_SIZE =", SIGN_BIN_SIZE)
    print(cmd)
    version_value = r'0.0.0+1'
    dependency_version = r'"(1,0.0.0+0)"'
    p_cmd = cmd.format(path=imgtool_py_file, pem_path=pem, key_hash='hash', version=version_value, flash_path=secure_flash_layout_file, value_400=value, dependency_info=dependency_version, count='auto', tfm_secure_bin=secure_image_bin, tfm_sign_bin= r'tfm_secure_sign.bin')
    print(p_cmd)
    subprocess.call(p_cmd, shell=True)

def getSignnon_secureBin():
    global TFM_DIR
    IMGTOOL_PY_PATH = os.path.join(TFM_DIR, 'bl2', 'ext', 'mcuboot', 'scripts', 'wrapper', 'wrapper.py')
    imgtool_py_file = Path(IMGTOOL_PY_PATH)	
    secure_image_bin = os.path.join(TFM_BUILD_DIR, 'install', 'outputs', PLATFORM, 'tfm_s.bin')
    pem = os.path.join(TFM_DIR, 'bl2', 'ext', 'mcuboot', 'root-rsa-2048_1.pem')
    value = 0x400
    flash_layout_file = os.path.join(TFM_BUILD_DIR, 'bl2', 'ext', 'mcuboot','CMakeFiles','signing_layout_ns.dir', 'signing_layout_ns.o')		
    cmd = 'python {path} -k {pem_path} --public-key-format {key_hash} -v {version} --layout {flash_path} --align 4 --pad --pad-header -H {value_400} -d {dependency_info} -s {count} --confirm {non_secure_bin} {tfm_sign_bin}'
    #cmd = 'python {path} -k {pem_path} --public-key-format {key_hash} -v {version} --layout {flash_path} --align 4 --pad --pad-header -H {value_400} -d {dependency_info} -s {count}  {non_secure_bin} {tfm_sign_bin}'
    print(cmd)
    print("nonsecure image")
    version_value = r'0.0.0+3'
    dependency_version = r'"(0,0.0.0+0)"'
	
    p_cmd = cmd.format(path=imgtool_py_file, pem_path=pem, key_hash='hash', version=version_value, flash_path=flash_layout_file, value_400=value, dependency_info=dependency_version, count='auto', non_secure_bin=NS_BIN, tfm_sign_bin= r'non_secure_sign.bin')
    print(p_cmd)
    subprocess.call(p_cmd, shell=True)

def getHex():
    global BL2_BIN_OFFSET
    global SIGN_BIN_OFFSET
    if platform.system() == "Windows":
        srec_cat_bin = 'srec_cat.exe'
    else:
        srec_cat_bin = 'srec_cat'
    tfm_hex = "rtos_tfm_" + 'MUSCA_B1' + ".hex"
    mcuboot_bin = os.path.join(TFM_BUILD_DIR, 'install', 'outputs', PLATFORM, 'bl2.bin')
    tfm_sign_bin = r'tfm_s_ns_signed.bin'
    cmd = srec_cat_bin + ' {mcuboot_bin_placeholer} -Binary -offset {bl2_bin_offset_placeholer} {tfm_sign_bin_placeholer}  -Binary -offset {sign_bin_offset_placeholer} -o {tfm_hex_placeholder} -Intel'
    p_cmd = cmd.format(mcuboot_bin_placeholer=mcuboot_bin, bl2_bin_offset_placeholer=BL2_BIN_OFFSET, tfm_sign_bin_placeholer=tfm_sign_bin, sign_bin_offset_placeholer=SIGN_BIN_OFFSET, tfm_hex_placeholder=tfm_hex)
    print(p_cmd)
    subprocess.call(p_cmd, shell=True)

if __name__== "__main__":
    getInputArg()
    valid_param = checkInputArgValid()
    if valid_param == 0:
        print("Invalid parameter!")
        usageDescription()
        sys.exit(-1)
    elif valid_param == 2:
        sys.exit(-1)
    #getSignsecureBin()
    getSignnon_secureBin()
    #getTFMFullBin()	
    #getHex()
