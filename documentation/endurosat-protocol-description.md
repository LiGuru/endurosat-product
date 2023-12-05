## Endurosat
### UHF TASK

1. Using information provided below for EnduroSat product, please write down piece/script of python code which is:
    - Sending read and write command to the device using serial interface and logging back the answer in a file. Used libraries are part of the solution
    - Make description and explain the meaning of this given device return: ***OK+0022093303***

***Table 14: SCW Format***
    
| [15] | [14] | [13]   [12] | [11]  | [10] [09] [08] | [07]  | [06]  | [05]  | [04]  | [03] | [02] | [01] | [00] |
|------|------|-------------|-------|----------------|-------|-------|-------|-------|------|------|------|------|
| Res  | HFXT | UartBound   | Reset | RfMode         | Echo  | BCN   | Pipe  | Boot  | CTS  | SEC  | FRAM | RFTS |
| 0    | 0    | r/w-3       | r/w-0 | r/w-3          | r/w-0 | r/w-0 | r/w-0 | r/w-X | r-X  | r-X  | r-X  | r-X  |

***Table 15: Bit Fields Meaning***

| Bit Field    | Description                                                                                                                                                           |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [15]         | Reserved: For future use (default value is 0)                                                                                                                         |
| [14]         | HFXT: High frequency oscillator status, 0—oscillator OK, 1—oscillator error                                                                                           |
| [13, 12]     | UartBaud: Speed of the UART interface. Possible values 00-9600, 01 -reserved, 10- 19200, 11-115200 (default). NOTE: 230.200 UART interface speed supported (optional) |
| [11]         | Reset: Write 1 to reset device, O— No effect (default)                                                                                                                |
| [10, 09, 08] | RFMode: see table 16                                                                                                                                                  |
| [07]         | Echo: Local UART echo of the transmitted symbols over the radio when a valid ESTTC command is received via radio; 1 — Echo on, 0 — Echo off(default)                  |
| [06]         | BCN: Beacon message control; 1— enabled, 0—disabled (default)                                                                                                         |
| [05]         | Pipe: Transparent mode communication control; 1- Pipe mode on, 0 — Pipe mode off (default)                                                                            |
| [04]         | Boot: Indicates whether the device is in bootloader or application mode 1 - Bootloader, 0 - Application                                                               |
| [03]         | CTS: Reserved for future use (default value is0)                                                                                                                      |
| [02]         | SEC:Reserved (default value is0)                                                                                                                                      |
| [01]         | FRAM: Indicates whether FRAM is initialized correctly after reset; OK, O-FRAM Error                                                                                   |
| [00]         | RFTS: Indicates whether radio transceiver is initialized correctly after reset 1-OK, 0- Radio Error                                                                   |
     
To switch back and forth between bootloader and application, the user will have to set both bit 4 and bit 11 bearing in mind their effect as described in table 15. If only bit 4 is set/cleared the device will stay in its current mode (bootloader or application).

***Table 16: Available RF Modes***

| RF Mode # 	      | Modulation 	 | Data rate, [bps] 	 | Fdev, [Hz] 	 | ModInd 	 |
|:-----------------|--------------|--------------------|--------------|----------|
| 0 [000]	         | 2GFSK        | 	     1200         | 	  600       | 	 1      |
| 1 [001]   	      | 2GFSK        | 	     2400         | 	  600       | 	 0.5    |
| 2 [010]  	       | 2GFSK        | 	     4800         | 	  1200      | 	 0.5    |
| 3 [011] default	 | 2GFSK        | 	     9600         | 	  2400      | 	 0.5    |
| 4 [100]   	      | 2GFSK        | 	     9600         | 	  4800      | 	 1      |
| 5 [101]   	      | 2GFSK        | 	     19200        | 	  4800      | 	 0.5    |
| 6 [110]  	       | 2GFSK        | 	     19200        | 	  9600      | 	 1      |
| 7 [111]  	       | 2GFSK        | 	     19200        | 	  19200     | 	 2      |

***Table 17: Status Control Word***

| Write  	                       | Answer  	                                                                                         |
|--------------------------------|---------------------------------------------------------------------------------------------------|
| ES+W[AA]OO[WWWW][B][C..C]<CR>	 | 1) OK+[WWWW][B][C..C]<CR> : successful conf                                                       |
|                                | 2) OK+C3C3[B][C..C]<CR> : response when the UHF is commanded to enter Bootloader from Application |
|                                | 3) OK+8787[B][C..C]<CR> : response when the UHF is commanded to enter Application from Bootloader |
|                                | 4) +ESTTCB[B][C..C]<CR> : response at exit of Pipe mode (not valid if command is sent via I2C)    |
|                                | 5) ERR+VAL[B][C..C]<CR> : invalid input data)                                                     |

