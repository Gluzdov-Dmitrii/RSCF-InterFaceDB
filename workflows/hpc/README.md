# HPC workflow requirements

Before creating a production submission script, record:

- scientific hypothesis and decision affected by the run;
- system definition, software/version and reproducible input generator;
- cheap baseline and reason the cluster run is necessary;
- convergence variables, replicate plan and uncertainty estimator;
- expected CPU/GPU hours, memory, wall time and storage;
- checkpoint/restart and failure handling;
- output hashes, metadata and durable archive destination;
- stop rule and owner.

Cluster scratch is never the only copy. Job scripts and compact inputs belong in Git; trajectories, checkpoints and bulk outputs do not.
