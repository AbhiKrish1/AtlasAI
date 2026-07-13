Decision 1 — Build a Finishable Product

Decision

AtlasAI v1 will focus on generating a complete YouTube Short from a topic instead of trying to support every possible feature.

Reason

A finished product is significantly more valuable than a large collection of unfinished features.

Trade-off

Less functionality today, but a polished and complete application.
///////
Decision 2 — Build a Pipeline Instead of a Monolith

Decision

AtlasAI will be built as independent pipeline stages instead of one large AI prompt.

Topic
↓

Content

↓

Prompts

↓

Images

↓

Voice

↓

Video

Reason

Each stage has one responsibility and can be improved or replaced independently.

Trade-off

Slightly more code, significantly cleaner architecture.
Decision 3 — Prefer Typed Objects Between Stages

Decision

Each stage returns structured Python objects (Pydantic models) instead of raw strings.

Example:

Topic
↓

ContentPlan

↓

ImagePlan

↓

VideoProject

Reason

Typed contracts make debugging, testing and future expansion much easier.

Decision 4 — Configuration Lives in One Place

Decision

Models, hosts and default settings will never be hardcoded.

Everything is stored inside:

backend/config/settings.py

Reason

Changing models or defaults should require editing one file instead of searching the entire project.
//////
Decision 5 — Separate Business Logic From AI Communication

Decision

AI communication is handled by services.

Business logic is handled by generators.

Example:

ContentGenerator

↓

OllamaService

↓

Ollama

Reason

Switching AI providers should only affect one service.

Decision 6 — Prompt Engineering Is Part of the Codebase

Decision

Prompts are stored separately from application logic.

utils/prompts.py

Reason

Prompt engineering is a first-class part of the application and should be easy to improve.

Decision 7 — Measure Before Optimizing

Decision

Performance improvements must be based on measurements rather than assumptions.

Example

Scene planning took approximately one minute.

This justified redesigning the architecture.

Reason

Optimization should solve real bottlenecks rather than imagined ones.

Decision 8 — Avoid Premature Abstractions

Decision

Do not introduce base classes or complex inheritance until repeated patterns naturally emerge.

Reason

Wrong abstractions are harder to maintain than a small amount of duplicated code.

Principle

First implementation → build it.

Second implementation → duplicate it.

Third implementation → refactor it.

Decision 9 — Refactor When Evidence Suggests a Better Design

Original Architecture

Topic

↓

ScriptAgent

↓

ScenePlanner

↓

PromptGenerator

Problem

Two separate LLM calls doubled content generation time.

New Architecture

Topic

↓

ContentGenerator

↓

PromptGenerator

↓

ImageGenerator

↓

VoiceGenerator

↓

VideoAssembler

Result

One AI request instead of two.

Lower latency.

Better consistency.

Decision 10 — Never Ask AI For Information We Already Know

Example

The title, duration and topic are already available after content generation.

PromptGenerator should receive them directly instead of asking another AI call to regenerate them.

Reason

Reduces hallucinations and unnecessary computation.

Decision 11 — Design For Replaceability

Every major component should be replaceable without affecting the rest of the system.

Example:

Qwen

↓

Llama

↓

Gemma

should only require changing one module.

Similarly,

Fooocus

↓

FLUX

↓

ComfyUI

should not require changes to the pipeline.

Decision 12 — Simplicity Before Scalability

AtlasAI will always choose the simplest solution that satisfies current requirements.

Examples:

One prompts.py file instead of a prompts folder.
No database in Version 1.
No Docker in Version 1.
No user accounts.
No cloud deployment.

Complexity will only be introduced when it becomes necessary.

Decision 13 — Every Module Has One Clear Responsibility

Each major class should answer one question.

Module	Responsibility
ContentGenerator	Create the video's content structure
PromptGenerator	Create image prompts
ImageGenerator	Generate images
VoiceGenerator	Generate narration
VideoAssembler	Produce the final MP4
Decision 14 — AtlasAI Is Not Inspired By Existing Projects Anymore

Originally the project borrowed ideas from Verticals to understand the problem.

As development progressed, AtlasAI evolved into its own architecture.

The goal is no longer:

"Recreate Verticals."

The goal is:

"Build the best local-first AI video pipeline we can design."

Decision 15 — Introduce Pipelines as Orchestrators

Decision

Business logic will live in generators, while orchestration will live in pipeline classes.

Reason

Generators should focus on a single transformation (input → output). Pipelines coordinate those transformations, making it easier to add logging, retries, performance metrics, caching, and future parallel execution without complicating the generators.

Trade-off

One extra layer in the architecture, but significantly cleaner responsibilities and easier future expansion.

