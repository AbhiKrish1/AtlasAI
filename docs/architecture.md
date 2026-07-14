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
Absolutely. I also think this is a good point to start documenting the architecture properly. Up until now, the ADRs have been recording major decisions, and the ComfyUI migration is definitely significant enough to warrant several new ADRs.

I'd actually revise the ADR sequence slightly based on what we've learned. These are the decisions we've actually made, rather than the ones we initially thought we'd make.

ADR-047 — Standardize on ComfyUI for Local Image Generation
Decision

AtlasAI will use ComfyUI as the default local image generation backend for Version 1.

Reason

Several local image generation solutions were evaluated. Fooocus provided good manual image generation but its API integration proved unreliable due to compatibility issues with newer Gradio versions and maintenance concerns.

ComfyUI provides:

Stable HTTP API
Workflow-based generation
Large ecosystem
Easy automation
Better long-term extensibility

Since AtlasAI's objective is fully automated video generation rather than interactive image creation, ComfyUI better satisfies the project's architectural goals.

Tradeoff

Pros

Stable REST API
Modular workflows
Easy to extend
Large community support

Cons

Higher initial learning curve
Requires workflow management
Slightly more setup than Fooocus
ADR-048 — Verify External Dependencies Before Integration
Decision

Every external dependency must first be validated independently before integrating it into AtlasAI.

Reason

Testing external systems in isolation separates infrastructure problems from application problems.

The integration process therefore becomes:

Manual Verification
        ↓
Integration Test
        ↓
Service Layer
        ↓
Generator
        ↓
Pipeline

This approach significantly reduces debugging complexity.

Tradeoff

Pros

Easier debugging
Smaller failure surface
Reusable test utilities

Cons

Slightly longer development process
Requires temporary test scripts
ADR-049 — Store ComfyUI Workflows as Project Resources
Decision

ComfyUI workflows will be stored as JSON files inside the AtlasAI repository rather than embedded in Python code.

Example:

backend/
└── resources/
    └── workflows/
        txt2img.json
Reason

The workflow itself is configuration rather than application logic.

Keeping workflows separate allows them to evolve independently of the codebase.

Future improvements (ControlNet, SDXL, Flux, img2img, upscaling) become workflow changes instead of source code modifications.

Tradeoff

Pros

Cleaner architecture
Easier maintenance
Better separation of concerns
Non-programmers can edit workflows

Cons

Requires loading JSON from disk
Node IDs must remain synchronized with the workflow
ADR-050 — Keep ImageEngineService Engine-Agnostic
Decision

ImageEngineService will expose a single public API while hiding all ComfyUI-specific implementation details.

Example:

generate_image(
    positive_prompt,
    negative_prompt,
    output_path
)

The rest of AtlasAI must never know about:

HTTP requests
Workflow JSON
Polling
Prompt IDs
ComfyUI endpoints
Reason

AtlasAI should depend on capabilities, not implementations.

If a future version replaces ComfyUI with another backend, only ImageEngineService should require modification.

Tradeoff

Pros

Low coupling
Easy engine replacement
Easier testing
Cleaner pipeline

Cons

Slight abstraction overhead
Requires one additional service layer
ADR-051 — Keep Workflow Logic Inside ImageEngineService (Version 1)
Decision

Version 1 will not introduce a dedicated WorkflowBuilder abstraction.

The workflow JSON will be loaded directly by ImageEngineService, and only the required prompt fields and filename prefix will be modified.

Reason

The current workflow changes only three values:

Positive prompt
Negative prompt
Output filename

Introducing an additional builder layer would add complexity without meaningful benefit.

Future workflow variations can justify extracting this responsibility when needed.

Tradeoff

Pros

Simpler implementation
Less code
Easier to understand
Faster development

Cons

Workflow editing is coupled to the service
Multiple workflows may require refactoring later
ADR-052 — Keep Services Small and Focused

Decision

Split image generation into multiple focused services instead of one large service.

Reason

Smaller classes are easier to understand, test, debug, and extend.

