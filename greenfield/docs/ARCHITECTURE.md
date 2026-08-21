# System Architecture — Project Director

## 1. Architectural shape

Project Director is event-driven and workflow-orchestrated. AI reasoning creates structured artifacts; deterministic services execute them.

```text
Web / Future NLE Plugins
          |
       API/BFF
          |
  Domain/Application Layer
          |
   Durable Workflows
     /     |      \
 Media    AI     Render workers
   |       |        |
   +-------+--------+
           |
 PostgreSQL + pgvector
 Object Storage
 Redis (ephemeral only)
```

## 2. Hard boundary: reasoning vs execution

AI agents MAY create or revise:
- ProductionBrief
- StoryProposal
- EditPlan
- CritiqueReport
- bounded TimelinePatch proposals

AI agents MUST NOT:
- directly mutate source assets;
- execute arbitrary shell commands;
- construct unvalidated FFmpeg command strings;
- bypass timeline validation;
- publish content without an explicit product permission path.

Media/render services execute validated typed operations.

## 3. Media ingestion pipeline

1. Register upload and project asset.
2. Multipart upload directly to object storage.
3. Verify checksum/type/duration/limits.
4. FFprobe source streams.
5. Generate proxy/mezzanine, thumbnails and waveform data.
6. Extract normalized audio for analysis.
7. Transcribe with word-level timestamps.
8. Diarise speakers.
9. Detect shots/scenes.
10. Run visual/audio feature extraction.
11. Build/augment Media Intelligence Graph.
12. Compute embeddings/search index.
13. Emit ProjectIntelligenceReady milestones progressively.

All activities are idempotent and keyed by source asset + pipeline version + configuration hash.

## 4. Media Intelligence Graph

The graph is a logical model over relational data, vectors and temporal spans. It does not require a graph database initially.

Every meaningful node has:
- stable ID;
- project ID;
- type;
- source evidence references;
- source start/end time where applicable;
- confidence;
- provenance (detector/model/version);
- structured attributes;
- embedding where useful.

Edges encode relationships such as:
- SPOKEN_BY
- OCCURS_IN
- SHOWS
- ANSWERS
- SUPPORTS
- CONTRADICTS
- REVEALS
- PAYS_OFF
- REFERS_TO
- VISUALLY_SUPPORTS
- SAME_TOPIC
- SAME_ENTITY

The graph supports hybrid retrieval: structured filters + full-text + vector similarity + temporal adjacency.

## 5. Canonical Timeline/EDL

Timeline is the only authoritative edit representation. It is independent of browser playback, FFmpeg, Premiere or Resolve.

Core rules:
- integer timebase/ticks; no floating-point frame positions;
- source ranges and timeline ranges are explicit;
- source media remains immutable;
- every timeline has schema_version and revision/version;
- transitions/effects/captions/audio automation are typed objects;
- unknown extension data is namespaced;
- timeline patches use explicit operations and optimistic concurrency.

Example conceptual item:

```json
{
  "id": "item_01",
  "kind": "video_clip",
  "track_id": "v1",
  "source_asset_id": "asset_cam_a",
  "source_in": 1152000,
  "source_out": 1728000,
  "timeline_in": 0,
  "timeline_out": 576000,
  "timebase": 48000,
  "transform": {"scale": 1.0, "x": 0.0, "y": 0.0},
  "provenance": {
    "created_by": "director_agent",
    "evidence_ids": ["beat_hook_7"]
  }
}
```

## 6. Agent architecture

Agents are stateless reasoning components invoked by workflows/application services. Long-term state is persisted as domain artifacts, not hidden chat memory.

### Executive Producer
Input: user objective + project intelligence + brand profile.
Output: ProductionBrief.

### Story Producer
Input: ProductionBrief + retrieved graph evidence.
Output: ranked StoryProposals with beat/evidence references.

### Director
Input: approved StoryProposal + ProductionBrief + media evidence.
Output: EditPlan containing ordered beats, source candidates, pacing/visual intent and constraints.

