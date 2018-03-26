# PA OneCall Mapper *alpha/demo*

[PA OneCall](http://www.pa1call.org/PA811/Public/) has an e-mail-based notification system that will alert you of "Call Before you Dig" requests in your area (*note: CivicMapper is not affiliated with or contracted by PA OneCall*)  As an approved subscriber (i.e., you have to request approval from PA OneCall), you can receive the occasional e-mail from them that looks like this:

```
CDC 00000 POCS MM/DD/YY TT:TT:TT 20180000000-000 NEW XCAV RTN

============PENNSYLVANIA UNDERGROUND UTILITY LINE PROTECTION REQUEST============
Serial Number--[20180651231]-[000] Channel#--[1117AWEB][0222]
Message Type--[NEW][EXCAVATION][ROUTINE]

County--[ALLEGHENY] Municipality--[KILBUCK TWP]
Work Site--[CAMP HORNE RD]
Nearest Intersection--[OLD CAMP HORNE RD]
Second Intersection--[HARMONY RD]
At Intersection--[N] Between Intersections--[Y] Site Marked in White--[Y]
Subdivision--[]
Location Information--
[WE ARE DOING A 10 X 5 STREET REPAIR AT 123 MAIN STREET RD FOR XYZ
WATER AUTHORITY. LOOK FOR RECENTLY EXCAVATED &/OR TEMPORARILY PATCHED
AREA. THIS IS WHERE WE WILL BE WORKING. CONTACT JOE PERSON @
412-555-5555 WITH ANY QUESTIONS.]
Caller Lat/Lon--[]
Mapped Type--[P] Mapped Lat/Lon--
[41.161067/-79.038070,41.538249/-80.850385,40.473058/-80.089223,
40.517399/-80.864821,40.517905/-80.760586,40.518771/-80.0834593]
Attachments--[http://www.pa811.org/attachments/20180651231]
Type of Work--[STREET REPAIR] Depth--[6 FEET]
Extent of Excavation--[VARIOUS] Method of Excavation--[DIGGING]
Equip Type--[EXCAVATOR]
Street--[X] Sidewalk--[ ] Pub Prop--[X] Pvt Prop--[ ] Other--[R/W-UTILITY]
Private Front--[ ] Rear--[ ] Left--[ ] Right--[ ]

Lawful Start Dates--[09-Mar-16] thru [20-Mar-16] Response Due Date--[08-Mar-16]
Scheduled Excavation Date--[09-Mar-16] Dig Time--[0700] Duration--[ONE DAY]

Caller--[JOANNE PERSON]
Caller Phone--[412-555-5555] Caller Ext--[]
Excavator--[BOB'S CONTRACTING]
Address--[123 HIGHWAY RD]
City--[PITTSBURGH] State--[PA] Zip--[12345]
FAX--[555-555-555] Caller Type--[B]
Email--[EMAIL@DEMO.COM]
Work For--[A LOCAL WATER AUTHORITY]
Person to Contact--[JOE PERSON]
Contact Phone--[412-555-5555] Contact Ext--[]
Best Time to Call--[0800-1700]
Job Number--[12345/123-01]

Prepared--[06-Mar-16] at [1121] by [SOMEBODAY]
Remarks--
[]

ACP0 ACP=ALLEGH CTY PWD AL 0 AL =PPLS GAS BD 0 BD =VERIZON PA 
DC 0 DC =DUQ LIGHT PGH IA 0 IA =BUCKEYE PT ALTN KIL0 KIL=KILBUCK TWP 
LT 0 LT =COL GAS ROCHEST MZ 0 MZ =MCCANDLESS TSA OHO0 OHO=OTSA 
PNZ0 PNZ=SHELL APPALACH WX 0 WX =WVWA 

Serial Number--[20180651231]-[000]
========== Copyright (c) 2018 by Pennsylvania One Call System, Inc. ==========
```

This set of scripts will can take a PA One Call e-mails and publish them to a standard geodata web service endpoint so the tickets can be viewed on a web map.

Currently:

* it only parses and publishes the request Serial Number, Mapped Type, and Mapped Lat/Lon information from the ticket; other information could be parsed and stored with it, or linked via a related table in the published service
* it checks what has been published already, and so won't re-publish/duplicate old tickets if the inbox gets messy
* only Esri AGOL Feature Services are supported as endpoints; however it would be trivial to store and publish the data in other formats, (e.g., a csv or geojson in a GitHub repository, a table in CARTO, etc.)

For now, this is just an experiment and technology demo; CivicMapper is not affiliated with or contracted by PA OneCall.

## Software

This is built with Python 3.6 and uses the Python Requests library. We use `pipenv` for a python package and virtual environment management.

The [`config.py`](https://github.com/civicmapper/onecall-mapper/blob/master/config.example.py) file is used to specify e-mails, data endpoints, and authentication information so that the script can get what it needs to get and publish what it's intended to publish.

When run, the script:

1. logs into your IMAP-based e-mail inbox and searches for messages from the configured address (default: `Delivery@pa1call.net`)
2. loads any e-mails matching the sender and subject from PA One call into memory
3. uses a series of regex statements on each e-mail to parse out desired info
4. checks the existing publication endpoint, to see if any of the notices from the inbox have already been published
5. publishes new notices to the publication endpoint.

It's designed to be run as a scheduled task periodically (e.g., a `cron` job or a Windows scheduled task). 
