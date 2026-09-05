# Database layer

`schema/001_initial.sql` is the normalized SQLite reference implementation. The
JSON observation contract in `data/schemas/` is the interchange format used at
the extraction boundary. Database files themselves are generated artifacts and
must remain outside Git.

Version 0.2 contains 56 tables, 77 integrity triggers and 43 controlled property
terms, including method-specific dispersion, rheology, interfacial and MWCNT
endpoints. Ambiguous legacy terms may be retained at staging/curation level but
are blocked from model-ready snapshots.

Every SQLite client must execute and verify `PRAGMA foreign_keys = ON` after opening
a connection; the setting is connection-local. Python validation remains responsible
for unit conversions, composition closure and higher-level leakage checks that SQLite
cannot establish on its own.

Schema changes require a numbered migration, a data-dictionary update and a test.
