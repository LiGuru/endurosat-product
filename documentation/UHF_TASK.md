## Description UHF_TASK_A

***Sending read and write command to the device using serial interface and logging back the answer in a file. Used libraries are part of the solution***

### Approach 
***The provided script initializes and configures modules for UART communication, particularly focusing on UHF and antenna modules. It includes the following components:***

    Initialization:
        Sets up the system logger and configuration parameters.
        Initializes a UART service for communication.
        Creates an object for UART communication.

    Module Configuration:
        Initializes UHF and antenna modules with specified addresses and attributes.
        Logs the initial state of both modules.

    Communication Execution:
        If not using dummy data, retrieves and sets the current configuration for both UHF and antenna modules through UART communication.

    Dummy Data Handling:
        If using dummy data:
            Creates a simulated response for UHF and antenna modules.
            Sets specific modes and configurations for the UHF module.
            Simulates the configuration response for the antenna module.

    Logging:
        Logs the final state of both UHF and antenna modules.

This script is designed for configuring and managing communication modules, demonstrating functionality for both real and simulated scenarios.


## Task Description UHF_TASK_B:
***The task involves decoding and describing the configuration of a device based on the provided return:***
```markdown
    OK+0022093303
```

### UHF Configuration Description

```
    UseUHFModule('address': '0x22', 'uart_baud_mode': 3, 'uhf_specific_attributes': [], 'hfxt': False, 'uart_baud': 115200, 'reset': False, 'rf_mode': 3, 'echo': False, 'bcn': False, 'pipe': False, 'boot': False, 'fram': 'OK', 'rfts': True, 'modulation_type': '2GFSK', 'modulation_data_rate': 9600, 'modulation_fdev': 2400, 'modulation_index': 0.5, 'reset_counter': 9, 'rssi': 0, 'schema': '3303')

```

* **Address:** '0x22'
* **UART Baud Mode**: 3 (Baud Rate: 115200 bps)
  - This field represents the speed of the UART (Universal Asynchronous Receiver-Transmitter) interface.
  - The value '3' is encoded in binary as '11' and formatted to occupy three bits ('03b').
  - The possible values and their binary representations are:
    - 00: 9600
    - 01: Reserved
    - 10: 19200
    - 11: 115200 (default)
  - The provided value '3' translates to '11', indicating that the UART Baud is set to the default speed of 115200.
* **HFXT (High-Frequency Crystal Oscillator) Status:** False (No oscillator error)
  - This field indicates the status of the High-Frequency Oscillator (HFXT).
  - The value 'False' suggests that the oscillator is functioning correctly.
* **Device Reset Status**: False (No ongoing reset)
  - The 'False' value means that writing '1' to this field will reset the device, but currently, no reset has been triggered.
* **RF Mode**: 3 (Specific radio frequency configuration)
  - This field signifies the Radio Frequency Mode.
  - The value '3' is encoded as '11' in binary, occupying three bits ('03b').
* **UART Echo**: False (Local UART echo of transmitted symbols turned off)
  - Indicates whether local UART echo is active.
  - 'False' suggests that echo is currently turned off.
* **Beacon Message Control (BCN)**: False (Beacon messages disabled)
  - Beacon message control field.
  - 'False' indicates that beacon messages are currently disabled.

* **Transparent Mode Communication Control (Pipe)**: False (Pipe mode turned off)
  - Transparent mode communication control field.
  - 'False' signifies that transparent mode communication is currently inactive.

* **Boot Mode**: False (Device in application mode)
  - Indicates whether the device is in bootloader or application mode.
  - 'False' suggests that the device is currently in application mode.

* **FRAM Initialization Status**: 'OK' (Successful initialization)
  - Indicates the initialization status of FRAM (Ferroelectric Random-Access Memory).
  - The value 'OK' suggests that FRAM is initialized without errors.

* **Radio Transceiver Initialization Status (RFTS)**: True (Successful initialization)
  - Indicates the initialization status of the radio transceiver.
  - 'True' signifies that the radio transceiver is initialized correctly.

* **Modulation Type**: '2GFSK' (2-Level Gaussian Frequency Shift Keying)
* **Modulation Data Rate**: 9600 bps
* **Modulation Frequency Deviation**: 2400 Hz
* **Modulation Index**: 0.5 (Ratio of peak frequency deviation to data rate)
* **Reset Counter**: 9 (Current reset count)
* **Received Signal Strength Indicator (RSSI)**: 0 (Current signal strength)

This comprehensive description provides insights into each attribute of the device's current configuration and status. If you have any further questions or if there's anything else you'd like to explore, feel free to let me know!

## Antenna Configuration Description

```
UseAntennaModule('address': 34, 'antenna_specific_attributes': [], 'auto_release_enabled': True, 'robust_release_enabled': False, 'release_time_minutes': 255, 'rssi': 0, 'rssi_last_time_minutes': 0, 'schema': '01FF')

```

The UseAntennaModule class represents an Antenna Module with specific attributes and functionalities. Below is a detailed description of its key parameters:

* ***Address:*** The hexadecimal address of the antenna module is set to 34.
* ***Auto Release Enabled:*** Automatic release sequence status is enabled (True), indicating that the antenna can perform an automatic release sequence.
* ***Robust Release Enabled:*** Robust automatic release sequence status is disabled (False), meaning that the antenna will not execute a more resilient release sequence, even if issues are detected.
* ***Release Time Minutes:*** The time, in minutes, after device power-up when the antenna deployment should occur. In this case, it is set to the maximum value of 255.
* ***RSSI (Received Signal Strength Indicator):*** The received signal strength indicator is set to 0, indicating no received signal strength.
* ***RSSI Last Time Minutes:*** The time, in minutes, since the last received signal strength indicator measurement. It is set to 0, indicating that no recent measurement has been recorded.
* ***Schema:*** The configuration schema for the antenna module is set to '01FF', indicating specific settings and conditions for the antenna module.

This description provides an overview of the key attributes and functionalities of the Antenna Module, including its addressing, release sequence settings, and signal strength indicators.

## Additional Information: Configuration File

***The script relies on a configuration file (config.ini) with the following sections and parameters:***

[Application]

    name: Name of the application.

[Log]

    level: Logging level (debug, info, warn, error, critical).
    file: Log file name.
    logger-name: Logger name.

[Port.Config]

    debug: Debug mode (1 for true, 0 for false).
    port: UART port (e.g., "/dev/ttyACM0").
    baudrate: Baud rate for UART communication.
    bits: Number of data bits.
    stopbits: Number of stop bits.
    parity: Parity setting.
    flow: Flow control setting.
    timeout: Timeout for UART communication.
    carriage: Carriage return configuration ("<cr>" options: r=\r, rn=\r\n, n=\n, nr=\n\r).

[UHF.Config]

    address: Address configuration for the UHF module.

[Antenna.Config]

    address: Address configuration for the antenna module.

These configurations define the parameters necessary for initializing and communicating with the UART modules in the provided script. Adjustments can be made in the configuration file to customize the behavior of the script.
