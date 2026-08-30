# Project Director — Greenfield Foundation

> Working title. This directory is a clean-room product and architecture specification for a new AI Producer/Director platform. It does **not** inherit AutoClip application code or architecture.

## North star

A creator should be able to provide raw footage and an objective rather than a list of editing commands. A brand should likewise be able to provide a product/brief and receive a strategically designed batch of UGC-style ad creative.

The platform has two first-class production modes:

1. **Creator Studio** — raw footage → understanding → story → directed edit → derivatives.
2. **AI Ad Factory** — product/brief → audiences/angles/hooks → UGC production → controlled variants → performance learning.

Both modes use the same production brain, canonical Timeline and render engine.

## Product thesis

Project Director combines the useful categories represented by FireCut, OpusClip, Descript and Captions, plus an AI Ad Factory, but the differentiator is an **AI production team**:

- Executive Producer — understands objective, audience, format and constraints.
- Story Producer — discovers viable narratives in raw media.
- Campaign Strategist — creates audiences, angles, objections and creative experiments for ads.
- Hook/Script specialists — develop social-native hooks and scripts.
- Director / UGC Director — chooses structure, scene order, reveals, pacing and visual treatment.
- Editor — converts decisions into a deterministic, non-destructive timeline.
- Audio, Caption, Visual, Generation and Shorts specialists — polish execution.
- Critic / Ad Critic — audits retention, clarity, authenticity, proof, pacing, brand fit and technical quality.
- Performance Learner — connects published outcomes to creative decisions and recommends the next tests.

## Foundational principles

1. **Media first, AI second.** Raw/generated media, transcript, scenes, speakers and derived signals are canonical data, not prompt text.
2. **One canonical Media Intelligence Graph.** Every agent and editor works from the same evidence-aware representation.
3. **One canonical Timeline/EDL.** AI generates edit decisions; rendering is a separate deterministic concern.
4. **Non-destructive always.** Source media is immutable. Every edit is versioned and reversible.
5. **Provider independent.** LLM, transcription, vision, avatar, voice, image/video generation, embeddings and publishing sit behind contracts.
6. **Durable workflows.** Long-running production workflows use durable orchestration rather than in-process state.
7. **Human steerability.** The user can approve, reject or conversationally modify decisions.
8. **Evidence/provenance.** Important creative choices and synthetic assets retain structured evidence/provenance.
9. **Evaluation is a product feature.** Every AI stage has tests, confidence, scoring and measurable quality gates.
10. **Performance learning is opt-in and privacy-aware.** Published analytics can improve recommendations without silently training on private footage.
11. **Controlled experimentation.** Ad variants record exact creative lineage so performance can be attributed to hooks, angles, personas, offers and CTAs.
12. **Authenticity controls.** Synthetic UGC must not masquerade as genuine real-person testimony.

## Greenfield repository target

```text
project-director/
├── apps/
│   ├── web/
│   ├── api/
│   ├── worker-ai/
│   ├── worker-media/
│   └── worker-render/
├── packages/
│   ├── media-schema/
│   ├── timeline/
│   ├── ai-contracts/
│   ├── generation-contracts/
│   ├── events/
│   ├── sdk/
│   └── ui/
├── services/
│   ├── ingest/
│   ├── transcription/
│   ├── vision/
│   ├── intelligence/
│   ├── producer/
│   ├── campaigns/
│   ├── hooks/
│   ├── scripts/
│   ├── generation/
│   ├── director/
│   ├── editor/
│   ├── critic/
│   ├── captions/
│   ├── audio/
│   ├── shorts/
│   ├── render/
│   ├── publishing/
│   └── analytics/
├── workflows/
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

M0 Foundation → M1 Media → M2 Intelligence Graph → M3 Producer → M4 Director → M5 Editor → M6 Automated Polish → M7 Shorts → **M8A AI Ad Factory MVP** → M8B B-roll/Graphics/Music → M9 Critic/Ad Critic → M10 Publishing/Performance Learning → M11 Premiere/Resolve integrations → M12 scaled creative experimentation.

See:
- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/DOMAIN-SCHEMAS.md`
- `docs/SPRINT-0.md`
- `docs/AI-AD-FACTORY.md`
