# Sprint 0 — Engineering Foundation

## Sprint objective

Create the smallest production-grade skeleton that proves the contracts and infrastructure before building AI features.

## Definition of done

Sprint 0 is complete when:
- monorepo boots locally with one documented command;
- web and API health endpoints work;
- PostgreSQL, Redis, object storage emulator and Temporal development server are wired locally;
- project/source-asset persistence exists;
- direct upload flow is represented end-to-end;
- a workflow can ingest a sample asset, FFprobe it, create a proxy activity placeholder/result and report progress;
- canonical time/media/timeline models compile in Python and TypeScript with contract tests;
- CI runs lint/typecheck/unit/contract tests;
- observability/error IDs exist from the beginning;
- no AI provider is required to pass the foundation test suite.

## P0 backlog

### S0-001 Monorepo
Create apps/web, apps/api, apps/worker-media, apps/worker-ai, apps/worker-render, packages/*, workflows, infrastructure, tests, evals and docs. Pin runtime/toolchain versions.

### S0-002 Local infrastructure
Docker Compose for PostgreSQL + pgvector, Redis, S3-compatible local object storage and Temporal dev dependencies. Health checks and named volumes.

### S0-003 API skeleton
FastAPI app factory, configuration, structured errors, request IDs, health/readiness, OpenAPI generation and versioned `/v1` routing.

### S0-004 Web skeleton
Next.js application with typed API client generation, project shell, upload placeholder and realtime progress transport abstraction.

### S0-005 Persistence
Initial migrations for workspace, project, source_asset, media_stream and workflow_run. Tenant/project authorization hooks even if MVP auth uses a development identity.

### S0-006 Storage abstraction
S3-compatible interface, signed multipart upload initiation/completion, checksum metadata, storage-key policy and lifecycle hooks.

### S0-007 Canonical time package
Implement rational/integer time primitives with conversion, comparison, range intersection and serialization tests in Python/TypeScript.

### S0-008 Media schema package
Implement SourceAsset, MediaStream, EvidenceRef, TranscriptWord, Shot, Scene, Detection, StoryBeat and Provenance contracts.

### S0-009 Timeline package
Implement Timeline/Track/TimelineItem/TimelinePatch schema and validation: no negative ranges, source range validity, track compatibility, version checking and stable serialization.

### S0-010 Workflow skeleton
Implement IngestSourceWorkflow with activities: verify upload → probe media → persist streams → emit progress → mark ingest ready. Activity results must be idempotent.

### S0-011 FFprobe adapter
No arbitrary user-supplied flags. Execute fixed command templates, parse output into MediaStream contracts, capture stderr safely and enforce timeout/resource limits.

### S0-012 Event contracts
Versioned project/workflow/render event envelope with monotonically increasing project sequence or resumable cursor semantics.

### S0-013 Observability
Structured logging, trace IDs, OpenTelemetry hooks and Sentry integration boundary. Never log signed URLs, tokens or raw provider secrets.

### S0-014 CI
Format/lint/typecheck/tests; schema compatibility tests; migration check; container build smoke test; dependency/security scan.

### S0-015 Golden fixture
Add a small legally redistributable synthetic/sample media fixture or generator for deterministic ingest/probe/timeline tests.

## P1 backlog — Sprint 1 preview

- proxy generation;
- waveform generation;
- normalized analysis audio;
- transcription provider contract;
- first transcription implementation;
- transcript storage/indexing;
- shot detection;
- initial intelligence graph persistence;
- hybrid semantic search endpoint.

## Engineering rules

1. No business logic in HTTP route handlers.
2. No provider SDK types leak into domain models.
3. No AI-generated shell/FFmpeg commands.
4. No process memory is authoritative workflow state.
5. No float seconds in canonical timeline contracts.
6. No destructive source edits.
7. Every external operation has timeout/retry policy.
8. Every expensive operation has cost/usage metadata hooks.
9. Every AI artifact introduced later must be schema validated and evidence grounded.
10. Every PR that changes a canonical contract adds/updates compatibility tests.

## Architecture decision records to create during Sprint 0

- ADR-001 Monorepo/toolchain choice
- ADR-002 Temporal for durable orchestration
- ADR-003 Canonical rational time model
- ADR-004 PostgreSQL + pgvector before graph DB
- ADR-005 S3-compatible object storage
- ADR-006 Timeline as NLE-neutral source of truth
- ADR-007 AI provider capability abstraction
- ADR-008 Modular monolith API + scalable workers