Decision#16 — Rename Agents to Generators

Decision

Rename the agents package to generators.

Reason

The components are not autonomous AI agents. Their role is to transform one input into one output.

Using the term "Generator" better reflects their responsibility and avoids confusion with agentic AI systems.

Trade-off

Requires a small refactor now, but results in clearer naming across the project.
ADR #17 — Design Data Models Before Implementation

Decision

Define the core data models (ContentPlan, PromptPlan, ImageSet, etc.) before implementing the generators that produce them.

Reason

The pipeline is fundamentally a flow of data. Designing the contracts first ensures every generator has a clear responsibility and prevents cascading changes when new stages are added.

Trade-off

A small amount of upfront design work, but a much more stable and extensible architecture.
📖 ADR #19 — Freeze Domain Models Before Feature Development

Decision

Before implementing new generators, finalize the domain models that define the data flowing through AtlasAI.

Reason

Generators, pipelines, and tests all depend on these models. Stabilizing them first minimizes rework and keeps the architecture consistent.

Trade-off

A short design pause now, but significantly fewer breaking changes as the project grows.
📖 ADR #20 — Use Structured Outputs Instead of Prompt-Enforced JSON

Decision

AtlasAI will use schema-constrained structured outputs wherever the underlying model supports them, rather than relying solely on prompt instructions like "Return ONLY JSON."

Reason

Prompt-based JSON generation is fragile and can fail when models include extra text. Schema-constrained outputs are more reliable, easier to validate, and integrate naturally with our Pydantic models.

Trade-off

Requires model/provider support for structured outputs. For providers that don't support them, AtlasAI will fall back to prompt-based JSON generation and validation.

ADR #22 — Introduce AtlasProject as the Workflow State

Decision

Introduce an AtlasProject model that represents the complete state of a generation session. Each pipeline stage updates this object instead of passing multiple independent objects.

Reason

A single project object simplifies orchestration, enables checkpointing, supports resuming interrupted generations, and provides a natural data source for the future frontend.

Trade-off

Slightly larger central model, but much simpler pipeline coordination and better extensibility.
📖 ADR #23 — AtlasProject as the Single Source of Truth

Decision

AtlasAI will introduce an AtlasProject object that represents the complete lifecycle of a video generation session. Every pipeline stage reads from and writes to this object.

Reason

Passing independent objects between pipeline stages becomes increasingly difficult as the project grows. A single project model enables checkpointing, resumability, frontend progress tracking, and cleaner orchestration.

Trade-off

A larger central object, but a significantly simpler workflow and future extensibility.


ADR #24 — Standardize Pipeline Stages

Decision

Every pipeline component will implement a common interface:

run(project: AtlasProject) -> AtlasProject

Reason

A consistent interface simplifies orchestration, enables reordering of stages, and makes future additions such as retries, progress tracking, and plugins much easier.

Trade-off

Pipeline stages receive the full project object instead of only the fields they strictly need, but the consistency and simplicity outweigh the extra coupling.
//////
Type	Naming Convention
Models	ContentPlan, PromptPlan, AtlasProject
Generators	ContentGenerator, ImageGenerator
Services	OllamaService, FooocusService
Pipeline	AtlasPipeline
Output Objects	ImageSet, VoiceTrack, VideoProject
/////
📖 ADR #26 — AtlasProject as the Only Mutable State

Decision

During pipeline execution, AtlasProject is the only object whose state changes. All other domain models (ContentPlan, PromptPlan, etc.) are immutable outputs that are attached to the project.

Reason

A single mutable workflow object makes orchestration, checkpointing, debugging, serialization, and future UI integration significantly simpler while keeping the individual domain models focused on representing completed work.

Trade-off

Pipeline stages share access to the same project object, requiring discipline to ensure each stage only modifies the fields it owns.
ADR #27 — Use Domain-Specific Method Names

Decision

Generators will expose a generate() method instead of a generic run().

Reason

The method name reflects the responsibility of the component, making the code more self-documenting and easier to understand.

Trade-off

Slightly less consistency with generic pipeline frameworks, but significantly clearer intent.
📖 ADR #28 — Keep Generators Stateless

Decision

Generators return domain models (ContentPlan, PromptPlan, etc.) instead of mutating AtlasProject directly. The pipeline is responsible for attaching those models to the project and updating progress.

Reason

This keeps generators pure and easy to test. It also centralizes orchestration logic in one place instead of spreading state mutations across multiple classes.

Trade-off

The pipeline performs a small amount of bookkeeping, but generators become simpler, more reusable, and easier to reason about.
📖 ADR #29 — Validate Architecture Before Expanding Features

Decision

