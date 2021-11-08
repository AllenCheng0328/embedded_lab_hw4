/* mbed Microcontroller Library
 * Copyright (c) 2006-2013 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <mbed.h>
#include "ble/BLE.h"
#include "ble/Gap.h"

class StudentID {
public:
    const static uint16_t STUDENT_UUID              = 0xB000;
    const static uint16_t STUDENT_CHARACTERISTIC_UUID = 0xB001;

    StudentID(BLE &_ble, char rcvID[]) :
        ble(_ble), ID_service(STUDENT_CHARACTERISTIC_UUID, rcvID, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY)
    {
        GattCharacteristic *charTable[] = {&ID_service};
        GattService         IDservice(StudentID::STUDENT_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
        ble.gattServer().addService(IDservice);
    }

private:
    BLE                              &ble;
    ReadOnlyArrayGattCharacteristic<char, 9>  ID_service;
};


