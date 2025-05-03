# Mem0 MCP Server API Reference

This document provides a comprehensive reference for all the tools available in the Mem0 MCP Server.

## Basic Memory Operations

### mem0_add_memory

```
mem0_add_memory(
    text: str,
    user_id: str,
    agent_id: str = "",
    run_id: str = "",
    metadata: dict = {},
    enable_graph: bool = False,
    includes: str = "",
    excludes: str = "",
    timestamp: int = 0,
    expiration_date: str = ""
) -> dict
```

Adds a memory to Mem0.

**Parameters:**
- `text` (required): The text content to store as a memory
- `user_id` (required): User identifier for the memory
- `agent_id` (optional): Agent identifier
- `run_id` (optional): Session/conversation identifier
- `metadata` (optional): Dictionary of additional metadata
- `enable_graph` (optional): Whether to process the memory for knowledge graph
- `includes` (optional): Regex pattern for text to include
- `excludes` (optional): Regex pattern for text to exclude
- `timestamp` (optional): Custom creation time (Unix timestamp)
- `expiration_date` (optional): Expiration date in ISO 8601 format

**Returns:** Dictionary with status and details of the operation

### mem0_search_memory

```
mem0_search_memory(
    query: str,
    user_id: str,
    agent_id: str = "",
    run_id: str = "",
    filters: str = "",
    threshold: float = 0.0,
    enable_graph: bool = False,
    memory_duration: str = "",
    memory_type: str = ""
) -> dict
```

Searches memories in Mem0.

**Parameters:**
- `query` (required): The search query
- `user_id` (required): User identifier to search within
- `agent_id` (optional): Agent identifier to filter by
- `run_id` (optional): Session identifier to filter by
- `filters` (optional): JSON string of additional filters
- `threshold` (optional): Minimum similarity score (0.0-1.0)
- `enable_graph` (optional): Whether to use graph for retrieval
- `memory_duration` (optional): Filter by "short_term" or "long_term"
- `memory_type` (optional): Filter by memory type (conversation, working, attention, episodic, semantic, procedural)

**Returns:** Dictionary with search results

### mem0_get_all_memories

```
mem0_get_all_memories(
    user_id: str,
    agent_id: str = "",
    run_id: str = "",
    limit: int = 0,
    page: int = 0,
    page_size: int = 0,
    enable_graph: bool = False
) -> dict
```

Gets all memories for a user.

**Parameters:**
- `user_id` (required): User identifier
- `agent_id` (optional): Agent identifier to filter by
- `run_id` (optional): Session identifier to filter by
- `limit` (optional): Maximum number of memories to return
- `page` (optional): Page number for pagination
- `page_size` (optional): Results per page
- `enable_graph` (optional): Whether to include graph context

**Returns:** Dictionary with all matching memories

### mem0_get_memory_by_id

```
mem0_get_memory_by_id(memory_id: str) -> dict
```

Gets a specific memory by ID.

**Parameters:**
- `memory_id` (required): The unique identifier of the memory

**Returns:** Dictionary with the memory details

### mem0_delete_memory

```
mem0_delete_memory(memory_id: str) -> dict
```

Deletes a specific memory.

**Parameters:**
- `memory_id` (required): The unique identifier of the memory to delete

**Returns:** Dictionary with status of the operation

### mem0_update_memory

```
mem0_update_memory(memory_id: str, data: str) -> dict
```

Updates a specific memory.

**Parameters:**
- `memory_id` (required): The unique identifier of the memory to update
- `data` (required): The new text content for the memory

**Returns:** Dictionary with status and details of the operation

## Specialized Memory Types

### mem0_add_short_term_memory

```
mem0_add_short_term_memory(
    text: str,
    user_id: str,
    run_id: str,
    memory_type: str = "conversation",
    metadata: dict = {},
    enable_graph: bool = False
) -> dict
```

Adds a short-term memory.

**Parameters:**
- `text` (required): The text content to store
- `user_id` (required): User identifier
- `run_id` (required): Session identifier for context
- `memory_type` (optional): Type of short-term memory ("conversation", "working", or "attention")
- `metadata` (optional): Additional metadata
- `enable_graph` (optional): Whether to process for knowledge graph

