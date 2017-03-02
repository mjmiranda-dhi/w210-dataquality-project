Reduced data set.  Contains essential data elements:

* sku
* productId
* name
* type
* regularPrice
* categoryPathId (link to category data to find place in hierarchy)
* categoryPathName
* class
* classId
* subclass
* subclassId
* department

Example data:

| sku | productId | name | type | regularPrice | categoryPathId | categoryPathName | class | classId | subclass | subclassId | department |
| --- | --------- | ---- | ---- | ------------:| -------------- | ---------------- | ----- | ------- | -------- | ---------- | ---------- |
48521 | 1185268622267 | Duracell - CopperTop AA Batteries (2-Pack) | HardGood | 2.99 | abcat0208002 | Alkaline Batteries | BATTERIES | 62 | ALKALINE | 90 | PHOTO/COMMODITIES |
309062 | 1218643240258 | Pioneer - 4' 3-Way Surface-Mount Speakers with IMPP Composite Cones (Pair) | HardGood | 144.99 | pcmcat223000050008 | 3-Way Speakers | CAR STEREO | 11 | SO CAR SPEAKERS | 486 | MOBILE AUDIO |


_Please note: to resolve issues with text delimitation, all double-quotes in the data were converted to single quotes during JSON-to-CSV conversion.  This may lead to strange results, such as "Pioneer 4' (i.e., four foot) speakers," as above._
