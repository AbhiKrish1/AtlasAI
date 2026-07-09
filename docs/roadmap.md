                AtlasPipeline
                      │
                      ▼
               AtlasProject
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
ContentGenerator  PromptGenerator  VoiceGenerator
      │               │
      ▼               ▼
 ContentPlan     PromptPlan
                      │
                      ▼
              ImageGenerator
                      │
                      ▼
                  ImageSet
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      VoiceTrack            VideoAssembler
                                │
                                ▼
                           VideoProject