Tradeoff

More files to manage, but significantly improved maintainability.
# ADR-053: Workflow Parameter Mapping

## Decision
Store workflow parameter mappings in separate `.mapping.json` files alongside ComfyUI workflow templates.

## Reason
Decouple application logic from ComfyUI node IDs and make workflow updates configuration-driven.

## Trade-offs
+ Easier workflow maintenance.
+ Supports multiple workflows without code changes.
- Requires maintaining a small mapping file for each workflow.
# ADR-055: Workflow Template Model

## Decision
Represent workflows as `WorkflowTemplate` objects containing both the workflow definition and parameter mapping.

## Reason
Provide a stable contract between the loader and the image engine while supporting future workflow metadata.

## Trade-offs
+ Clearer interfaces.
+ Easier to extend.
- Adds one lightweight model class.
# ADR-056: Generic Runtime Parameters

## Decision
Pass workflow inputs as a runtime parameter dictionary instead of fixed method arguments.

## Reason
Keep the image engine independent of specific workflow parameters and allow new parameters to be introduced through configuration.

## Trade-offs
+ Workflow-agnostic engine.
+ No API changes when adding new parameters.
- Slightly less compile-time validation of parameter names.
# ADR-057: Data-Driven Parameter Injection

## Decision
Inject workflow parameters by iterating over a runtime parameter dictionary and using the workflow mapping to locate target fields.

## Reason
Make the image engine independent of specific workflow parameters and eliminate code changes when introducing new workflow inputs.

## Trade-offs
+ Fully workflow-agnostic engine.
+ Future parameters require only mapping updates.
+ Simpler orchestration logic.
- Invalid parameter names are ignored unless validated separately.
# ADR-058: Layered Testing Strategy

## Decision
Validate the image engine through unit tests, followed by integration tests, and finally pipeline-level tests.

## Reason
Catch implementation issues at the smallest possible scope before verifying end-to-end behavior.

## Trade-offs
+ Easier debugging.
+ Faster feedback during development.
+ More reliable integration testing.
- Requires writing tests before higher-level features.
# ADR-061: Exception Boundary

## Decision
Services translate third-party and low-level exceptions into AtlasAI domain exceptions before propagating them.

## Reason
Prevent implementation details from leaking across service boundaries and provide a stable error API.

## Trade-offs
+ Decouples business logic from third-party libraries.
+ Easier to swap implementations.
+ Consistent error handling across the project.
- Requires small wrapper code around external library calls.
# ADR-062: Root Exception Type

## Decision
Introduce `AtlasAIError` as the root exception for all project-specific errors.

## Reason
Provide a single exception type that callers can catch while allowing domain-specific exception hierarchies underneath.

## Trade-offs
+ Consistent error handling.
+ Easy to extend with new domains.
- Adds one additional inheritance level.
# ADR-063: Hierarchical Workflow Exceptions

## Decision
Group all workflow-related exceptions under a common `WorkflowError` base class.

## Reason
Allow callers to catch either specific workflow failures or all workflow-related failures through a single exception hierarchy.

## Trade-offs
+ Clear exception organization.
+ Simplifies error handling.
+ Easy to extend with future workflow errors.
- Adds one additional inheritance level.
# ADR-064: ComfyUI Exception Hierarchy

## Decision
Group all ComfyUI-specific failures under a dedicated `ComfyUIError` hierarchy.

## Reason
Isolate infrastructure-level failures from higher application layers and provide a stable error interface.

## Trade-offs
+ Prevents third-party exceptions from leaking.
+ Easier service replacement.
+ Consistent infrastructure error handling.
- Requires translating low-level exceptions inside the service.
# ADR-065: Exception Package Façade

## Decision
Expose AtlasAI exceptions through `backend.exceptions.__init__` rather than importing from individual modules.

## Reason
Provide a stable public interface for exception imports and hide the internal module organization.

## Trade-offs
+ Simpler imports.
+ Easier future refactoring.
+ Cleaner public API.
- Requires maintaining the exported symbol list.
# ADR-066: Centralized JSON Loading

