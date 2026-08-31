# video-use Adoption Audit

## Executive decision

Use `video-use` as a **reference implementation and source of renderer/editor invariants**, not as an application foundation.

Project Director remains greenfield. We should selectively adapt algorithms and rules from `video-use` where they solve concrete media-correctness problems, while reimplementing them behind our own canonical schemas, workflow engine, provider abstractions and test suite.

## File-by-file decision

### helpers/render.py — ADAPT HEAVILY, DO NOT COPY AS-IS

**Keep/adapt:**
- Per-segment extraction before concat.
- Short audio fades at cut boundaries to suppress clicks/pops.
- Non-destructive EDL-driven rendering.
- Output-timeline subtitle remapping.
- Overlay PTS shifting.
- Captions/subtitles applied after overlays.
- Separate draft / preview / final quality tiers.
- Two-pass loudness normalization concept.
- Deterministic render behavior.

**Reimplement:**
- Replace free-form JSON EDL with canonical Timeline schema.
- Use integer/rational timebase, not floating-point seconds as authoritative time.
- No raw ffmpeg filter strings supplied by AI or user-controlled domain objects.
- Build a validated RenderGraph from typed operations.
- Do not force 24 fps / 1080p globally; preserve project settings and handle CFR/VFR intentionally.
- Add source codec/color-space/HDR handling.
- Add deterministic asset hashes and render cache keys.
- Make loudness target a platform/export profile, not a hard-coded global constant.
- Replace local temp-directory assumptions with worker/object-storage architecture.

**Rating:** 9/10 reference value.

### helpers/pack_transcripts.py — REIMPLEMENT THE CONCEPT

**Keep/adapt:**
- Phrase-level compact reading representation.
- Break phrases on speaker change and meaningful silence.
- Retain word-level source timestamps.
- Include audio events in semantic context.
- Provide a token-efficient view for LLM reasoning.

**Problems/limits:**
- 0.5s is a useful default but not universally correct.
- Duration is calculated from first phrase to last phrase, not true source duration.
- Markdown should not be the canonical data model.
- Speaker IDs are provider-shaped.
- No confidence, language, alternative token, alignment-quality or provenance data.

**Our design:**
Canonical TranscriptWord / TranscriptEvent records remain structured. Generate multiple derived semantic views on demand:
- phrase view;
- speaker-turn view;
- topic view;
- story-beat view;
- compact LLM context;
- ad-script evidence view.

Grouping thresholds are content/profile dependent.

**Rating:** 9/10 conceptual value; 4/10 direct code reuse.

### helpers/timeline_view.py — REIMPLEMENT AND EXPAND

**Keep/adapt:**
- Filmstrip + waveform + transcript + silence visualization.
- Visual inspection only around decision points.
- Render-output inspection, not only source inspection.
- Time-range-based visual evidence request.

**Reimplement:**
- Do not sequentially spawn one ffmpeg process per frame.
- Use a single decode/sampling operation or GPU-aware thumbnail service.
- Persist thumbnails, waveform pyramids and visual embeddings.
- Add shot boundaries, faces/active speaker, OCR, motion, focus/exposure and audio-event overlays.
- Make it an API/service and browser component rather than a generated PNG-only helper.
- Support complete project/timeline visualization.

**Rating:** 10/10 product idea; 3/10 direct code reuse.

### helpers/transcribe.py — REIMPLEMENT BEHIND PROVIDER CONTRACT

**Keep/adapt:**
- Extract audio optimized for speech.
- Request word-level timestamps.
- Diarization and audio-event tagging.
- Cache transcription.
- Optional known-speaker count.

**Problems/limits:**
- Hard-coded ElevenLabs endpoint/model.
- Cache key is filename/existence only; changed source can return stale transcript.
- Direct API-key loading from .env.
- No retry/backoff, job state, cost accounting or provider failover.
- No normalized provider-neutral transcript schema.
- Entire WAV upload can be inefficient for very long inputs.

**Our design:**
TranscriptionProvider with ElevenLabs, Whisper/local, Deepgram, AssemblyAI etc. Normalize all results into canonical Transcript schema. Cache by source content hash + provider + model + language/settings. Support chunking, retries and alignment quality.