**Returns:** Dictionary with status and details

### mem0_add_episodic_memory

```
mem0_add_episodic_memory(
    text: str,
    user_id: str,
    event_date: str = "",
    metadata: dict = {},
    enable_graph: bool = False
) -> dict
```

Adds an episodic memory (experience or event).

**Parameters:**
- `text` (required): The text content to store
- `user_id` (required): User identifier
- `event_date` (optional): Date of the event in ISO format
- `metadata` (optional): Additional metadata
- `enable_graph` (optional): Whether to process for knowledge graph

**Returns:** Dictionary with status and details

### mem0_add_semantic_memory

```
mem0_add_semantic_memory(
    text: str,
    user_id: str,
    category: str = "",
    metadata: dict = {},
    enable_graph: bool = True
) -> dict
```

Adds a semantic memory (factual knowledge).

**Parameters:**
- `text` (required): The text content to store
- `user_id` (required): User identifier
- `category` (optional): Category of the knowledge
- `metadata` (optional): Additional metadata
- `enable_graph` (optional): Whether to process for knowledge graph (default: True)

**Returns:** Dictionary with status and details

### mem0_add_procedural_memory

```
mem0_add_procedural_memory(
    text: str,
    user_id: str,
    skill_area: str = "",
    metadata: dict = {},
    enable_graph: bool = False
) -> dict
```

Adds a procedural memory (skills, processes).

**Parameters:**
- `text` (required): The text content to store
- `user_id` (required): User identifier
- `skill_area` (optional): Area of skill/expertise
- `metadata` (optional): Additional metadata
- `enable_graph` (optional): Whether to process for knowledge graph

**Returns:** Dictionary with status and details

### mem0_add_memory_selective

```
mem0_add_memory_selective(
    text: str,
    user_id: str,
    includes: str = "",
    excludes: str = "",
    metadata: dict = {},
    run_id: str = "",
    enable_graph: bool = False
) -> dict
```

Adds a memory with control over what parts are stored.

**Parameters:**
- `text` (required): The text content to process
- `user_id` (required): User identifier
- `includes` (optional): Regex pattern for text to include
- `excludes` (optional): Regex pattern for text to exclude
- `metadata` (optional): Additional metadata
- `run_id` (optional): Session identifier
- `enable_graph` (optional): Whether to process for knowledge graph

**Returns:** Dictionary with status and details

## Advanced Features

### mem0_update_categories

```
mem0_update_categories(
    custom_categories: list,
    explanation: str = ""
) -> dict
```

Updates the project's custom memory categories.

**Parameters:**
- `custom_categories` (required): List of category dictionaries
- `explanation` (optional): Explanation for the update

**Returns:** Dictionary with status and details

### mem0_get_categories

```
mem0_get_categories() -> dict
```

Gets the current custom memory categories.

**Parameters:** None

**Returns:** Dictionary with all configured categories

### mem0_set_instructions

```
mem0_set_instructions(
    instructions: str,
    explanation: str = ""
) -> dict
```

Sets custom memory extraction instructions.

**Parameters:**
- `instructions` (required): The instruction text
- `explanation` (optional): Explanation for the update

**Returns:** Dictionary with status and details

### mem0_get_instructions

```
mem0_get_instructions() -> dict
```

Gets the current memory extraction instructions.

**Parameters:** None

**Returns:** Dictionary with the current instructions

### mem0_get_graph_relations

```
mem0_get_graph_relations(
    user_id: str,
    entity: str,
    relation_type: str = ""
) -> dict
```

Gets knowledge graph relationships for an entity.

**Parameters:**
- `user_id` (required): User identifier
- `entity` (required): The entity to get relationships for
- `relation_type` (optional): Type of relationship to filter by

**Returns:** Dictionary with relationship data

### mem0_send_feedback

```
mem0_send_feedback(
    memory_id: str,
    feedback_type: str,
    comments: str = ""
) -> dict
```

Provides feedback on memory quality.

**Parameters:**
- `memory_id` (required): The unique identifier of the memory
- `feedback_type` (required): Type of feedback (helpful, not_helpful, irrelevant, outdated, incomplete)
- `comments` (optional): Additional comments about the feedback

**Returns:** Dictionary with status and details 