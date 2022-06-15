Mazak VQC 15/40

TDS used:

    7i80HD anyio (3x50-pin)

    7i49 resolver servo interface, 50-pin

    7i44 (sserial breakout

    2*7i84 (the regular "not-D" version) (32 input/16 output each,
    sserial)
        7i84-A
            in: 19
                TB2 15: 1-8 10-16
                TB3  4: 1-4
            out: 13
        7i84-B
            in: 22
                TB2 12: 1-9 13 (14-16?)
                TB3 10: 1-6 9-12
            out: 16
        total:
            41 in
            29 out

    7i73 smart serial remote control panel interface

we're using:

    7i80HD-25 (AnyIO FPGA board)

        MAC 00:60:1B:11:81:AA

        W1, W2 in the DOWN position (default), IP address is 192.168.1.121

        W3 in the UP position (default), pull-up IO pins on power-up
        and reset

        W4 in the UP position (default), 5V tolerance mode enabled

        W5 in the UP position (default), boot from primary flash

        W6, W7, W8 all in the UP position (default), 5V on all 3 50-pin
        connectors

        P1 is connected to +5 & Ground (from an external power supply)

        Default firmware doesn't support resolvers (like the 7i49 has).
        Download 7i80.zip (Mesa's 7i80HD "Support Software" zip file)

    7i49 (6 channel resolver/servo interface)

        W1 is in the LEFT position (NOT default), accept external 5V power via P1

        W2 is in the UP position (default), standard resolver signal
        levels on all channels

        P1 is connected to +5 & Ground (from an external power supply)

    7i44 (8 channel RS-422/RS-485 interface)

        W1 is in the BOTTOM position (NOT default), accept external 5V power via P1

        P1 is connected to +5 & Ground (from an external power supply)

        It expects Cat6 568B pinout.  Is Cat5e ok?

        RS-422 SSLBP "smart serial"

    2x7i84 (32 in/16 out each, sserial)

        this is the sourcing output version, not the sinking output
        "D" version

        W1 is in the LEFT position (default), operate logic on field
        power, no connection to TB1 pin 5.

        W2 is in the LEFT position (default), 2.5 Mbaud

        TB1:
            pin 1-4 are connected to P24 on the Mazak (+24V DC)
            pin 5 is not connected (internally connected to VFIELDB via W1 in the left position)
            pin 6-8 are connected to G24 on the Mazak (ground for P24 power rail)


# NC Connectors

Mating pins?  https://www.radwell.co.uk/en-GB/Buy/HONDA/HONDA/MRP-M112

spec sheet here: https://www.onlinecomponents.com/en/datasheet/mrpm112-41909323

wants AWG 24-28 (0.5106-0.3211 mm conductor diameter, insulation OD 1.2-1.5 mm)

We don't have the correct mating connectors or pins, so we're using 0.72
mm² cross-sectional area stranded wire, to which we're attaching some
random pin connectors that we bought.  They friction-fit into the female
connectors ok.

The CND[1234] cable connectors are marked "Honda MR-50W".  The controller
should have the mating connector.

connectors between control computer and machine cabling:

    MR-50L Honda connectors?

    pins: "MRP-M1( )( )"?


# Mazak VQC 15/40 hardware

spindle drive: Mitsubishi Freqrol-SF

servo amps: Mitsubishi Meldas TRS50B AXO4D


# Power supplies

There are two 24V DC power systems:

1. P24 (+24 VDC) and G24 (ground) is always on, powered by the EC-11
power supply.

2. "+24" (+24 VDC) and "0G" (ground) can normally be turned on and off
using the green power-on button on the control panel.  Supplied by the
PD14C-1 power supply that's part of the NC.  Powers the computer and
a bunch of other stuff.  0G is connected to G24 when this power supply
is on.

We hardwired "0G" to "G24" with a jumper wire.

We disconnected the PD14C-1 power supply by the NC and instead wired
a small off-the shelf 24V DC, 1.5A (100 VAC input) power supply to the
"+24"/"0G" power rail.  It's powered by the 100V AC from the machine.

We're powering the 5V Mesa boards using a stand-alone ATX power supply.
This power supply's Ground is connected to 0G/G24.  The power supply
also provides the +12/-12 VDC for the resolvers.


## Servos

The X and Y servos (and I think Z) are labeled:

    HA-83C-S
    Permanent Magnet AC Servo Motor
    Mitsubishi Electric Corp

The back of each servo has a "detector", aka "pickup unit" labeled:

    PICKUP UNIT
    TYPE: ATT-A-11
    SPEC NO: BKO-NC6198
    PARTS NO: RS2034N2E3
    TAMAGAWA SEIKI CO LTD

    A bundle of 7 wire/wire-pairs from this pickup unit go to the
    servo amp.  This is the resolver used by the servo amp.

Each ball screw has a "resolver", aka pickup unit mounted on the end
near the servo.  The one on the Y ball screw is labeled:

    Sanyo Denki
    P/N: 101
    SPEC NO: BKO-NC 6062
    TYPE: RT XC-11 (maybe "RT-4XC-11"?)
    PICKUP UNIT

    The bundle of 3 wire-pairs from each of these pickup units goes to
    the NC, via CNA-3, -4, and -5.  This is the resolver used by the NC
    for position control.

    The machine's resolver connector (CNA3 etc) needs +12, -12V, and
    Ground.  We used +12/-12 from the ATX power supply that powers the
    Mesa boards.  Its +12 goes to CNA{3,4,5} pin "P12", its -12V goes to
    "M12", and two "AG" pins are connected to 0G.


# To bring machine up

Apply pressurized air (what pressure?).

Open the manual air valve at the machine's air intake.

Turn on "+24V"/"0G" power supply.

Release all E-stop buttons (1 by operator console, 1 by tool magazine
access door, 1 optional on "handy controller").

Power on MAR relay ("power-on" net).

Power on the hydraulic pump ("hydraulic-lube-pump-on" net).

Activate the tool magazine main solenoid ("magazine-run" net).
