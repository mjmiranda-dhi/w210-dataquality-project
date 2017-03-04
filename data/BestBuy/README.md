# W210 Final Project
##UC Berkeley MIDS W210 (Spring 2017)
##Data Quality / Outlier Detection in Hierarchical Data
_Burt, D.M. | Miranda, M.J. | Shen, Max | Weeks, Timothy_

&nbsp;
&nbsp;

## Data Set: Best Buy
_Source: Best Buy, Inc. (via Best Buy API)_

### Categories
Best Buy categories have a root of _cat00000_ (name: "Best Buy").  Each node in the tree (including the root) is searchable in the first column (_categoryId_), and the layout of the CSV/TSV files provides a path back to the root by reading from left to right across the row.

### Products
The categories the products are assigned to can be found in the categoryPathId and categoryPathName columns.  The original data from Best Buy provided a chain of IDs from the assigned-node category back to the root category.  In the CSV/TSV files, however, only the assigned-node category is given; the path back to the root is available using a join to the _categories_ data on product.categoryPathId = category.categoryId.

### Product Walkback
Due to popular demand, there is now a _"walkback"_ version of the __product__ data set.  This puts the path back to the root into the _product_ data.  Check out the documentation in the _walkback_ folder for more information.
