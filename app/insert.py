#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------
#

from models import Phone
from models import Line
from models import Button
from models import Kem
from models import KemUnit
from models import KemButton


########################
#                      #
#     Study - 101      #
#                      #
########################


p = Phone(
    mac = '00451D0F67E5',
    sys_id = 1,
    serial = 'FCH2228E7MY',
    model = 'CP-8865-3PCC',
    ip = '10.10.30.101',
    location = 'Study',
    extension = 101,
    station_name = '101 - Study',
    did = '214.444.9969',
    additional_template = 'jamie.xml',
    lines = [
        Line(button=1, server='10.10.30.30', secret='101'),
        Line(button=2, server='10.10.20.10', secret='101', 
            label='Control4', hide_missed=True, ring='No Ring')
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=2145467055;nme=Mommy Cell'),
        Button(button=4, func='fnc=sd;ext=2144570933;nme=Dad Cell'),
        Button(button=5, func='fnc=sd;ext=2143940172;nme=Mom Cell'),
        Button(button=9, func='fnc=sd;ext=321@$PROXY;nme=Overhead Paging (321)'),
        Button(button=10, func='fnc=sd;ext=801@$PROXY;nme=Page All (801)')
    ])
p.save()


########################
#                      #
#  Mommy Office - 102  #
#                      #
########################


p = Phone(
    mac = '706E6D10DF74',
    sys_id = 1,
    serial = 'FCH2123D2HC',
    model = 'CP-8851-3PCC',
    ip = '10.10.30.102',
    location = 'Mommy Office',
    extension = 102,
    station_name = '102 - Mommifce',
    did = '214.444.9979',
    lines = [
        Line(button=1, server='10.10.30.30', secret='102'),
        Line(button=2, server='10.10.20.10', secret='102', 
            label='Control4', hide_missed=True, ring='No Ring')
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=701;nme=Daddy All'),
        Button(button=4, func='fnc=sd;ext=2144153735;nme=Daddy Cell'),
        Button(button=5, func='fnc=sd;ext=5127334797;nme=Momma'),
        Button(button=6, func='fnc=sd;ext=8066797995;nme=Dad'),
        Button(button=7, func='fnc=sd;ext=5125891315;nme=Christen'),
        Button(button=10, func='fnc=sd;ext=801@$PROXY;nme=Page All (801)')
    ],
    kem = Kem(
        model='CP-8800-Audio',
        server_type='Asterisk',
        units=[
            KemUnit(
                unit=1,
                buttons=[
                    KemButton(button=1, func='fnc=blf+sd+cp;sub=101@$PROXY;ext=101;nme=Study'),
                    KemButton(button=2, func='fnc=blf+sd+cp;sub=102@$PROXY;ext=102;nme=Mommy Office'),
                    KemButton(button=3, func='fnc=blf+sd+cp;sub=103@$PROXY;ext=103;nme=Kitchen'),
                    KemButton(button=4, func='fnc=blf+sd+cp;sub=105@$PROXY;ext=105;nme=Garage'),
                    KemButton(button=5, func='fnc=blf+sd+cp;sub=201@$PROXY;ext=201;nme=Daddy Bed'),
                    KemButton(button=6, func='fnc=blf+sd+cp;sub=202@$PROXY;ext=202;nme=Mommy Bed'),
                    KemButton(button=7, func='fnc=blf+sd+cp;sub=205@$PROXY;ext=205;nme=James'),
                    KemButton(button=8, func='fnc=blf+sd+cp;sub=208@$PROXY;ext=208;nme=Exercise'),
                    KemButton(button=9, func='fnc=blf+sd+cp;sub=209@$PROXY;ext=209;nme=Guest'),
                    KemButton(button=10, func='fnc=blf+sd+cp;sub=301@$PROXY;ext=301;nme=Datacenter'),
                    KemButton(button=11, func='fnc=blf+sd+cp;sub=302@$PROXY;ext=302;nme=Megahertz'),
                    KemButton(button=12, func='fnc=blf+sd+cp;sub=310@$PROXY;ext=310;nme=Jamie Computer')
            ])
        ])
    )

p.save()


########################
#                      #
#    Kitchen - 103     #
#                      #
########################


p = Phone(
    mac = '7001B5DD4FAC',
    sys_id = 1,
    serial = 'FCH2217E9U',
    model = 'CP-8841-3PCC',
    ip = '10.10.30.103',
    location = 'Kitchen',
    extension = 103,
    lines = [
        Line(button=1, server='10.10.30.30', secret='103', label='$EXT'),
        Line(button=2, server='10.10.20.10', secret='103', label='Control4', 
            hide_missed=True, ring='No Ring')
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=701;nme=Daddy All'),
        Button(button=4, func='fnc=sd;ext=702;nme=Mommy All'),
        Button(button=9, func='fnc=sd;ext=321@$PROXY;nme=Overhead Paging (321)'),
        Button(button=10, func='fnc=sd;ext=801@$PROXY;nme=Page All (801)')
    ])
p.save()


########################
#                      #
#    Garage - 105      #
#                      #
########################


p = Phone(
    mac = '00AA6E203C07',
    sys_id = 1,
    serial = 'WZP22291HE1',
    model = 'CP-7841-3PCC',
    ip = '10.10.30.105',
    location = 'Garage',
    extension = 105,
    lines = [
        Line(button=1, server='10.10.30.30', secret='105', label='$EXT')
    ])
p.save()


