# Memory Types Guide

The Mem0 MCP Server implements a cognitive-inspired memory architecture that organizes memories into different types based on their nature, persistence, and purpose. This guide explains the different memory types available and when to use each.

## Memory Duration Types

Memories in the system are broadly categorized into two duration types:

### Short-Term Memory

Short-term memories are temporary and contextual. They typically relate to the current conversation or task and may not need to be retained long-term.

**Characteristics:**
- Tied to specific sessions/conversations (using `run_id`)
- Intended for immediate context and recent information
- Typically less persistent than long-term memories

**When to use:**
- For tracking conversation context
- For storing working memory during complex tasks
- For maintaining attention focus during multi-step processes

### Long-Term Memory

Long-term memories are persistent and intended to be retrievable across multiple sessions and contexts.

**Characteristics:**
- Preserved across conversations
- More structured and categorized
- Often enriched with metadata

**When to use:**
- For storing preferences, facts, and personal information
- For recording important events and experiences
- For preserving knowledge and skills

## Specific Memory Types

Within these broad categories, the system supports several specific memory types:

### Short-Term Memory Types

#### Conversation Memory

Conversation memories track the content and context of ongoing dialogues.

**Creation:**
```python
mem0_add_short_term_memory(
    text="User mentioned they're planning a trip to Japan next spring.",
    user_id="richard_yaker",
    run_id="conversation_20230512",
    memory_type="conversation"
)
```

#### Working Memory

Working memory holds information that is actively being processed or manipulated.

**Creation:**
```python
mem0_add_short_term_memory(
    text="Working with the user to debug their React component.",
    user_id="richard_yaker",
    run_id="debugging_session_20230512",
    memory_type="working"
)
```

#### Attention Memory

Attention memory highlights particularly important information that needs to be kept in focus.

**Creation:**
```python
mem0_add_short_term_memory(
    text="User needs to submit the application by 5pm today.",
    user_id="richard_yaker",
    run_id="application_session",
    memory_type="attention"
)
```

### Long-Term Memory Types

#### Episodic Memory

Episodic memories record specific events, experiences, or occurrences with temporal context.

**Creation:**
```python
mem0_add_episodic_memory(
    text="I visited the Grand Canyon with my family.",
    user_id="richard_yaker",
    event_date="2023-07-15",
    metadata={"location": "Grand Canyon", "type": "vacation"}
)
```

#### Semantic Memory

Semantic memories store factual knowledge, concepts, and information independent of specific events.

**Creation:**
```python
mem0_add_semantic_memory(
    text="User prefers dark mode in all applications.",
    user_id="richard_yaker",
    category="preferences",
    metadata={"topic": "ui_preferences"}
)
```

#### Procedural Memory

Procedural memories capture skills, processes, and how-to knowledge.

**Creation:**
```python
mem0_add_procedural_memory(
    text="To deploy the application: 1) Build the project, 2) Upload to the server, 3) Restart the service.",
    user_id="richard_yaker",
    skill_area="deployment",
    metadata={"application": "company_webapp"}
)
```

## Selective Memory

In addition to these structured types, the system supports selective memory storage that allows for fine control over what parts of a text are stored.

**Creation:**
```python
mem0_add_memory_selective(
    text="My name is John Smith. I prefer dark mode and using vim keybindings in my IDE.",
    user_id="richard_yaker",
    excludes="My name is.*?\\.",  # Exclude personal identification
    metadata={"topic": "preferences"}
)
```

## Best Practices for Memory Types

### When to Use Each Type

- **Conversation Memory**: For tracking what was discussed in the current session
- **Working Memory**: For tracking progress on complex, multi-step tasks
- **Attention Memory**: For highlighting critical deadlines or important details
- **Episodic Memory**: For recording experiences, events, and occurrences
- **Semantic Memory**: For storing facts, preferences, and knowledge
- **Procedural Memory**: For preserving methods, processes, and skills

### Tips for Effective Memory Organization

1. **Use consistent categories** for semantic memories
2. **Include dates** with episodic memories when possible
3. **Add relevant metadata** to improve searchability
4. **Use descriptive skill_area values** for procedural memories
5. **Link related memories** using the graph features
6. **Use selective memory** for privacy-sensitive information

## Memory Type Transition

The system is designed with an understanding that memories may transition between types. For example:

- A conversation memory might be promoted to semantic memory if it contains important factual information
- Working memory might be converted to procedural memory if it documents a useful process
- Attention memory might be transformed into episodic memory once an important event has occurred

This transition can be managed manually by creating new memories of the appropriate type based on the content of existing memories. 