## Decision
Use a private `_load_json()` helper within `WorkflowLoader` to load and validate workflow resources.

## Reason
Avoid duplicated JSON loading logic and provide a single place to translate parsing failures into AtlasAI domain exceptions.

## Trade-offs
+ Simpler public methods.
+ Consistent error handling.
+ Easier maintenance.
- Adds one private helper method.
# ADR-067: Encapsulated ComfyUI Response Parsing

## Decision
Hide ComfyUI history response parsing behind a private helper method.

## Reason
Prevent public methods from depending on ComfyUI's response structure and localize future compatibility changes.

## Trade-offs
+ Better encapsulation.
+ Easier maintenance if the API evolves.
+ Cleaner public methods.
- Adds one private helper.
# ADR-068: Workflow Mapping Validation

## Decision
Validate workflow mappings before injecting runtime parameters.

## Reason
Fail with descriptive AtlasAI exceptions instead of exposing low-level `KeyError`s caused by invalid workflow mappings.

## Trade-offs
+ Clearer diagnostics.
+ Safer workflow updates.
+ Easier debugging.
- Small amount of validation logic during parameter injection.
# ADR-069: Centralized Logging

## Decision
Configure logging through a shared `get_logger()` utility and keep logging configuration separate from application services.

## Reason
Provide consistent logging across AtlasAI while preventing services from managing logging configuration.

## Trade-offs
+ Centralized configuration.
+ Consistent log formatting.
+ Easier future integration with file logging or structured logging.
- Requires one shared utility module.
# ADR-071: Milestone Freeze Policy

## Decision
Freeze the architecture of each milestone after implementation, hardening, logging, and testing are complete. Subsequent changes should be limited to bug fixes, performance improvements, or issues with a clear architectural impact.

## Reason
Maintain stability while allowing future development to build on a reliable foundation without repeated redesigns.

## Trade-offs
+ Predictable development process.
+ Reduced architecture drift.
+ Easier testing and maintenance.
- Some improvements may be intentionally deferred to later milestones.
# ADR-072: Logging Configuration Service

## Decision
Provide centralized logging through a shared logger utility exposing `configure_logging()` and `get_logger()`.

## Reason
Separate logging configuration from application services while allowing future logging backends without modifying service code.

## Trade-offs
+ One configuration point.
+ Consistent logging.
+ Easy future expansion.
- Small shared utility module.
# ADR-073: Centralized Logger Utility

## Decision
Introduce a shared logger utility that configures logging lazily and provides configured loggers through `get_logger()`.

## Reason
Ensure consistent logging across AtlasAI while eliminating the need for services to perform logging initialization.

## Trade-offs
+ Single configuration point.
+ Prevents forgotten initialization.
+ Easy future extension.
- Uses a small module-level initialization flag.
# ADR-074: Logging Granularity

## Decision
Log major workflow operations at INFO level, implementation details at DEBUG level, and failures at ERROR level.

## Reason
Provide useful operational visibility without overwhelming normal application logs.

## Trade-offs
+ Cleaner production logs.
+ More useful debugging.
+ Consistent logging policy.
- Requires choosing log levels carefully during development.
# ADR-076: Centralized Configuration

## Decision

Application-wide configuration shall be centralized in
backend/config/settings.py.

## Reason

Avoid duplicated configuration values and provide a single
source of truth for services.

## Trade-offs

+ Easier maintenance
+ Simpler future deployment
+ Consistent defaults

- One additional module
🚀 ADR-077: Application Service Layer
Decision

Introduce a new Application Service layer that acts as the public interface for AtlasAI.

Frontend
      ↓
FastAPI
      ↓
GenerationService
      ↓
ImageEngineService
      ↓
Infrastructure
Reason

Separate application orchestration from engine implementations.

Trade-offs

✅ Cleaner API

✅ Easier frontend integration

✅ Supports future engines

✅ Better scalability

➖ One additional service layer

I think this is absolutely worth the extra layer.