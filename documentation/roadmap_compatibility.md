# Phase 7 Roadmap Compatibility Layer Specification

This document details the interface schema between Phase 6 (Skill Gap Analysis) and Phase 7 (Learning Roadmap Generation). The `roadmap_compatibility` field in the response from Phase 6 provides a clean, dependency-resolved representation of missing skills designed for direct, structured consumption by Phase 7.

## Data Schema

The compatibility layer returns a JSON array of skill items:

```json
"roadmap_compatibility": [
  {
    "skill": "Deep Learning",
    "priority": "critical",
    "impact_score": 95,
    "learning_time_weeks": 6,
    "dependencies": [
      "Python",
      "Machine Learning"
    ]
  }
]
```

### Fields

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `skill` | `string` | The exact name of the missing skill. |
| `priority` | `string` | Priority level in lowercase: `"critical"`, `"important"`, or `"optional"`. |
| `impact_score` | `integer` | Score from `0` to `100` representing career impact. |
| `learning_time_weeks` | `integer` | Estimated effort required to acquire the skill in weeks. |
| `dependencies` | `array[string]` | Direct prerequisites required before this skill can be learned. |

## Dependency Resolution Rules

1. **Topological Order**:
   - The outer field `priority_ranking` lists the skills in a topologically sorted sequence resolving prerequisites first (e.g. Python -> Machine Learning -> Deep Learning -> LLMs).
   - Phase 7 should sequence learning path modules utilizing this order.

2. **Effort & Priority Mappings**:
   - Priority translates directly to the roadmap node urgency level.
   - `learning_time_weeks` guides the estimated timeline duration of the respective module.
