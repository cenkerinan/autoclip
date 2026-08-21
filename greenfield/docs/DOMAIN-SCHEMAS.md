# Canonical Domain Schemas

This document defines the contracts that should be stabilized before UI or agent implementation. Concrete Pydantic/TypeScript models should be generated/kept compatible with these semantics.

## 1. Time

Never use floating-point seconds as canonical edit coordinates.

```text
TimePoint { ticks: int64, timebase: int32 }
TimeRange { start: TimePoint, end: TimePoint }
```

Normalize comparisons into a shared rational timebase. Source frame rate is metadata, not the sole timeline clock.

## 2. EvidenceRef

Every AI creative decision can point back to evidence.

```text
EvidenceRef
- id
- project_id
- source_asset_id?
- range?
- evidence_type: transcript | visual | audio | metadata | user_instruction
- object_id?
- confidence: 0..1
- provenance
```

## 3. SourceAsset

```text
SourceAsset
- id
- project_id
- kind: video | audio | image | subtitle
- original_filename
- storage_key
- checksum
- container
- duration
- streams[]
- capture_time?
- camera_label?
- status
- created_at
```

## 4. Transcript

```text
Transcript
- id
- source_asset_id
- language
- provider
- model
- version
- words[]

TranscriptWord
- id
- text
- start
- end
- confidence
- speaker_id?
```

Utterances/paragraphs are derived groupings and must retain word IDs.

## 5. Scene/Shot

```text
Shot
- id
- source_asset_id
- range
- confidence
- representative_frame_key
- attributes: framing, motion, quality, exposure, blur, etc.

Scene
- id
- source_asset_id
- range
- shot_ids[]
- semantic_summary?
```

## 6. Detection

Generic typed detection for extensibility:

```text
Detection
- id
- project_id
- source_asset_id
- range
- type
- label
- confidence
- attributes
- provenance
```

Examples: face, person, food, logo, laughter, applause, active_speaker, text_ocr, reaction, camera_shake, poor_audio.

## 7. Semantic/Story nodes

```text
StoryBeat
- id
- project_id
- type: hook | setup | question | conflict | escalation | reveal | reaction | evidence | payoff | cta | joke | emotional
- summary
- evidence_refs[]
- confidence
- novelty_score?
- emotional_score?
- visual_score?
- information_score?
- sensitivity_flags[]
```

## 8. ProductionBrief

```text
ProductionBrief
- id
- project_id
- version
- format
- platforms[]
- target_duration
- audience
- objective
- tone
- central_promise?
- hard_constraints[]
- sensitivities[]
- brand_profile_id?
- success_criteria[]
- created_from_user_instruction
```

## 9. StoryProposal

```text
StoryProposal
- id
- brief_id
- rank
- working_title
- premise
- central_question
- hook_beat_id
- ordered_beat_ids[]
- payoff_beat_id?
- open_loops[]
- estimated_duration
- evidence_coverage
- confidence
- risks[]
- rationale
```

A StoryProposal is invalid if required beats have no source evidence.

## 10. EditPlan

```text
EditPlan
- id
- story_proposal_id
- version
- sequences[]
- global_pacing
- music_intent?
- caption_intent?
- visual_style_intent?

PlannedSequence
- id
- purpose
- beat_ids[]
- candidate_source_ranges[]
- selected_source_ranges[]
- target_duration
- visual_instructions[]
- audio_instructions[]
- transition_intent?
```

## 11. Timeline

```text
Timeline
- id
- project_id
- schema_version
- version
- timebase
- canvas
- fps
- tracks[]
- markers[]
- metadata

Track
- id
- kind: video | audio | caption | graphic
- order
- muted
- locked
- items[]

TimelineItem
- id
- kind
- timeline_range
- source_ref?
- source_range?
- effects[]
- transitions[]
- gain_automation?
- transform?
- text_payload?
- provenance
```

## 12. TimelinePatch

Conversational/agent edits use a constrained patch protocol rather than arbitrary JSON mutation.

```text
TimelinePatch
- id
- timeline_id
- base_version
- reason
- operations[]
- generated_by
- evidence_refs[]

Operations (initial)
- insert_item
- remove_item
- replace_item_source
- trim_item
- move_item
- split_item
- set_effect
- remove_effect
- set_caption_style
- set_track_gain
- add_marker
```

Every patch validates against `base_version`; conflicts require rebase/regeneration.

## 13. CritiqueReport

```text
CritiqueReport
- id
- timeline_id
- timeline_version
- brief_id
- summary
- findings[]
- overall_scores

CritiqueFinding
- id
- category: hook | pacing | repetition | clarity | grounding | visual | audio | payoff | brand | safety | technical
- severity: info | low | medium | high | blocking
- timeline_range?
- source_evidence_refs[]
- description
- recommendation
- confidence
```

## 14. Provenance

Every model-derived object carries:

```text
Provenance
- producer_type: human | algorithm | ai
- producer_name
- provider?
- model?
- model_version?
- prompt_contract_version?
- pipeline_version
- created_at
```

Do not persist hidden chain-of-thought. Persist concise structured rationale/evidence only.

## 15. Versioning policy

- Schemas use explicit semantic schema versions.
- Timeline edits create immutable versions/checkpoints plus compact command history where appropriate.
- AI artifacts are append-only versions; “regenerate” never silently overwrites the artifact used by an existing timeline.
- Pipeline/model versions are recorded so old projects remain auditable.