Complete and validate the core generation engine before implementing additional generators such as image, voice, or video.

Reason

A stable foundation ensures new features can be added incrementally without repeatedly changing the underlying architecture.

Trade-off

Visible features arrive slightly later, but development accelerates afterward because every new component plugs into a proven workflow.
///
SPRINT 2
///
ADR #30 — Separate Positive and Negative Prompts

Decision

Each scene prompt will explicitly store a positive prompt and a negative prompt instead of a single combined prompt.

Reason

Modern image generation models generally support positive and negative conditioning. Keeping them separate improves readability, makes prompt tuning easier, and avoids embedding generator-specific syntax into a single string.

Trade-off

Slightly larger model, but significantly better flexibility for future image providers.
ADR #31 — Separate Creative Intent From Rendering Style

Decision

PromptGenerator will generate the semantic description of a scene, while rendering style (e.g., cinematic, photorealistic, 8K) will be appended from a centralized style configuration.

Reason

Creative intent and rendering style evolve independently. Separating them reduces token usage, keeps prompts cleaner, and allows global style changes without regenerating scene descriptions.

Trade-off

An additional formatting step in PromptGenerator, but much greater consistency and maintainability.
ADR #32 — LLM Generates Semantic Content Only

Decision

LLMs in AtlasAI will generate only the semantic content (what should be shown), while AtlasAI itself appends rendering styles, quality modifiers, and negative prompts.

Reason

Separating creative intent from rendering configuration makes outputs more consistent, easier to tune, and independent of any specific image generation model.

Trade-off

A small amount of post-processing in the application, but much greater control over the final visual style.
.

📖 ADR #33 — Use Keyword-Oriented Image Prompts

Decision

PromptGenerator will produce concise, comma-separated visual concepts instead of natural-language sentences.

Reason

Stable Diffusion-based image generators generally perform better with keyword-style prompts than conversational descriptions.

Trade-off

Prompts become less readable to humans but produce more consistent image quality.
📖 ADR #34 — Project-Based Output Organization

Decision

Every AtlasAI run will create its own project directory, and all generated assets (images, audio, video, metadata) will live inside it.

Reason

This prevents files from being overwritten, keeps runs isolated, makes debugging easier, and prepares the project for a future frontend and resume functionality.

Trade-off

Slightly deeper folder hierarchy, but much better organization and scalability.
📖 ADR #35 — Timestamped Project Directories

Decision

Each project directory will include a timestamp and a shortened unique identifier (e.g. 20260628_143522_83b4d965) rather than only a UUID.

Reason

Timestamped folders are much easier to browse and debug while remaining unique. They also provide useful context without opening metadata files.

Trade-off

Slightly longer directory names, but significantly better usability during development and future production use.
ADR #37 — Services Own Dependency Lifecycle

Decision

Service classes are responsible not only for communicating with external software but also for ensuring those dependencies are available before use.

Reason

Generators and pipelines should focus solely on content generation. Dependency startup and readiness checks belong inside the corresponding service.

Trade-off

Slightly more responsibility in service classes, but a dramatically simpler application flow and better user experience.
📖 ADR #38 — Prefer Stable Integration APIs Over UI Internals

Decision

AtlasAI will integrate with Fooocus through a stable API interface rather than directly invoking Gradio's internal prediction endpoints.

Reason

Gradio component IDs and dependency graphs are implementation details that can change between releases. A dedicated API provides a more stable contract and reduces maintenance.

Trade-off

A small amount of setup now, in exchange for a much more reliable integration going forward.
📖 ADR #39 — Validate External Integrations Before Abstraction

Decision

Before implementing a service class for an external dependency, first create a small standalone integration test that verifies the API contract.

Reason

It separates "does the dependency work?" from "is our architecture correct?", making debugging much simpler.

Trade-off

One temporary test file, but much less risk of building abstractions on incorrect assumptions.
ADR #40 — Build Adapters from Official Integration Examples

Decision

When integrating with external systems that provide generated client code or official examples, AtlasAI will use those examples as the starting point and wrap them behind service classes rather than reconstructing requests manually.

Reason

Generated examples are version-matched to the running service and significantly reduce the risk of integration bugs.

Trade-off

The initial adapter may contain more parameters than AtlasAI ultimately exposes, but those details remain isolated inside the service layer.
📖 ADR #46 — Image Engine Pivot

Decision

AtlasAI will use ComfyUI as the image generation backend for Version 1 instead of Fooocus.

Reason

After investigating both the built-in Gradio API and FooocusAPI, we determined that integration issues were consuming project time without improving AtlasAI itself. ComfyUI provides a mature API-first architecture that aligns better with AtlasAI's service-oriented design.