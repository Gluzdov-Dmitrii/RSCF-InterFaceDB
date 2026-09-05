# Instructions for all project agents

## Mission

Build a traceable database and evidence base that can support defensible scientific conclusions and two strong journal articles. Treat research integrity, phase context, units, uncertainty and provenance as product requirements.

## Non-negotiable rules

- Never invent a citation, DOI, numerical value, method, sample size or source locator.
- Separate source facts, model output, inference and proposed hypothesis in every deliverable.
- One database observation represents one result under one defined context, composition, condition and method run.
- Do not merge liquid-vapor surface tension, liquid-liquid interfacial tension, dynamic surface tension, contact angle or adsorption into one target.
- Preserve raw value text, original values and units. Store canonical values separately with a versioned conversion.
- Record both phases for liquid-liquid data; contact angle needs droplet, ambient phase and solid surface.
- Dynamic data need a series coordinate and defined time origin; never confuse surface age with sample aging.
- Keep scientific origin separate from ingestion route, for example MD imported from a paper.
- Every extracted claim or value needs `source_id` and a page, table, figure or dataset-record locator.
- Agent-extracted evidence remains `machine_extracted` until `single_review`, `double_review` or `adjudicated` human review.
- Do not put PDFs, partner documents, raw data, databases, models, trajectories, secrets or run outputs in Git.
- Do not redistribute full text or partner material without a recorded license or authorization.

## Working method

1. Read the current weekly plan and relevant decision records before starting.
2. Create or reuse a stable task or source identifier.
3. Log the exact search query, platform, filters and date.
4. Write outputs only to the path named in the task.
5. Validate links, schema, units and duplicates before reporting completion.
6. Report gaps and contradictions explicitly; do not silently reconcile them.
7. Commit small, coherent changes. Generated and heavy artifacts stay outside Git.

## Scientific priorities

The leading database line is method-aware, uncertainty-aware prediction evaluated on component-, system-, family- and time-disjoint splits. The leading MWCNT line tests whether interfacial and dispersion descriptors explain drilling-fluid behavior better than nanotube concentration alone.

Large MD, QM or CFD campaigns require a written hypothesis, baseline, convergence plan, resource estimate and stop criterion. Do not launch them merely to fill missing cells.
