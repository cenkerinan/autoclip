# Product Requirements Document — Project Director

## 1. Vision

Project Director is an AI-native production system that turns raw, messy footage into publishable, strategically structured video content. It must behave less like an automation panel and more like a competent producer/director/editor team.

## 2. Jobs to be done

### Primary job
A creator uploads raw footage and describes the desired outcome. The system understands the material, proposes viable stories, creates an editable production, and produces platform-specific derivatives.

### Secondary jobs
- Search raw footage semantically across speech and visuals.
- Turn transcript edits into media edits.
- Remove low-value pauses, filler, false starts and repeated takes.
- Build multicam sequences around active speaker and visual interest.
- Generate caption styles, reframes, zooms, B-roll suggestions and graphics.
- Create Shorts/Reels/TikToks as standalone narratives rather than arbitrary excerpts.
- Critique and revise a generated edit.
- Export renders and later professional NLE timelines.

## 3. Target users

1. Presenter-led YouTube creators.
2. Podcasters and multicam interview producers.
3. Short-form creators and social teams.
4. Agencies producing repeatable branded content.
5. Small businesses that have footage but limited editing/production expertise.

## 4. Core user experience

### Create project
User supplies:
- media files or supported source imports;
- target platform(s);
- desired duration/range;
- genre/content type;
- audience;
- objective;
- tone/style;
- hard constraints and sensitivities;
- optional reference content/brand kit.

### Understand footage
System produces:
- synchronized assets/proxies;
- transcript + word timings;
- speaker identities/diarisation;
- scenes/shots;
- visual entities/events;
- audio quality/noise/music signals;
- semantic topics and claims;
- hooks, reveals, reactions, jokes, emotional beats, CTAs and retention opportunities;
- searchable Media Intelligence Graph.

### Produce
System presents 1–3 story proposals with:
- working title;
- premise;
- hook;
- central question/conflict;
- key beats;
- open loops;
- payoff;
- recommended length;
- evidence/timecodes;
- confidence and risks.

### Direct
On approval, Director generates a structured edit plan:
- sequence order;
- exact source ranges;
- A-roll/B-roll decisions;
- pacing targets;
- visual changes;
- captions/graphics notes;
- music/SFX intent;
- reveal/payoff timing.

### Edit
Editor materializes the plan into the canonical Timeline/EDL. User can edit by timeline, transcript or conversation.

### Critique
Critic audits:
- hook delay;
- repetition;
- dead sections;
- unsupported claims;
- pacing;
- visual monotony;
- audio/technical issues;
- premature payoff;
- brand/sensitivity violations;
- CTA placement.

Critic produces structured findings. Revisions generate a new timeline version; previous versions remain intact.

### Derivatives
Shorts engine identifies independent story candidates, not just high-scoring windows. Each derivative has a complete hook → escalation/value → payoff structure.

## 5. MVP acceptance criteria

The first vertical slice is successful when a user can:

1. create a project and upload one long video;
2. receive a time-aligned transcript and scene segmentation;
3. search semantically and jump to source timecodes;
4. receive at least two grounded story proposals using only material that exists in the source;
5. approve one proposal;
6. receive a non-destructive timeline assembled from source ranges;
7. preview the timeline in the browser;
8. edit the sequence by transcript and basic timeline operations;
9. ask the Producer/Director to make a bounded revision such as “stronger opening” or “hold this reveal until later”;
10. render a valid MP4;
11. view a Critic report linked to exact timeline/source ranges.

## 6. Quality requirements

### Grounding
- Every production claim or selected spoken segment references source evidence/timecodes.
- Agents may not invent quotes or visual events.
- Low-confidence detections are explicitly represented.

### Determinism
- The renderer consumes a versioned timeline schema and produces reproducible output for equivalent inputs/settings.
- Agent creativity never directly mutates raw media files.

### Latency
- Upload/proxy/transcription run asynchronously with visible progress.
- Partial intelligence should become usable before the entire project finishes where dependencies permit.

### Reliability
- Workflows survive API restarts and worker restarts.
- Activities are retryable/idempotent where feasible.
- No process-local set is the source of truth for production state.

### Security/privacy
- Private assets use signed, time-limited access.
- Tenant/project authorization exists at every API boundary.
- Provider data handling and model-retention choices are explicit configuration.
- Destructive project deletion includes object-storage deletion lifecycle.

## 7. Canonical product objects

- Workspace
- User
- Project
- SourceAsset
- MediaStream
- ProxyAsset
- Transcript
- TranscriptWord
- Speaker
- Shot/Scene
- Detection
- StoryBeat
- MediaGraphNode / MediaGraphEdge
- ProductionBrief
- StoryProposal
- EditPlan
- Timeline
- TimelineVersion
- Track
- TimelineItem
- RenderJob
- CritiqueReport
- CritiqueFinding
- Derivative
- BrandProfile
- PerformanceSnapshot (later)

## 8. Non-goals for MVP

- Full Premiere Pro replacement.
- Frame-perfect advanced compositing.
- Generative video as a required dependency.
- Fully autonomous publishing.
- Training proprietary foundation models.
- Mobile-first editing.
- Marketplace/plugin ecosystem.

## 9. Differentiation principles

1. **Story before effects.** Captions, zooms and silence removal are execution details, not the product’s brain.
2. **Evidence-grounded creativity.** Every recommendation is linked to real media.
3. **Conversation changes structured edits.** The chat surface is an interface to versioned production state, not an isolated chatbot.
4. **The Critic closes the loop.** Generation without evaluation is incomplete.
5. **Cross-format intelligence.** The system reasons across long-form and short-form objectives using the same source graph.
6. **Performance feedback becomes institutional memory.** Later versions learn creator-specific patterns from opted-in analytics.

## 10. Product metrics

MVP:
- time to first useful story proposal;
- percent of generated timeline retained by user;
- number of manual cuts before acceptable first export;
- grounded-selection error rate;
- render success rate;
- user-rated story quality;
- Critic precision/false-positive rate.

Post-MVP:
- editing time saved;
- publish rate of generated derivatives;
- retention/CTR lift versus creator baseline;
- revision count to acceptance;
- recommendation acceptance by feature/agent.
