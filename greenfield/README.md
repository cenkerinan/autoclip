# Project Director — Greenfield Foundation

> Working title. This directory is a clean-room product and architecture specification for a new AI Producer/Director platform. It does **not** inherit AutoClip application code or architecture.

## North star

A creator should be able to provide raw footage and an objective rather than a list of editing commands.

Example request:

> Make this into the best 15-minute YouTube food-entertainment episode you can. Keep the owner sympathetic, build curiosity around the secret sauce, hold my final verdict until the end, then create eight strong Shorts from unused material.

The system should understand the footage, propose stories, direct the edit, generate a non-destructive timeline, critique its own work, revise it, create derivatives, and eventually learn from publishing performance.

## Product thesis

Project Director combines the useful categories represented by FireCut, OpusClip, Descript and Captions, but the differentiator is an **AI production team**:

- Executive Producer — understands objective, audience, format and constraints.
- Story Producer — discovers viable narratives in raw media.
- Director — chooses structure, scene order, reveals, pacing and visual treatment.
- Editor — converts decisions into a deterministic, non-destructive timeline.
- Audio, Caption, Visual and Shorts specialists — polish execution.
- Critic — audits retention, clarity, repetition, pacing, brand fit and technical quality.
- Performance Learner — later connects published outcomes to creative decisions.

## Foundational principles

1. **Media first, AI second.** Raw media, transcript, scenes, speakers and derived signals are canonical data, not prompt text.
2. **One canonical Media Intelligence Graph.** Every agent and editor works from the same time-aligned representation.
3. **One canonical Timeline/EDL.** AI generates edit decisions; rendering is a separate deterministic concern.
4. **Non-destructive always.** Source media is immutable. Every edit is versioned and reversible.
5. **Provider independent.** LLM, transcription, vision, embeddings and generation capabilities sit behind contracts.
6. **Durable workflows.** Long-running production workflows use Temporal-style durable orchestration rather than in-process state.
7. **Human steerability.** The user can approve, reject or conversationally modify decisions at story, sequence, shot and polish levels.
8. **Explainability without verbosity.** Important creative choices store structured rationales and evidence/timecodes.
9. **Evaluation is a product feature.** Every AI stage has tests, confidence, scoring and measurable quality gates.
10. **Performance learning is opt-in and privacy-aware.** Published analytics can improve recommendations without silently training on private footage.

## Greenfield repository target

```text
project-director/
├── apps/
│   ├── web/                 # Next.js creator workspace/editor
│   ├── api/                 # FastAPI application/API boundary
│   ├── worker-ai/           # intelligence and agent activities
│   ├── worker-media/        # probe/proxy/transcode/scene/audio activities
│   └── worker-render/       # final deterministic renders
├── packages/
│   ├── media-schema/        # canonical Media Intelligence Graph contracts
│   ├── timeline/            # canonical non-destructive Timeline/EDL
│   ├── ai-contracts/        # provider and agent IO contracts
│   ├── events/              # domain/realtime event contracts
│   ├── sdk/                 # typed API SDK
│   └── ui/                  # shared design system
├── services/
│   ├── ingest/
│   ├── transcription/
│   ├── vision/
│   ├── intelligence/
│   ├── producer/
│   ├── director/
│   ├── editor/
│   ├── critic/
│   ├── captions/
│   ├── audio/
│   ├── shorts/
│   ├── render/
│   └── analytics/
├── workflows/               # durable workflow definitions
├── infrastructure/
├── evals/
├── tests/
└── docs/
```

## Initial stack

- Web: Next.js + React + TypeScript
- API: Python + FastAPI
- Database: PostgreSQL + pgvector
- Durable orchestration: Temporal
- Cache/ephemeral coordination: Redis
- Object storage: S3-compatible storage
- Media: FFmpeg/FFprobe; GPU acceleration where justified
- Browser playback/editor: WebCodecs where supported, MSE fallback, Canvas/WebGL for overlays
- Realtime: WebSocket/SSE event stream
- Observability: OpenTelemetry + Sentry + metrics/log aggregation
- Infra: Docker + Terraform; cloud-provider-neutral boundaries where practical

## Delivery sequence

M0 Foundation → M1 Media → M2 Intelligence Graph → M3 Producer → M4 Director → M5 Editor → M6 Automated Polish → M7 Shorts → M8 B-roll/Graphics/Music → M9 Critic → M10 Publishing/Learning → M11 Premiere/Resolve integrations.

See the accompanying documents for the PRD, architecture, canonical schemas, agent contracts and Sprint 0 backlog.