**Rating:** 8/10 behavioral reference; 2/10 production code reuse.

### helpers/transcribe_batch.py — REPLACE

**Keep:**
- Parallelism.
- Skip already-valid transcription.
- Batch-level progress and error collection.

**Replace with:**
Temporal workflows + bounded worker queues + provider rate limits + retry policies + idempotency + cancellation + observability.

A local ThreadPoolExecutor is correct for a CLI prototype but not our distributed application.

**Rating:** 2/10 direct reuse.

### helpers/grade.py — LEARN FROM, REIMPLEMENT

**Keep/adapt:**
- Analyze before adjusting.
- Conservative automatic correction.
- Native bit-depth normalization.
- Separate corrective grade from creative look.
- Clamp automatic adjustments.

**Problems/limits:**
- Mean/range/saturation heuristics are too simple for professional grading.
- Per-segment independent grading can visibly shift shot-to-shot.
- No skin-tone detection, white-balance estimation, scene consistency, camera matching, HDR/color management or gamut handling.
- Fixed ffmpeg eq heuristics cannot replace a proper color pipeline.

**Our design:**
Build a Color Analysis service:
- exposure/contrast/white-balance signals;
- scene/camera grouping;
- shot matching;
- skin-tone constraints;
- project color-space metadata;
- conservative auto-correction;
- explicit creative look layer;
- temporal consistency checks.

Initially ffmpeg filters can execute the corrections, but typed parameters own the domain representation.

**Rating:** 6/10 reference value; 2/10 direct reuse.

## Production invariants to adopt

These should become automated tests in Project Director:

1. Never cut inside an aligned word when making speech-driven edits unless explicitly forced.
2. Apply bounded edge treatment/crossfade where hard audio edits would click.
3. Recompute caption timing in output-timeline coordinates after cuts.
4. Overlay timing must be relative to the canonical timeline, not source PTS assumptions.
5. Captions must be composed at a layer/order where graphics cannot unintentionally hide them.
6. Source transcripts are immutable/cached and only regenerated when their content/settings fingerprint changes.
7. Source media remains immutable.
8. Preview output must be quality-assured, not merely successfully encoded.
9. Inspect rendered output around edit boundaries.
10. Critic repair loops are bounded and failure is surfaced rather than looping indefinitely.

## Improvements beyond video-use

Project Director must reason over four evidence planes:

```text
Transcript / language
        +
Visual / scene / object / face / action
        +
Audio / music / reaction / ambience
        +
Narrative / campaign / audience intent
        ↓
Media Intelligence Graph
```

Transcript-first is an optimization, not the definition of the content.

For food, travel, ads, sports, demonstrations and cinematic footage, visually strong silent material can carry more editorial value than speech.

## Recommended implementation order

### Sprint 0 / M1
- Canonical integer/rational Timecode.
- Transcript provider contract.
- Content-addressed transcript cache.
- Phrase-view generator based on `pack_transcripts.py` concept.
- Waveform pyramid + thumbnail sampler.
- Typed RenderGraph.
- FFmpeg executor.

### M2/M4
- Visual Evidence Sampler inspired by `timeline_view.py`.
- Word-safe edit snapping.
- Silence/audio-event candidate generation.
- Render-boundary QC.

### M5/M6
- Output-timeline caption mapper.
- Overlay/caption layer ordering validation.
- Loudness export profiles.
- Audio edge treatment.
- draft / preview / final rendering profiles.

### M9
- Technical Critic automated checks based on rendered output.
- Editorial and Director critics on top of the same evidence.

## Bottom line

Do not merge `video-use` into Project Director.

Do build our media layer with its strongest ideas deliberately encoded as typed contracts, renderer invariants, automated tests and Critic checks.

The most valuable ideas are:
1. compact semantic transcript views;
2. on-demand visual drill-down;
3. deterministic EDL rendering;
4. word-safe cuts;
5. output-timeline caption remapping;
6. render-result self-evaluation;
7. bounded automatic repair.

Those are worth incorporating immediately.
