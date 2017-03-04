Reduced data set.  Contains essential data elements:

* sku
* productId
* name
* type
* regularPrice
* class
* classId
* subclass
* subclassId
* department
* categoryPathId (link to category data to find place in hierarchy)
* categoryPathName
* categoryParentLevel1Id (1st parent category one level up)
* categoryParentLevel1Name
* categoryParentLevel2Id (parent category _two levels_ up)
* categoryParentLevel2Name 
* categoryParentLevel3Id (parent category _three levels_ up)
* categoryParentLevel3Name
* categoryParentLevel4Id (parent category _four levels_ up)
* categoryParentLevel4Name
* categoryParentLevel5Id (parent category _five levels_ up)
* categoryParentLevel5Name
* categoryParentLevel6Id (parent category _six levels_ up)
* categoryParentLevel6Name
* categoryParentLevel7Id (parent category _seven levels_ up)
* categoryParentLevel7Name
* randId (randomly-assigned identifier to simplify partitioning data, if needed)


Example data:

sku | productId | name | type | regularPrice | class | classId | subclass | subclassId | department | categoryPathId | categoryPathName | categoryParentLevel1Id | categoryParentLevel1Name | categoryParentLevel2Id | categoryParentLevel2Name | categoryParentLevel3Id | categoryParentLevel3Name | categoryParentLevel4Id | categoryParentLevel4Name | categoryParentLevel5Id | categoryParentLevel5Name | categoryParentLevel6Id | categoryParentLevel6Name | categoryParentLevel7Id | categoryParentLevel7Name | randId
--- | --------- | ---- | ---- | ------------ | ----- | ------- | -------- | ---------- | ---------- | -------------- | ---------------- | ---------------------- | ------------------------ | ---------------------- | ------------------------ | ---------------------- | ------------------------ | ---------------------- | ------------------------ | ---------------------- | ------------------------ | ---------------------- | ------------------------ | ---------------------- | ------------------------ | ------
4286793 | 1051806990720 | SanDisk - 512MB CompactFlash Memory Card | HardGood | 14.99 | FLASH MEMORY | 54 | COMPACT FLASH MEMORY | 697 | PHOTO/COMMODITIES | abcat0404002 | Compact Flash | pcmcat225800050009 | Memory Cards | abcat0404000 | Memory Cards & Readers | pcmcat241300050030 | Point & Shoot Camera Accessories | abcat0401001 | Point & Shoot Cameras | abcat0401000 | Digital Cameras | abcat0400000 | Cameras & Camcorders | cat00000 | Best Buy | D912557D-34B4-43CB-B0AB-F7AD69582C6E
15421571 | 1614568 | Sonotropism - CD | Music | 12.99 | COMPACT DISC | 77 | JAZZ-CONTEMPORARY | 1002 | VIDEO/COMPACT DISC | cat02007 | Jazz | cat02001 | Music | abcat0600000 | Movies & Music | cat00000 | Best Buy |  |  |  |  |  |  |  |  | AA780422-8343-4B23-8622-000024BDBD8D
9847622 | 1218184163692 | LG - 1.8 Cu. Ft. Over-the-Range Microwave - Stainless-Steel | HardGood | 349.99 | KITCHEN | 203 | OTR MICROWAVES | 6069 | APPLIANCE | abcat0903001 | Over-the-Range Microwaves | abcat0903000 | Microwaves | abcat0900000 | Appliances | cat00000 | Best Buy |  |  |  |  |  |  |  |  | 98F14A1B-C608-44EC-B355-002C2375CAD9


_Please note: to resolve issues with text delimitation, all double-quotes in the data were converted to single quotes during JSON-to-CSV conversion.  This may lead to strange results, such as "Pioneer 4' (i.e., four foot) speakers," as above._
