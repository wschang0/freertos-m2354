/*
 * Copyright (c) 2019, Arm Limited. All rights reserved.
 * Copyright (c) 2022, Nuvoton Technology Corp. All rights reserved. 
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#include "os_wrapper/mutex.h"

#include "FreeRTOS.h"
#include "semphr.h"
#include "mpu_wrappers.h"


void* os_wrapper_thread_new(const char* name, int32_t stack_size,
    TaskFunction_t func, void* arg,
    uint32_t priority)
{
    TaskHandle_t xHandle = NULL;

    xTaskCreate(func, name, stack_size, arg, priority, &xHandle);
    return (void*)xHandle;

}

void* os_wrapper_thread_get_handle(void)
{
    return (void*)xTaskGetCurrentTaskHandle();
}

uint32_t os_wrapper_thread_get_priority(void* handle, uint32_t* priority)
{
    *priority = (uint32_t)uxTaskPriorityGet((TaskHandle_t)handle);

    return OS_WRAPPER_SUCCESS;
}

void os_wrapper_thread_exit(void)
{
    vTaskDelete(NULL);
}



void* os_wrapper_semaphore_create(uint32_t max_count, uint32_t initial_count,
    const char* name)
{
    return (void*)xSemaphoreCreateCounting(max_count, initial_count);
}

uint32_t os_wrapper_semaphore_acquire(void* handle, uint32_t timeout)
{
    BaseType_t status;

    status = xSemaphoreTake((SemaphoreHandle_t)handle,
        (timeout == OS_WRAPPER_WAIT_FOREVER) ?
        portMAX_DELAY : timeout/portTICK_PERIOD_MS);
    if(status != pdTRUE) {
        return OS_WRAPPER_ERROR;
    }

    return OS_WRAPPER_SUCCESS;
}

uint32_t os_wrapper_semaphore_release(void* handle)
{
    BaseType_t status;

    status = xSemaphoreGive((SemaphoreHandle_t)handle);
    if(status != pdTRUE) {
        return OS_WRAPPER_ERROR;
    }

    return OS_WRAPPER_SUCCESS;
}


uint32_t os_wrapper_semaphore_delete(void* handle)
{
    vSemaphoreDelete((SemaphoreHandle_t)handle);
    return OS_WRAPPER_SUCCESS;
}

void * os_wrapper_mutex_create( void )
{
SemaphoreHandle_t xMutexHandle;

#if( configSUPPORT_DYNAMIC_ALLOCATION == 1 )
	xMutexHandle = xSemaphoreCreateMutex();
#else
	xMutexHandle = NULL;
#endif
	return ( void * )xMutexHandle;
}

uint32_t os_wrapper_mutex_acquire( void * handle, uint32_t timeout )
{
    BaseType_t xRet;

	if( ! handle )
		return OS_WRAPPER_ERROR;

	xRet = xSemaphoreTake(( SemaphoreHandle_t )handle,
												( timeout == OS_WRAPPER_WAIT_FOREVER ) ?
                             portMAX_DELAY : ( TickType_t )timeout );

	if( xRet != pdPASS )
		return OS_WRAPPER_ERROR;
	else
		return OS_WRAPPER_SUCCESS;
}

uint32_t os_wrapper_mutex_release( void * handle )
{
    BaseType_t xRet;

	if( ! handle )
		return OS_WRAPPER_ERROR;

	xRet = xSemaphoreGive(( SemaphoreHandle_t )handle );

	if( xRet != pdPASS )
		return OS_WRAPPER_ERROR;
	else
		return OS_WRAPPER_SUCCESS;
}

uint32_t os_wrapper_mutex_delete( void * handle )
{
	vSemaphoreDelete(( SemaphoreHandle_t )handle );

	return OS_WRAPPER_SUCCESS;
}