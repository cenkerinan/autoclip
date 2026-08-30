# AI Ad Factory — UGC Production Mode

## Purpose
AI Ad Factory is a first-class production mode inside Project Director. It turns a brand/product brief and assets into high-volume vertical UGC-style advertising for TikTok, Reels and Shorts.

> Upload a product or brief. Generate ads. Let the AI production team do the rest.

It reuses the Media Intelligence Graph, ProductionBrief, Director, canonical Timeline, specialist agents, Critic, renderer and later the Performance Learner.

## Production modes
1. **AI creator UGC** — synthetic presenter/avatar delivers an approved script with product cutaways.
2. **Product/photo-to-motion UGC** — product images become motion-led vertical creative with voice, captions and hooks.
3. **Voice + B-roll** — fast explainer/review/problem-solution creative.
4. **AI-enhanced real UGC** — strengthen real creator/customer footage with hooks, edits, captions, reframes and alternate CTAs.
5. **Testimonial-style** — only from verified/approved testimonial evidence; never invent a real customer's experience.
6. **Founder/expert** — approved identity/avatar or generic synthetic creator explains problem, mechanism, proof and offer.

## Workflow

```text
Campaign Brief
  → Brand/Product Understanding
  → Audience Segments
  → Creative Angles
  → Hook Factory
  → Script Factory
  → Creative Matrix
  → Voice / Avatar / Generated Shots / Product B-roll
  → UGC Director
  → Canonical Timeline
  → Captions / Graphics / Audio / Polish
  → Ad Critic
  → Controlled Variants
  → Batch Render
  → Publish/Export
  → Performance Feedback
  → Next Creative Batch
```

## Creative Matrix
Variants must be structured experiments rather than random regenerations.

Dimensions can include:
- hook
- audience pain/desire
- angle
- creator persona
- proof mechanism
- opening visual
- CTA
- duration
- caption style
- offer framing

Each CreativeVariant stores lineage so we know exactly what changed. The system intelligently samples combinations rather than blindly rendering a full Cartesian product.

## Agents
### Campaign Strategist
Creates campaign hypothesis, segments, objections, angles and testing plan.

### Hook Agent
Generates pain, curiosity, contrarian, demo, transformation, value, comparison, objection and pattern-interrupt hooks.

### Script Agent
Uses: Hook → Problem/Desire → Mechanism/Escalation → Proof → Offer → CTA.

### UGC Director
Specifies social-native delivery, shot changes, product reveals, interruptions, pacing and authenticity cues.

### Creator Casting Agent
Selects an appropriate authorized synthetic creator/avatar/voice profile or recommends real-UGC enhancement.

### Visual Generation Agent
Creates product motion/supporting shots through provider-neutral generation contracts.

### Ad Editor
Materializes approved decisions into the canonical Timeline.

### Ad Critic
Scores thumb-stop potential, first-3-second clarity, authenticity, fatigue risk, pace, proof, objections, product visibility, CTA, brand fit and claims/policy risk.

### Variant Agent
Creates controlled variants that change one or a small number of dimensions, preserving interpretability.

## Provider contracts
Do not hard-code current vendors.

```text
AvatarVideoProvider.generate_presenter(...)
VoiceProvider.synthesize(...)
VideoGenerationProvider.text_to_video(...)
VideoGenerationProvider.image_to_video(...)
VideoGenerationProvider.video_edit(...)
ImageGenerationProvider.generate/edit(...)
PublishingProvider.publish/schedule/fetch_metrics(...)
```

## Compliance and provenance
- Synthetic creator content must not silently impersonate genuine customer testimony.
- Do not invent experiences and attribute them to real people.
- Material product claims link to brand-supplied/approved evidence.
- Support platform-specific synthetic-media disclosures.
- Campaigns have prohibited-claim/legal-copy controls.
- Generated voice/avatar/video assets retain provenance.
- No cloning of a real person's likeness or voice without appropriate authorization.

## New domain objects
- AdCampaign
- AudienceSegment
- CreativeAngle
- HookConcept
- AdScript
- CreatorPersona
- SyntheticAsset
- CreativeVariant
- AdRender
- PublishTarget
- PerformanceSnapshot
- CreativeExperiment
- ExperimentCell

## Ad Factory MVP
A user can:
1. create a campaign;
2. upload a product image and short brief;
3. generate 3 angles and 5 hooks;
4. select/auto-select an angle + hook;
5. generate a 20–35 second UGC script;
6. generate voice;
7. use a synthetic presenter or product-motion visual;
8. create captions/product cutaways;
9. assemble everything into the canonical Timeline;
10. render 3 controlled variants;
11. compare variants side-by-side;
12. retain exact creative lineage.

## Long-term loop

```text
Generate creative batch
 → Publish/test
 → Measure hook/angle/persona/CTA performance
 → Learn
 → Recommend next experiments
 → Generate stronger batch
```

The moat is the closed loop between product understanding, creative strategy, production, controlled experimentation and measured performance.
