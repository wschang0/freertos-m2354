cd d:/MCU/TF-M_Review/mcuboot-src/scripts
D:/MCU/TF-M_Review/trusted-firmware-m/bl2/ext/mcuboot/scripts/wrapper/wrapper.py -v 0.0.0 --layout D:/out/m2354/install/image_signing/layout_files/signing_layout_ns.o -k D:/MCU/TF-M_Review/trusted-firmware-m/bl2/ext/mcuboot/root-RSA-3072_1.pem --public-key-format full --align 1 --pad --pad-header -H 0x400 -s 1 -L 128 -d "(0, 0.0.0+0)" D:/MCU/FreeRTOS/FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2354_IAR_GCC/Projects/Keil/NonSecure/Objects/FreeRTOSDemo_ns.bin --overwrite-only  D:/out/m2354/bin/freertos_signed.bin
cd D:/MCU/FreeRTOS/FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2354_IAR_GCC/Projects/Keil/NonSecure
bin2hex --offset=0x10070000 D:/out/m2354/bin/freertos_signed.bin D:/out/m2354/bin/freertos_signed.hex
