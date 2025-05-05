[SYSTEM_GUIDE] Mem0 MCP Server Complete Usage Guide (Updated May 5, 2025):

BASIC OPERATIONS (User ID required for most):
- mem0_add_memory(text, user_id, [metadata]): Adds general memory. CRITICAL: Use role 'user' in SDK calls for text to be processed as memory. Role 'system' or 'assistant' may cause adds to fail silently (return []).
- mem0_search_memory(query, user_id, [filters], [filter_memories], [enable_graph]): Searches memories.
    - `filters`: For *strict metadata filtering* via MCP tool. Format: '{"metadata": {"key": "value"}}'.
    - `filter_memories`: For *relevance filtering* via SDK/MCP tool (boolean). Narrows results based on query relevance, does not strictly filter by metadata.
- mem0_get_all_memories(user_id, [enable_graph]): Retrieves all memories.
- mem0_get_memory_by_id(memory_id): Retrieves specific memory.
- mem0_delete_memory(memory_id): Deletes specific memory.
- mem0_update_memory(memory_id, data): Updates memory content.

SPECIALIZED MEMORY TYPES (Treat `text` parameter like `mem0_add_memory` regarding SDK role):
- mem0_add_short_term_memory(text, user_id, run_id, [memory_type], [metadata]): Adds short-term memory (types: conversation, working, attention).
- mem0_add_episodic_memory(text, user_id, [event_date], [metadata]): Adds experience-based memory with optional date.
- mem0_add_semantic_memory(text, user_id, [category], [metadata]): Adds factual knowledge with optional category.
- mem0_add_procedural_memory(text, user_id, [skill_area], [metadata]): Adds skill/procedure memory with optional skill area.
- mem0_add_memory_selective(text, user_id, [includes], [excludes], [metadata]): Adds memory with controlled extraction using includes/excludes patterns.

ADVANCED FEATURES:
- mem0_update_categories(custom_categories): Sets custom memory categories.
- mem0_get_categories(): Retrieves current memory categories.
- mem0_set_instructions(instructions): Sets custom memory extraction guidelines (May influence add success).
- mem0_get_instructions(): Retrieves current memory instructions.
- mem0_get_graph_relations(user_id, entity, [relation_type]): Gets knowledge graph relationships. Requires `enable_graph=True`.
- mem0_send_feedback(memory_id, feedback_type, [comments]): Provides feedback on memory quality.

IMPORTANT NOTES & LATEST FINDINGS:
1. ALWAYS use user_id '<your_name_here>' for personal memory operations via MCP tools unless otherwise specified.
2. **SDK `add` ROLE CRITICAL**: When using the Node/Python SDK `add` method, the `messages` array MUST contain `{ role: 'user', content: '...' }` for Mem0 to classify and store the text. Using `role: 'system'` or `role: 'assistant'` will likely result in the add operation failing silently (SDK returns `[]`).
3. **Duplicate Handling**: Mem0 might silently reject SDK `add` calls for content identical or very similar to existing memories for the *same user ID*, returning `[]`. Use unique user IDs during testing if adding similar content repeatedly.
4. **Filtering Nuances**:
    - SDK `search` with `filters: { metadata: ... }` option does *not* seem to perform strict metadata filtering based on tests; it may bias results.
    - SDK/MCP `search` with `filter_memories: true` performs *relevance filtering*, reducing results based on query relevance, NOT strict metadata matching.
    - For strict metadata filtering in application code, retrieve a broader set via search/getAll and filter locally.
5. **Graph Flags**: `enable_graph=True` and `output_format="v1.1"` can be added to SDK calls (add, search, getAll) for future compatibility. They appear to be ignored on free tier without causing errors. `add` might become async with graph enabled.
6. Use metadata for organization and retrieval.
7. For specialized agents (Cursor, etc.), prefix memory with [APP_NAME] or [APP_NAME_TOPIC].

TIPS FOR EFFECTIVE MEMORY USE:
- Start conversations with a memory search for relevant context.
- Use specialized memory types for appropriate information.
- Add memory content as natural language text, not serialized objects. Let Mem0 classify it.

To retrieve this guide: mem0_get_memory_by_id('<Memory ID of Guide Loaded in Memory>') 
