/*
 * Copyright (c) 2017-2021, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

/*
 * An example to implement tfm_ns_interface_dispatch() in NS RTOS to integrate
 * TF-M interface on Armv8-M TrustZone based platforms.
 *
 * In this example, NS OS calls mutex in tfm_ns_interface_dispatch() to
 * synchronize multiple NS client calls.
 * NS OS pseudo code in this example is not based on any specific RTOS.
 *
 * Please note that this example cannot be built directly.
 */

#include <stdint.h>

/* Include NS RTOS specific mutex declarations */
#include "FreeRTOS.h"
#include "semphr.h"
#include "os_wrapper/mutex.h"
#include "tfm_ns_interface.h"

/* Static ns lock handle */
static void *ns_lock_handle = NULL;

#define OS_SUCCESS      (0)
#define OS_ERROR        (-1)

/* Initialize the ns lock */
int32_t ns_interface_lock_init()
{
    /* NS RTOS specific mutex creation/initialization */
    ns_lock_handle = xSemaphoreCreateMutex();
    if (ns_lock_handle) {
        return OS_SUCCESS;
    }

    return OS_ERROR;
}

int32_t tfm_ns_interface_dispatch(veneer_fn fn,
                                  uint32_t arg0, uint32_t arg1,
                                  uint32_t arg2, uint32_t arg3)
{
    int32_t result;

    /* TF-M request protected by NS lock. */
    while (xSemaphoreTake(ns_lock_handle, 100) != OS_SUCCESS);

    result = fn(arg0, arg1, arg2, arg3);

    /*
     * Whether to check/handle lock release return code depends on NS RTOS
     * specific implementation and usage scenario.
     */
    xSemaphoreGive(ns_lock_handle);

    return result;
}
