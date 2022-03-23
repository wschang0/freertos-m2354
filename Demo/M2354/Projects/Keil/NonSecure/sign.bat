cd ..\..\..\..\..\..\trusted-firmware-m-m2354\build\lib\ext\mcuboot-src\scripts
..\..\..\..\..\bl2\ext\mcuboot\scripts\wrapper\wrapper.py -v 0.0.0 --layout ..\..\..\..\build\install\image_signing\layout_files\signing_layout_ns.o -k ..\..\..\..\..\bl2\ext\mcuboot\root-RSA-3072_1.pem --public-key-format full --align 1 --pad --pad-header -H 0x400 -s 1 -L 128 -d "(0, 0.0.0+0)" ..\..\..\..\..\..\FreeRTOS\Demo\M2354\Projects\Keil\NonSecure\Objects\FreeRTOSDemo_ns.bin --overwrite-only  ..\..\..\..\..\..\freertos_signed.bin
cd ..\..\..\..\..\..\
bin2hex --offset=0x10070000 freertos_signed.bin freertos_signed.hex
cd C:\M2354\FreeRTOS\Demo\M2354\Projects\Keil\NonSecure