### Editor
Primarily deterministic planning/materialization. Converts validated EditPlan into Timeline. AI may rank alternatives but typed algorithms enforce temporal/media correctness.

### Specialist agents
Audio, Captions, Visual Treatment, Shorts, B-roll/Graphics. Each returns bounded patches or recommendations.

### Critic
Input: Timeline + ProductionBrief + graph + technical analysis.
Output: CritiqueReport with severity, exact ranges, evidence, recommendation and confidence. It does not silently rewrite the timeline.

## 7. Provider abstraction

Capabilities, not vendor names, drive application logic.

```text
LLMProvider
- structured_generate(schema, context, policy)
- embed(texts)

TranscriptionProvider
- transcribe(asset, options) -> timed words

VisionProvider
- analyze(frames/segments, requested_capabilities)

DiarizationProvider
- diarize(audio)
```

Every result stores provider/model/version and relevant inference configuration for reproducibility/auditing.

## 8. Data layer

PostgreSQL is authoritative for metadata and structured artifacts. pgvector handles embeddings initially. Large binaries live in object storage. Redis is for cache, rate limiting and transient coordination only.

Recommended tenancy hierarchy:
Workspace -> Project -> Assets / Intelligence / Productions.

Use UUID/ULID-style identifiers and tenant-scoped indexes. Avoid user-provided paths as storage keys.

## 9. Workflow orchestration

Temporal-style workflows:
- IngestSourceWorkflow
- BuildIntelligenceWorkflow
- GenerateStoryProposalsWorkflow
- GenerateEditWorkflow
- CritiqueTimelineWorkflow
- RenderTimelineWorkflow
- GenerateDerivativesWorkflow

Workflow state stores identifiers and small structured values, never large media/transcripts. Activities are retryable; external AI calls use idempotency/application request IDs where supported.

## 10. Rendering

Render planner converts canonical Timeline into a validated RenderPlan. The FFmpeg adapter consumes RenderPlan; agents never emit FFmpeg directly.

Stages:
1. validate timeline;
2. resolve source/proxy/mezzanine locations;
3. calculate media graph/filter graph;
4. render segments/intermediates where beneficial;
5. mix audio;
6. composite captions/graphics;
7. encode delivery target;
8. verify output with FFprobe + integrity checks;
9. persist render manifest.

## 11. Web editor

MVP editor:
- source/program monitor;
- transcript panel;
- timeline tracks;
- waveform;
- split/trim/ripple delete/reorder;
- undo/redo through command history;
- version checkpoints;
- Producer chat that emits proposed structured changes;
- critique markers.

The browser should edit metadata/timeline state, not repeatedly upload/re-render source media.

## 12. Realtime events

Domain events are versioned. Examples:
- asset.uploaded
- asset.proxy.ready
- transcript.partial
- transcript.completed
- intelligence.progress
- story.proposals.ready
- timeline.version.created
- critique.completed
- render.progress
- render.completed

Clients can reconnect using event cursor/sequence IDs.

## 13. Security

- direct-to-storage signed uploads;
- malware/content-type validation as appropriate;
- signed playback URLs/cookies;
- workspace/project authorization on every object;
- encrypted secrets through managed secret store;
- audit log for sensitive mutations;
- no model keys in browser clients;
- configurable provider retention/privacy policies;
- rate/cost controls on expensive AI/render actions.

## 14. Evaluation architecture

Each reasoning artifact has an evaluation suite:
- schema validity;
- evidence grounding;
- temporal validity;
- hallucination rate;
- duplicate/repetition metrics;
- story coherence rubric;
- hook/payoff rubric;
- human preference sets.

A golden-project corpus is established before aggressive prompt/model iteration. Provider/model upgrades run against the corpus before production rollout.

## 15. Scale path

MVP may run a modular monolith API plus separately scalable workers. Do not prematurely split every service into a network microservice. Package/domain boundaries are enforced in code; deployment boundaries split only when compute/scaling/failure characteristics justify it.
