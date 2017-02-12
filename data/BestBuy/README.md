Best Buy Data


### Categories
Best Buy categories have a root of _cat00000_ (name: "Best Buy").  Each node in the tree (including the root) is searchable in the first column (_categoryId_), and the layout of the CSV/TSV files provides a path back to the root by reading from left to right across the row.

<br>
<br>

### Products
The categories the products are assigned to can be found in the categoryPathId and categoryPathName columns.  The original data from Best Buy provided a chain of IDs from the assigned-node category back to the root category.  In the CSV/TSV files, however, only the assigned-node category is given; the path back to the root is available using a join to the _categories_ data on product.categoryPathId = category.categoryId.
