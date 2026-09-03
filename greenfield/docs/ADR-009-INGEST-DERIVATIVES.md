# ADR-009 — Content-addressed ingest and analysis derivatives

## Status
Accepted.

## Decision
Every source asset is fingerprinted with SHA-256 after upload verification. Expensive derived work is keyed by source checksum plus pipeline/configuration version.

The ingestion layer normalizes FFprobe output into provider/tool-neutral media contracts before any AI work begins.

Derived assets are planned independently:
- proxy video;
- normalized analysis audio;
- thumbnail/visual-evidence material;
- waveform data.

Audio-only and image-only assets do not run irrelevant video activities.

## Why
Filenames are not identity. The same filename can contain different bytes and the same bytes can arrive under different filenames. Content-addressed identity prevents stale transcription/proxy reuse and enables safe deduplication.

FFprobe output is an external-tool payload and must not become our domain schema. Normalization protects the rest of the application from FFmpeg version details.

## Constraints
- No user/AI supplied ffprobe flags.
- Probe commands use fixed templates and timeouts.
- Source media is immutable.
- Derived outputs record source checksum, pipeline version and configuration hash.
- HDR/color metadata and rotation are retained.
- Canonical timeline time remains integer/rational; probe decimal durations are ingestion metadata converted to bounded integer time.