########################
#                      #
#   Daddy Bed - 201    #
#                      #
########################


p = Phone(
    mac = '700B4F7BE64E',
    sys_id = 1,
    serial = 'FCH2244D1CU',
    model = 'CP-8865-3PCC',
    ip = '10.10.30.121',
    location = 'Daddy Bed',
    extension = 201,
    station_name = '201 - Master',
    did = '214.444.9969',
    additional_template = 'jamie.xml',
    lines = [
        Line(button=1, server='10.10.30.30', secret='201'),
        Line(button=2, server='10.10.20.10', secret='201', label='Control4', 
            hide_missed=True, ring='No Ring'),
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=2145467055;nme=Mommy Cell'),
        Button(button=4, func='fnc=sd;ext=2144570933;nme=Dad Cell'),
        Button(button=5, func='fnc=sd;ext=2143940172;nme=Mom Cell'),
        Button(button=9, func='fnc=sd;ext=321@$PROXY;nme=Overhead Paging (321)'),
        Button(button=10, func='fnc=sd;ext=801@$PROXY;nme=Page All (801)')
    ])
p.save()


########################
#                      #
#   Mommy Bed - 202    #
#                      #
########################


p = Phone(
    mac = '706E6D10E104',
    sys_id = 1,
    serial = 'FCH2123D2P8',
    model = 'CP-8851-3PCC',
    ip = '10.10.30.122',
    location = 'Mommy Bed',
    extension = 202,
    station_name = '202 - Master',
    did = '214.444.9979',
    lines = [
        Line(button=1, server='10.10.30.30', secret='202'),
        Line(button=2, server='10.10.20.10', secret='202', 
            label='Control4', hide_missed=True, ring='No Ring')
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=701;nme=Daddy All'),
        Button(button=4, func='fnc=sd;ext=2144153735;nme=Daddy Cell'),
        Button(button=5, func='fnc=sd;ext=5127334797;nme=Momma'),
        Button(button=6, func='fnc=sd;ext=8066797995;nme=Dad'),
        Button(button=7, func='fnc=sd;ext=5125891315;nme=Christen'),
        Button(button=9, func='fnc=sd;ext=321@$PROXY;nme=Overhead Paging (321)'),
        Button(button=10, func='fnc=sd;ext=801@$PROXY;nme=Page All (801)')
    ])
p.save()


########################
#                      #
#     James - 205      #
#                      #
########################


p = Phone(
    mac = '00AA6E203B91',
    sys_id = 1,
    serial = 'WZP22291HAK',
    model = 'CP-7841-3PCC',
    ip = '10.10.30.125',
    location = 'James',
    extension = 205,
    station_name = '205 - James',
    did = '214.444.9940',
    lines = [
        Line(button=1, server='10.10.30.30', secret='205', label='$DID')
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=701;nme=Daddy (701)'),
        Button(button=4, func='fnc=sd;ext=702;nme=Mommy (702)')
    ])
p.save()


########################
#                      #
#   Exercise - 208     #
#                      #
########################


p = Phone(
    mac = '7001B5DD4DAE',
    sys_id = 1,
    model = 'CP-7841-3PCC',
    ip = '10.10.30.128',
    location = 'Exercise',
    extension = 208,
    station_name = '208 - Exercise',
    lines = [
        Line(button=1, server='10.10.30.30', secret='208', label='$EXT'),
    ])
p.save()


########################
#                      #
#     Guest - 209      #
#                      #
########################


p = Phone(
    mac = '4C710C4DAF6C',
    sys_id = 1,
    serial = 'WZP23391EQN',
    model = 'CP-7821-3PCC',
    ip = '10.10.30.129',
    location = 'Guest',
    extension = 209,
    station_name = '209 - Guest',
    did = '214.444.5509',
    lines = [
        Line(button=1, server='10.10.30.30', secret='209'),
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=205;nme=Housekeeping')
    ])
p.save()


########################
#                      #
#  Dataceneter - 301   #
#                      #
########################


p = Phone(
    mac = '2C0BE9050373',
    sys_id = 1,
    serial = 'FCH2047F1RS',
    model = 'CP-7841-3PCC',
    ip = '10.10.30.131',
    location = 'Datacenter',
    extension = 301,
    station_name = '301 - Datacenter',
    did = '214.444.9969',
    lines = [
        Line(button=1, server='10.10.30.30', secret='301'),
        Line(button=2, server='10.10.20.10', secret='201', label='Control4', 
            hide_missed=True, ring='No Ring'),
    ],
    buttons = [
        Button(button=3, func='fnc=sd;ext=2145467055;nme=Mommy Cell'),
        Button(button=4, func='fnc=sd;ext=2144570933;nme=Dad Cell'),
        Button(button=5, func='fnc=sd;ext=2143940172;nme=Mom Cell'),
        Button(button=9, func='fnc=sd;ext=321@$PROXY;nme=Overhead Paging (321)'),
        Button(button=10, func='fnc=sd;ext=801@$PROXY;nme=Page All (801)')
    ])
p.save()


########################
#                      #
#      Jim - 401       #
#                      #
########################


p = Phone(
    mac = '2C0BE905051D',
    sys_id = 1,
    serial = 'FCH2047F24A',
    model = 'CP-7841-3PCC',
    location = 'Jim',
    extension = 401,
    station_name = '401 - Jim',
    remote = True,
    lines = [
        Line(button=1, server='10.10.30.30', secret='401', label='$DID')]
    )
p.save()