| Read  	                  | Answer  	                                               |
|--------------------------|---------------------------------------------------------|
| ES+R[AA]OO[B][C..C]<CR>	 | 1) OK+[RR][AA][BB][WWWW][B][C..C]<CR> : successful conf |


| Field  | Description                                                                                                                                                   |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [AA]   | is device address in HEX;                                                                                                                                     |
| [WWWW] | is 16 bit value in HEX format, used to modify the SCW bit field in Write command and current SCW content as a result of "Write" and "Read" command execution; |
| [RR]   | is the last received signal strength indicator (RSSI);                                                                                                        |
| [BB]   | is the reset counter. It counts the number of times whereby the device has undergone reset (power down, reset via command, new SW via bootloader;             |
| [B]    | is blank space ASCII character;                                                                                                                               |
| [C..C] | are the 8 ASCII characters representing the calculated CRC32.                                                                                                 |

***Example commands:***
    ES+R2200 BD888E1F<CR>
    ES+W22003323 589B0F83<CR>

2. Using information provided below for EnduroSat product, please write down piece/script of python code which is:

    - Sending read and write command to the device using serial interface and logging back the answer in a file. Used libraries are part of the solution
    - Make description and explain the meaning of this device return: ***01FF***


| Write  	                       | Answer  	                                   |
|--------------------------------|---------------------------------------------|
| ES+W[AA]F2[FFFF][B][C..C]<CR>	 | 1) OK+[FFFF][B][C..C]<CR> : successful conf |
| 	                              | 2) ERR<CR> : Invalid command value          |

| Read  	                  | Answer  	                                   |
|--------------------------|---------------------------------------------|
| ES+R[AA]F2[B][C..C]<CR>	 | 1) OK+[PPPP][B][C..C]<CR> : successful conf |

***Table 32: Antenna Release Configuration [Application]***

| Field  | Description                                                   |
|--------|---------------------------------------------------------------|
| [AA]   | is device address in HEX;                                     |
| [PPPP] | UHF Antenna release configuration;                            |
| [FFFF] | is the last received signal strength indicator (RSSI);        |
| [B]    | is blank space ASCII character;                               |
| [C..C] | are the 8 ASCII characters representing the calculated CRC32. |

***Table 33: FFFF***

| [15] [14] [13] | [12]  | [11] [10] [09] | [08]  |     [07] [06] [05] [04] [03] [02] [01] [00]     |
|:--------------:|:-----:|:--------------:|-------|:-----------------------------------------------:|
|    Reserved    | First |    Reserved    | EN    |                      Time                       |
|     0 0 0      | r/w-0 |     0 0 0      | r/w-0 | r/w-0 r/w-0 r/w-0 r/w-0 r/w-0 r/w-0 r/w-0 r/w-0 |

- ***[PPPP]***

    ```Indicates UHF Antenna release configuration. 
        The First Byte denotes the enable automatic antenna deployment flag and the enable robust deployment flag. 
        By default, these flags are not set (***deployment is disabled***). 
        The second Byte specifies the time in minutes (in HEX) after power-up after which the deployment sequence should be executed
  ```

- ***[FFFF]***

    ```The Upper Byte can be used to enable/disable the automatic release sequnnce by setting/clearing the ***EN*** bit. 
       The ***First*** bit indicates if the robust automatic release sequence is to be executed. 
       If set, the release logic will check (after power-up/reset amd first antena connection) if any rods are opened. 
       If such are found, the logic will consider that some issues have occured and will try to deploy them first. 
       If this algorithm is successfully executed, the ***First*** flag will be cleared automatically, 
       otherwise it will stay set and the UHF Tranciever will try to deploy all open rods again at next power-up/reset cycle. 
  ```
    
    ```The Lower Byte spcifies the time in minutes after device power-up when antenna deployment should happpen. 
       This value is in HEH and can be anything between ***0x0A*** and ***0XFF*** including.```

***Bear in mind*** that if a release command is given to the device and the device has powered up longer than the time indicates by the Lower Byte, the antenna release sequence ***will begin immediately!*** In case the command is sent via I2C, the user may not get an appropriate reply as the UHF Transceiver will swich to I2C master mode.

To prepare the UHF to release the antenna after next power-up, power-uo the UHF module, set the appropriate command values and power-off device. At the next power-up the UHF will wait until the set time elapsed and will release the antenna. If the device is not powered-off after release command is set, the release will happen as soon as the internal UHF timer reaches the set time.

if no connection to the antenna has been established or all rods have not deployed, the ***EN*** flag will not be cleared and the next power-up/reset logic will be restarted (release after the set time). Onlu once the antenna has returned a status that all rods are opened the ***EN*** flag will be cleared.

The release algorithm embedded in the UHF Transceiver will analyse the antenna statuses and will try to release all of them by turning on the different algorithms intrinsic to the UHF Antenna.

***Example commands:***

    ES+R22F2 2AE33143<CR>
    ES+W22F201FF 852DF0FE<CR>
    
    
