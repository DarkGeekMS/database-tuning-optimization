# Database Tuning and Optimization

This is a college project on database system tuning and query optimization.

## Database Filling

-   The _SQL_ database filling scripts and _NoSQL_ collections can be found in this [GDrive folder](https://drive.google.com/drive/folders/1IU2V4QAJ_IvlzgUSa1xszIMZ3Pq1ciYt?usp=sharing).

-   Make sure to disable foreign key checks bfore running _SQL_ scripts : `SET FOREIGN_KEY_CHECKS=0;`.

## Optimization Techniques

-   [x] Schema Optimization :
    -   [x] Normalization/Denormalization.
    -   [x] Data types optimization.

-   [ ] Memory and Cache Optimization :
    -   [ ] Paging.
    -   [ ] Hardware Specs.
    -   [ ] Stored Procedures.
    -   [ ] Storage Engine (_InnoDB_ vs. _MYISAM_).
    
-   [x] Index Optimization :
    -   [x] Indexes Generation on Non-Primary Keys.
    -   [x] UNION is better than OR with Indexes.

-   [x] Query Optimization :
    -   [x] Unnecessary Conditions Elimination.
    -   [x] UNION ALL instead of UNION.

## Required Statistics

-   [ ] Non-optimized _SQL_ vs. Optimized _SQL_ (100,000).

-   [ ] Optimized _SQL_ vs. _NoSQL_ (100,000).

-   [ ] Different Sizes of Optimized _SQL_ (10,000 / 100,000 / 1,000,000).

-   [ ] Different hardware on Optimized _SQL_.
